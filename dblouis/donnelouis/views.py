from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods
from django import forms
import json
from datetime import datetime, timedelta
from .models import Article, ImageArticle, Media, Lien, Contact, ForumSujet, ForumReponse, Avion, Notification
import difflib
import re
import requests
from urllib.parse import quote


# ===== FONCTION HELPER POUR LES NOTIFICATIONS =====

def create_notification(type_notif, titre, message, utilisateurs=None, article=None, media=None, sujet_forum=None):
    """
    Créer une notification pour tous les utilisateurs ou des utilisateurs spécifiques
    
    Args:
        type_notif: Type de notification (voir modèle Notification)
        titre: Titre de la notification
        message: Message de la notification
        utilisateurs: Liste des utilisateurs (None = tous les utilisateurs)
        article: Article associé (optionnel)
        media: Média associé (optionnel)
        sujet_forum: Sujet du forum associé (optionnel)
    """
    if utilisateurs is None:
        utilisateurs = User.objects.all()
    
    for user in utilisateurs:
        Notification.objects.create(
            utilisateur=user,
            type_notif=type_notif,
            titre=titre,
            message=message,
            article=article,
            media=media,
            sujet_forum=sujet_forum
        )


# ===== FORMULAIRE AJOUT AVION =====
class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ['nom', 'constructeur', 'type_avion', 'annee_premier_vol', 'capacite', 'description', 'image_principale']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'avion'}),
            'constructeur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Constructeur'}),
            'type_avion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type d\'avion'}),
            'annee_premier_vol': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Année du premier vol'}),
            'capacite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacité'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'image_principale': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de l\'image principale'}),
        }

@login_required(login_url='login')
def ajouter_avion(request):
    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            avion = form.save()
            messages.success(request, "Avion ajouté avec succès !")
            return redirect('detail_catalogue', slug=avion.slug)
    else:
        form = AvionForm()
    return render(request, 'donnelouis/ajouter_avion.html', {'form': form})


# ===== FONCTIONS HELPER POUR LES LIMITES D'ACCÈS =====

def get_article_count_today(request):
    """Retourne le nombre d'articles lus aujourd'hui par un utilisateur non connecté"""
    if request.user.is_authenticated:
        return 0
    
    if 'article_views' not in request.session:
        request.session['article_views'] = []
    
    # Nettoyer les vues d'hier
    today = datetime.now().date().isoformat()
    views = request.session['article_views']
    views = [v for v in views if v.startswith(today)]
    
    return len(views)


def add_article_view(request, article_id):
    """Enregistre la vue d'un article pour un utilisateur non connecté"""
    if request.user.is_authenticated:
        return True
    
    if 'article_views' not in request.session:
        request.session['article_views'] = []
    
    today = datetime.now().date().isoformat()
    request.session['article_views'].append(f"{today}_{article_id}")
    request.session.modified = True


def can_access_content(request):
    """Vérifie si l'utilisateur peut accéder au contenu (articles/médias)"""
    if request.user.is_authenticated:
        return True, 0
    
    count = get_article_count_today(request)
    remaining = max(0, 10 - count)
    
    return remaining > 0, remaining


# ===== FORMULAIRES =====

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nom', 'email', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre message', 'rows': 5}),
        }


class ForumSujetForm(forms.ModelForm):
    auteur_nom = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom (facultatif)'})
    )
    auteur_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email (facultatif)'})
    )
    
    class Meta:
        model = ForumSujet
        fields = ['titre', 'categorie', 'contenu', 'tags']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de votre sujet'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Détaillez votre sujet...'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags (séparés par des virgules)'}),
        }


class ForumReponseForm(forms.ModelForm):
    auteur_nom = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom (facultatif)'})
    )
    auteur_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email (facultatif)'})
    )
    
    class Meta:
        model = ForumReponse
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Votre réponse...'}),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'titre', 'categorie', 'date_publication', 'resume', 'image_principale',
            'theme1_titre', 'theme1_section_a_titre', 'theme1_section_a_texte',
            'theme1_section_b_titre', 'theme1_section_b_texte',
            'theme2_titre', 'theme2_section_a_titre', 'theme2_section_a_texte',
            'theme2_section_b_titre', 'theme2_section_b_texte',
            'theme3_titre', 'theme3_section_a_titre', 'theme3_section_a_texte',
            'theme3_section_b_titre', 'theme3_section_b_texte',
            'conclusion_titre', 'conclusion_texte'
        ]
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'article'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'date_publication': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resume': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Résumé de l\'article'}),
            'image_principale': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de l\'image principale'}),
            
            # Thème 1
            'theme1_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du thème 1'}),
            'theme1_section_a_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre section A'}),
            'theme1_section_a_texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contenu section A'}),
            'theme1_section_b_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre section B'}),
            'theme1_section_b_texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contenu section B'}),
            
            # Thème 2
            'theme2_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du thème 2'}),
            'theme2_section_a_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre section A'}),
            'theme2_section_a_texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contenu section A'}),
            'theme2_section_b_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre section B'}),
            'theme2_section_b_texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contenu section B'}),
            
            # Thème 3
            'theme3_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du thème 3'}),
            'theme3_section_a_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre section A'}),
            'theme3_section_a_texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contenu section A'}),
            'theme3_section_b_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre section B'}),
            'theme3_section_b_texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contenu section B'}),
            
            # Conclusion
            'conclusion_titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la conclusion'}),
            'conclusion_texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Texte de la conclusion'}),
        }


class ImageArticleForm(forms.ModelForm):
    class Meta:
        model = ImageArticle
        fields = ['image_url', 'legende', 'ordre']
        widgets = {
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de l\'image'}),
            'legende': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description/légende de l\'image'}),
            'ordre': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ordre d\'affichage (0, 1, 2...)'}),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'type_media', 'date_publication', 'description', 'url_media', 'image_principale']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'type_media': forms.Select(attrs={'class': 'form-control'}),
            'date_publication': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'url_media': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'image_principale': forms.URLInput(attrs={'class': 'form-control'}),
        }


class LienForm(forms.ModelForm):
    class Meta:
        model = Lien
        fields = ['titre', 'categorie', 'description', 'url', 'image_principale']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'image_principale': forms.URLInput(attrs={'class': 'form-control'}),
        }


# ===== VUES PUBLIQUES =====

def index(request):
    """Page d'accueil"""
    articles_recents = Article.objects.all()[:3]
    total_articles = Article.objects.count()
    
    context = {
        'articles_recents': articles_recents,
        'stats': {
            'total_articles': total_articles,
        }
    }
    return render(request, 'donnelouis/index.html', context)


def liste_articles(request):
    """Liste de tous les articles avec filtres"""
    articles = Article.objects.all()
    
    # Statistiques par catégorie
    stats = {
        'aviation': Article.objects.filter(categorie='aviation').count(),
        'avions': Article.objects.filter(categorie='avions').count(),
        'operations': Article.objects.filter(categorie='operations').count(),
    }
    
    context = {
        'articles': articles,
        'stats': stats,
    }
    return render(request, 'donnelouis/liste_articles.html', context)


def detail_article(request, slug):
    """Détail d'un article"""
    article = get_object_or_404(Article, slug=slug)
    
    # Vérifier l'accès pour les utilisateurs non connectés
    can_access, remaining = can_access_content(request)
    
    if not can_access:
        messages.error(request, "Vous avez atteint votre limite de 10 articles par jour. Connectez-vous pour accéder à plus de contenu !")
        return redirect('liste_articles')
    
    # Enregistrer la vue
    add_article_view(request, article.id)
    
    context = {
        'article': article,
        'is_authenticated': request.user.is_authenticated,
        'remaining_articles': remaining - 1 if not request.user.is_authenticated else None,
    }
    return render(request, 'donnelouis/detail_article.html', context)


def liste_medias(request):
    """Liste de tous les médias (vidéos et podcasts)"""
    medias = Media.objects.all()
    
    # Statistiques par type
    stats = {
        'videos': Media.objects.filter(type_media='video').count(),
        'podcasts': Media.objects.filter(type_media='podcast').count(),
    }
    
    context = {
        'medias': medias,
        'stats': stats,
    }
    return render(request, 'donnelouis/liste_medias.html', context)


def detail_media(request, slug):
    """Détail d'un média"""
    media = get_object_or_404(Media, slug=slug)
    
    # Vérifier l'accès pour les utilisateurs non connectés
    can_access, remaining = can_access_content(request)
    
    if not can_access:
        messages.error(request, "Vous avez atteint votre limite de 10 contenus par jour. Connectez-vous pour accéder à plus !")
        return redirect('liste_medias')
    
    # Enregistrer la vue
    add_article_view(request, media.id)
    
    context = {
        'media': media,
        'is_authenticated': request.user.is_authenticated,
        'remaining_articles': remaining - 1 if not request.user.is_authenticated else None,
    }
    return render(request, 'donnelouis/detail_media.html', context)


def liste_liens(request):
    """Liste de tous les liens"""
    liens = Lien.objects.all()
    
    # Statistiques par catégorie
    stats = {
        'aviation': Lien.objects.filter(categorie='aviation').count(),
        'ressources': Lien.objects.filter(categorie='ressources').count(),
        'communaute': Lien.objects.filter(categorie='communaute').count(),
        'outils': Lien.objects.filter(categorie='outils').count(),
    }
    
    context = {
        'liens': liens,
        'stats': stats,
    }
    return render(request, 'donnelouis/liste_liens.html', context)


# ===== CATALOGUE AVION =====

def liste_catalogue(request):
    """Liste de tous les avions du catalogue"""
    avions = Avion.objects.all()
    
    # Récupérer les constructeurs et types uniques
    constructeurs = Avion.objects.values_list('constructeur', flat=True).distinct().exclude(constructeur='')
    types_avions = Avion.objects.values_list('type_avion', flat=True).distinct().exclude(type_avion='')
    
    # Calculer les comptes par constructeur et type
    constructeurs_stats = {}
    for const in constructeurs:
        count = Avion.objects.filter(constructeur=const).count()
        if count > 0:
            constructeurs_stats[const] = count
    
    types_stats = {}
    for t in types_avions:
        count = Avion.objects.filter(type_avion=t).count()
        if count > 0:
            types_stats[t] = count
    
    stats = {
        'total_avions': avions.count(),
        'constructeurs_count': len(constructeurs_stats),
        'types_count': len(types_stats),
        'constructeurs': constructeurs_stats,
        'types': types_stats,
    }
    context = {
        'avions': avions,
        'stats': stats,
    }
    return render(request, 'donnelouis/liste_catalogue.html', context)

def detail_catalogue(request, slug):
    """Détail d'un avion du catalogue"""
    avion = get_object_or_404(Avion, slug=slug)
    context = {
        'avion': avion,
    }
    return render(request, 'donnelouis/detail_catalogue.html', context)


# ===== PAGE CONTACT =====

def contact(request):
    """Page de contact avec envoi d'email"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Envoyer l'email à louis.rivoal09@gmail.com
            try:
                send_mail(
                    subject=f"Nouveau message de contact: {contact.sujet}",
                    message=f"""
Nom: {contact.nom}
Email: {contact.email}
Sujet: {contact.sujet}

Message:
{contact.message}
                    """,
                    from_email='louis.rivoal09@gmail.com',
                    recipient_list=['louis.rivoal09@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, '✓ Votre message a été envoyé avec succès!')
            except Exception as e:
                messages.warning(request, '⚠ Le message a été enregistré mais l\'email n\'a pas pu être envoyé.')
            
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'donnelouis/contact.html', context)


# ===== VUES PROTÉGÉES (Authentification requise) =====

@login_required(login_url='login')
@login_required(login_url='login')
def ajouter_article(request):
    """Ajouter un article avec images (authentification requise)"""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user.get_full_name() or request.user.username
            article.save()
            
            # Traiter les images si fournies
            images_data = request.POST.getlist('image_url')
            legendes_data = request.POST.getlist('legende')
            ordres_data = request.POST.getlist('ordre')
            
            for i, image_url in enumerate(images_data):
                if image_url:  # Seulement si l'URL n'est pas vide
                    try:
                        ImageArticle.objects.create(
                            article=article,
                            image_url=image_url,
                            legende=legendes_data[i] if i < len(legendes_data) else '',
                            ordre=int(ordres_data[i]) if i < len(ordres_data) and ordres_data[i] else i
                        )
                    except (IndexError, ValueError):
                        pass
            
            # Créer une notification pour tous les utilisateurs
            create_notification(
                type_notif='article_nouveau',
                titre=f"📰 Nouvel article: {article.titre}",
                message=f"{article.auteur} a publié un nouvel article",
                article=article
            )
            
            messages.success(request, '✓ Article ajouté avec succès!')
            return redirect('detail_article', slug=article.slug)
    else:
        form = ArticleForm()
    
    context = {'form': form, 'titre': 'Ajouter un article', 'show_images': True}
    return render(request, 'donnelouis/ajouter_article.html', context)


@login_required(login_url='login')
def ajouter_media(request):
    """Ajouter un média (authentification requise)"""
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            media = form.save(commit=False)
            media.auteur = request.user.get_full_name() or request.user.username
            media.save()
            
            # Créer une notification pour tous les utilisateurs
            create_notification(
                type_notif='media_nouveau',
                titre=f"🎥 Nouveau média: {media.titre}",
                message=f"{media.auteur} a partagé un nouveau {media.get_type_media_display().lower()}",
                media=media
            )
            
            messages.success(request, '✓ Média ajouté avec succès!')
            return redirect('detail_media', slug=media.slug)
    else:
        form = MediaForm()
    
    context = {'form': form, 'titre': 'Ajouter un média'}
    return render(request, 'donnelouis/ajouter_contenu.html', context)


@login_required(login_url='login')
def ajouter_lien(request):
    """Ajouter un lien (authentification requise)"""
    if request.method == 'POST':
        form = LienForm(request.POST)
        if form.is_valid():
            lien = form.save()
            messages.success(request, '✓ Lien ajouté avec succès!')
            return redirect('liste_liens')
    else:
        form = LienForm()
    
    context = {'form': form, 'titre': 'Ajouter un lien'}
    return render(request, 'donnelouis/ajouter_contenu.html', context)

# ===== AUTHENTIFICATION =====

def login_view(request):
    """Page de connexion"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'✓ Bienvenue {user.username}!')
            return redirect('index')
        else:
            messages.error(request, '❌ Identifiant ou mot de passe incorrect')
    
    return render(request, 'donnelouis/login.html')


def logout_view(request):
    """Déconnexion"""
    auth_logout(request)
    # Afficher un message expliquant ce que l'utilisateur perd
    messages.warning(request, '👋 Vous avez été déconnecté. Vous retrouverez les limitation d\'accès (10 articles/jour, présence de publicités). Reconectez-vous pour un accès illimité!')
    return redirect('index')


def signup_view(request):
    """Page d'enregistrement"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation basique
        if not username or not email or not password1 or not password2:
            messages.error(request, '❌ Tous les champs sont requis')
        elif len(password1) < 8:
            messages.error(request, '❌ Le mot de passe doit contenir au moins 8 caractères')
        elif password1 != password2:
            messages.error(request, '❌ Les mots de passe ne correspondent pas')
        elif User.objects.filter(username=username).exists():
            messages.error(request, '❌ Ce nom d\'utilisateur existe déjà')
        elif User.objects.filter(email=email).exists():
            messages.error(request, '❌ Cet email est déjà utilisé')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, '✓ Compte créé avec succès! Connectez-vous maintenant.')
            return redirect('login')
    
    return render(request, 'donnelouis/signup.html')


# ===== IA / CHATGPT =====

def normalize_query(query):
    """Nettoie et normalise une requête en corrigeant les caractères spéciaux"""
    # Remplace les caractères accentués cassés
    query = query.replace('é', 'e').replace('è', 'e').replace('ê', 'e')
    query = query.replace('à', 'a').replace('â', 'a')
    query = query.replace('ù', 'u').replace('û', 'u')
    query = query.replace('ô', 'o').replace('ö', 'o')
    query = query.replace('ç', 'c')
    return query


def correct_spelling(query):
    """Corrige les fautes simples de saisie avec fuzzy matching"""
    mots = query.split()
    mots_corriges = []
    
    # Mots-clés courants du site
    mots_cles = ['article', 'vidéo', 'podcast', 'média', 'lien', 'ressource', 
                 'aviation', 'avion', 'pilote', 'vol', 'actualité', 'news', 'aide']
    
    for mot in mots:
        if len(mot) > 2:
            # Trouve les correspondances proches
            matches = difflib.get_close_matches(mot, mots_cles, n=1, cutoff=0.6)
            if matches:
                mots_corriges.append(matches[0])
            else:
                mots_corriges.append(mot)
        else:
            mots_corriges.append(mot)
    
    return ' '.join(mots_corriges)


def is_greeting(query):
    """Détecte les salutations et réponses simples"""
    greetings = ['salut', 'bonjour', 'bonsoir', 'coucou', 'allo', 'hi', 'hello',
                 'ça va', 'quoi', 'comment', 'etes vous', 'tu vas', 'merci', 'thanks']
    return any(g in query for g in greetings)


def search_web_for_planes(query):
    """Cherche des informations sur les avions via une API gratuite"""
    try:
        # Utiliser DuckDuckGo API (gratuit, sans clé API)
        search_url = f"https://duckduckgo.com/?q=avion+{quote(query)}&format=json"
        response = requests.get(search_url, timeout=3)
        if response.status_code == 200:
            return True  # Résultats trouvés
    except:
        pass
    return False


@require_http_methods(["POST"])
def chat_with_ai(request):
    """IA locale améliorée - Recherche dans la base de données + Web + gestion fautes"""
    try:
        data = json.loads(request.body)
        original_query = data.get('message', '').strip()
        query = original_query.lower()
        
        if not query or len(query) < 1:
            return JsonResponse({
                'message': 'Posez une question sur l\'aviation, les articles, médias ou liens du site! 😊'
            })
        
        # Gestion des salutations simples
        if is_greeting(query):
            greeting_responses = [
                "Salut! 👋 Comment puis-je t'aider concernant l'aviation? 🛫",
                "Bonjour! 😊 Que souhaites-tu savoir sur L'Air du Vol?",
                "Coucou! ✈️ Pose-moi une question sur les articles, vidéos ou ressources!",
                "Hello! 🌍 Je suis là pour t'aider à explorer le monde de l'aviation!"
            ]
            import random
            return JsonResponse({
                'success': True,
                'message': random.choice(greeting_responses),
                'results': []
            })
        
        # Correction orthographique
        corrected_query = correct_spelling(query)
        
        # Normalisation
        clean_query = normalize_query(corrected_query)
        
        # Mots-clés pour détecter le type de question
        is_about_articles = any(w in clean_query for w in ['article', 'lire', 'news', 'actualité', 'nouvelle'])
        is_about_media = any(w in clean_query for w in ['vidéo', 'podcast', 'média', 'video', 'audio', 'youtube'])
        is_about_links = any(w in clean_query for w in ['lien', 'ressource', 'site', 'reference'])
        is_about_aviation = any(w in clean_query for w in ['avion', 'aviation', 'pilot', 'vol', 'plane', 'aircraft'])
        is_about_planes = any(w in clean_query for w in ['a380', 'boeing', 'airbus', 'cessna', 'concorde', 'avion'])
        
        results = []
        
        # Recherche dans les articles
        articles = Article.objects.filter(
            Q(titre__icontains=clean_query) | Q(resume__icontains=clean_query) | 
            Q(theme1_titre__icontains=clean_query) | Q(categorie__icontains=clean_query)
        )[:3]
        
        if articles:
            for article in articles:
                results.append({
                    'type': 'article',
                    'titre': article.titre,
                    'slug': article.slug,
                    'resume': article.resume[:100] + '...'
                })
        
        # Recherche dans les médias
        medias = Media.objects.filter(
            Q(titre__icontains=clean_query) | Q(description__icontains=clean_query) |
            Q(type_media__icontains=clean_query)
        )[:3]
        
        if medias:
            for media in medias:
                results.append({
                    'type': 'media',
                    'titre': media.titre,
                    'slug': media.slug,
                    'description': media.description[:100] + '...'
                })
        
        # Recherche dans les liens
        liens = Lien.objects.filter(
            Q(titre__icontains=clean_query) | Q(description__icontains=clean_query) |
            Q(categorie__icontains=clean_query)
        )[:3]
        
        if liens:
            for lien in liens:
                results.append({
                    'type': 'lien',
                    'titre': lien.titre,
                    'url': lien.url,
                    'description': lien.description[:100] + '...'
                })
        
        # Recherche dans le catalogue d'avions
        avions = Avion.objects.filter(
            Q(nom__icontains=clean_query) | Q(description__icontains=clean_query) |
            Q(constructeur__icontains=clean_query)
        )[:2]
        
        if avions:
            for avion in avions:
                results.append({
                    'type': 'avion',
                    'titre': avion.nom,
                    'slug': avion.slug,
                    'description': avion.description[:100] + '...' if avion.description else 'Catalogue d\'avions'
                })
        
        # Réponse personnalisée selon le type de question
        if results:
            response_text = f"✨ J'ai trouvé {len(results)} résultat{'s' if len(results) > 1 else ''} pour '{original_query}' :"
        else:
            # Messages d'aide contextuels
            if is_about_articles:
                response_text = "📰 Aucun article trouvé sur ce sujet. Consultez la section Articles pour explorer d'autres contenus!"
            elif is_about_media:
                response_text = "🎥 Aucune vidéo ou podcast trouvé. Découvrez nos médias dans la section dédiée!"
            elif is_about_links:
                response_text = "🔗 Aucune ressource trouvée. Parcourez nos liens utiles dans la section Ressources!"
            elif is_about_aviation or is_about_planes:
                response_text = "✈️ Pas de résultat direct. Essayez de poser une question plus détaillée sur un type d'avion ou un sujet spécifique!"
            else:
                response_text = "🤖 Comment puis-je t'aider? Pose-moi une question sur:\n📰 Articles • 🎥 Vidéos • 🔗 Ressources • ✈️ Avions"
        
        return JsonResponse({
            'success': True,
            'message': response_text,
            'results': results
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Erreur de traitement. Réessayez! 😊'}, status=400)
    except Exception as e:
        return JsonResponse({'message': 'Désolé, une erreur est survenue! 🤖'}, status=500)


# ===== FORUM =====

def forum(request):
    """Affiche la liste de tous les sujets du forum"""
    sujets = ForumSujet.objects.all()
    categorie = request.GET.get('categorie', '')
    
    if categorie:
        sujets = sujets.filter(categorie=categorie)
    
    return render(request, 'donnelouis/forum.html', {
        'sujets': sujets,
        'categories': ForumSujet.CATEGORIES,
        'categorie_active': categorie,
    })


def detail_sujet_forum(request, slug):
    """Affiche un sujet du forum avec ses réponses"""
    sujet = get_object_or_404(ForumSujet, slug=slug)
    
    # Incrémenter les vues
    sujet.vues += 1
    sujet.save(update_fields=['vues'])
    
    reponses = sujet.reponses.all()
    
    if request.method == 'POST':
        form = ForumReponseForm(request.POST)
        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.sujet = sujet
            if request.user.is_authenticated:
                reponse.auteur = request.user
            else:
                reponse.auteur_nom = request.POST.get('auteur_nom', 'Anonyme')
                reponse.auteur_email = request.POST.get('auteur_email', '')
            reponse.save()
            
            # Créer une notification pour l'auteur du sujet (s'il est connecté)
            if sujet.auteur:
                Notification.objects.create(
                    utilisateur=sujet.auteur,
                    type_notif='forum_reponse',
                    titre=f"💬 Nouvelle réponse: {sujet.titre}",
                    message=f"{reponse.get_auteur_display()} a répondu à votre sujet",
                    sujet_forum=sujet
                )
            
            messages.success(request, 'Votre réponse a été ajoutée!')
            return redirect('detail_sujet_forum', slug=slug)
    else:
        form = ForumReponseForm()
    
    return render(request, 'donnelouis/detail_sujet_forum.html', {
        'sujet': sujet,
        'reponses': reponses,
        'form': form,
    })


@login_required(login_url='login')
def creer_sujet_forum(request):
    """Créer un nouveau sujet de forum"""
    if request.method == 'POST':
        form = ForumSujetForm(request.POST)
        if form.is_valid():
            sujet = form.save(commit=False)
            if request.user.is_authenticated:
                sujet.auteur = request.user
            else:
                sujet.auteur_nom = request.POST.get('auteur_nom', 'Anonyme')
                sujet.auteur_email = request.POST.get('auteur_email', '')
            sujet.save()
            messages.success(request, 'Votre sujet a été créé!')
            return redirect('detail_sujet_forum', slug=sujet.slug)
    else:
        form = ForumSujetForm()
    
    return render(request, 'donnelouis/creer_sujet_forum.html', {
        'form': form,
    })


@login_required(login_url='login')
def editer_sujet_forum(request, slug):
    """Éditer un sujet de forum"""
    sujet = get_object_or_404(ForumSujet, slug=slug)
    
    # Vérifier que l'utilisateur est l'auteur
    if sujet.auteur != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier ce sujet.")
    
    if request.method == 'POST':
        form = ForumSujetForm(request.POST, instance=sujet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre sujet a été mis à jour!')
            return redirect('detail_sujet_forum', slug=sujet.slug)
    else:
        form = ForumSujetForm(instance=sujet)
    
    return render(request, 'donnelouis/editer_sujet_forum.html', {
        'form': form,
        'sujet': sujet,
    })


@login_required(login_url='login')
def supprimer_sujet_forum(request, slug):
    """Supprimer un sujet de forum"""
    sujet = get_object_or_404(ForumSujet, slug=slug)
    
    # Vérifier que l'utilisateur est l'auteur
    if sujet.auteur != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce sujet.")
    
    if request.method == 'POST':
        sujet.delete()
        messages.success(request, 'Votre sujet a été supprimé!')
        return redirect('forum')
    
    return render(request, 'donnelouis/confirmer_suppression_sujet.html', {
        'sujet': sujet,
    })


@login_required(login_url='login')
def supprimer_reponse_forum(request, sujet_slug, reponse_id):
    """Supprimer une réponse de forum"""
    sujet = get_object_or_404(ForumSujet, slug=sujet_slug)
    reponse = get_object_or_404(ForumReponse, id=reponse_id, sujet=sujet)
    
    # Vérifier que l'utilisateur est l'auteur
    if reponse.auteur != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer cette réponse.")
    
    if request.method == 'POST':
        reponse.delete()
        messages.success(request, 'Votre réponse a été supprimée!')
        return redirect('detail_sujet_forum', slug=sujet.slug)
    
    return render(request, 'donnelouis/confirmer_suppression_reponse.html', {
        'sujet': sujet,
        'reponse': reponse,
    })


@login_required(login_url='login')
@require_http_methods(["POST"])
def voter_reponse_forum(request, slug, reponse_id):
    """Vote sur une réponse du forum (utile/non utile)"""
    sujet = get_object_or_404(ForumSujet, slug=slug)
    reponse = get_object_or_404(ForumReponse, id=reponse_id, sujet=sujet)
    
    # Récupérer le type de vote
    type_vote = request.POST.get('type_vote', 1)
    
    try:
        type_vote = int(type_vote)
        if type_vote not in [1, -1]:
            return JsonResponse({'error': 'Type de vote invalide'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Type de vote invalide'}, status=400)
    
    # Vérifier s'il existe déjà un vote
    vote_existant = reponse.vote_reponse.filter(utilisateur=request.user).first()
    
    if vote_existant:
        # Supprimer le vote existant
        reponse.votes -= vote_existant.type_vote
        vote_existant.delete()
        
        # Si le nouveau vote est différent, le créer
        if vote_existant.type_vote != type_vote:
            from .models import ForumVote
            ForumVote.objects.create(
                reponse=reponse,
                utilisateur=request.user,
                type_vote=type_vote
            )
            reponse.votes += type_vote
    else:
        # Créer un nouveau vote
        from .models import ForumVote
        ForumVote.objects.create(
            reponse=reponse,
            utilisateur=request.user,
            type_vote=type_vote
        )
        reponse.votes += type_vote
    
    reponse.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'votes': reponse.votes
        })
    else:
        return redirect('detail_sujet_forum', slug=slug)

