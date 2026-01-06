/**
 * Système des commentaires, favoris et signalements sur les articles
 */

class ArticleInteractions {
  constructor(articleId) {
    this.articleId = articleId;
    this.init();
  }

  init() {
    this.createButtons();
    this.attachListeners();
    this.checkFavoriteStatus();
    this.loadComments();
  }

  createButtons() {
    // Trouver le container des actions (après le titre)
    const articleDetail = document.querySelector('[data-article-id]');
    if (!articleDetail) return;

    const header = articleDetail.querySelector('h1');
    if (!header) return;

    // Créer la barre d'actions
    const actionBar = document.createElement('div');
    actionBar.className = 'article-actions-bar';
    actionBar.innerHTML = `
      <div class="article-actions">
        <button class="action-btn favorite-btn" title="Ajouter aux favoris">
          <span class="action-icon">🤍</span>
          <span class="action-label">Favori</span>
        </button>
        <button class="action-btn cache-btn" title="Mettre en cache pour offline">
          <span class="action-icon">📥</span>
          <span class="action-label">Offline</span>
        </button>
        <button class="action-btn comment-btn" title="Ajouter un commentaire">
          <span class="action-icon">💬</span>
          <span class="action-label">Commentaire</span>
        </button>
        <button class="action-btn report-btn" title="Signaler cet article">
          <span class="action-icon">🚩</span>
          <span class="action-label">Signaler</span>
        </button>
      </div>
    `;

    header.parentElement.insertBefore(actionBar, header.nextElementSibling);
  }

  attachListeners() {
    // Favori
    document.querySelector('.favorite-btn')?.addEventListener('click', () => this.toggleFavorite());

    // Cache offline
    document.querySelector('.cache-btn')?.addEventListener('click', () => this.cacheArticle());

    // Commentaire
    document.querySelector('.comment-btn')?.addEventListener('click', () => this.openCommentModal());

    // Signalement
    document.querySelector('.report-btn')?.addEventListener('click', () => this.openReportModal());
  }

  // ==================== FAVORIS ====================
  checkFavoriteStatus() {
    if (!this.isAuthenticated()) {
      document.querySelector('.favorite-btn').disabled = true;
      document.querySelector('.favorite-btn').title = 'Connectez-vous pour ajouter aux favoris';
      return;
    }

    fetch(`/api/article/${this.articleId}/favorite/check/`)
      .then(r => r.json())
      .then(data => {
        if (data.is_favorite) {
          document.querySelector('.favorite-btn').classList.add('active');
          document.querySelector('.favorite-btn .action-icon').textContent = '❤️';
        }
      });
  }

  toggleFavorite() {
    if (!this.isAuthenticated()) {
      alert('Veuillez vous connecter pour ajouter aux favoris');
      return;
    }

    fetch(`/api/article/${this.articleId}/favorite/toggle/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
      }
    })
      .then(r => r.json())
      .then(data => {
        const btn = document.querySelector('.favorite-btn');
        if (data.is_favorite) {
          btn.classList.add('active');
          btn.querySelector('.action-icon').textContent = '❤️';
          this.showNotification('Ajouté aux favoris ❤️');
        } else {
          btn.classList.remove('active');
          btn.querySelector('.action-icon').textContent = '🤍';
          this.showNotification('Retiré des favoris');
        }
      })
      .catch(() => alert('Erreur lors de la mise à jour'));
  }

  // ==================== OFFLINE CACHE ====================
  cacheArticle() {
    if (!this.isAuthenticated()) {
      alert('Veuillez vous connecter pour mettre en cache');
      return;
    }

    fetch(`/api/offline/cache/${this.articleId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
      }
    })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          document.querySelector('.cache-btn').classList.add('cached');
          this.showNotification('Article mis en cache pour offline 📥');
        }
      })
      .catch(() => alert('Erreur lors de la mise en cache'));
  }

  // ==================== COMMENTAIRES ====================
  loadComments() {
    fetch(`/api/article/${this.articleId}/comments/`)
      .then(r => r.json())
      .then(data => {
        const commentsSection = this.getOrCreateCommentsSection();
        
        if (data.comments.length === 0) {
          commentsSection.innerHTML = '<p class="no-comments">Aucun commentaire pour le moment. Soyez le premier!</p>';
        } else {
          commentsSection.innerHTML = '<h3>Commentaires</h3>' + 
            data.comments.map(c => `
              <div class="comment-item">
                <div class="comment-header">
                  <strong class="comment-author">${c.auteur}</strong>
                  <span class="comment-date">${c.date}</span>
                </div>
                <p class="comment-text">${this.escapeHtml(c.contenu)}</p>
              </div>
            `).join('');
        }
      })
      .catch(err => console.error('Erreur lors du chargement des commentaires:', err));
  }

  getOrCreateCommentsSection() {
    let section = document.getElementById('comments-section');
    if (!section) {
      section = document.createElement('div');
      section.id = 'comments-section';
      section.className = 'comments-section';
      document.querySelector('[data-article-id]')?.appendChild(section);
    }
    return section;
  }

  openCommentModal() {
    const modal = this.getOrCreateCommentModal();
    modal.classList.remove('hidden');
  }

  getOrCreateCommentModal() {
    let modal = document.getElementById('comment-modal');
    if (modal) return modal;

    modal = document.createElement('div');
    modal.id = 'comment-modal';
    modal.className = 'modal hidden';
    modal.innerHTML = `
      <div class="modal-overlay"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h2>Ajouter un commentaire</h2>
          <button class="modal-close">✕</button>
        </div>
        <form id="comment-form" class="modal-body">
          ${this.isAuthenticated() ? '' : `
            <div class="form-group">
              <label for="comment-name">Nom</label>
              <input type="text" id="comment-name" name="auteur_nom" class="form-control" required>
            </div>
            <div class="form-group">
              <label for="comment-email">Email</label>
              <input type="email" id="comment-email" name="auteur_email" class="form-control" required>
            </div>
          `}
          <div class="form-group">
            <label for="comment-text">Commentaire</label>
            <textarea id="comment-text" name="contenu" class="form-control" rows="5" required placeholder="Votre commentaire..."></textarea>
            <small>Votre commentaire sera modéré avant publication</small>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-secondary modal-close">Annuler</button>
            <button type="submit" class="btn-primary">Envoyer</button>
          </div>
        </form>
      </div>
    `;

    document.body.appendChild(modal);

    // Attachers les listeners
    modal.querySelector('.modal-close').addEventListener('click', () => {
      modal.classList.add('hidden');
    });
    modal.querySelector('.modal-overlay').addEventListener('click', () => {
      modal.classList.add('hidden');
    });

    modal.querySelector('#comment-form').addEventListener('submit', (e) => {
      e.preventDefault();
      this.submitComment(modal);
    });

    return modal;
  }

  submitComment(modal) {
    const form = modal.querySelector('#comment-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    fetch(`/api/article/${this.articleId}/comment/add/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
      },
      body: JSON.stringify(data)
    })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          this.showNotification(data.message);
          modal.classList.add('hidden');
          form.reset();
          this.loadComments();
        }
      })
      .catch(() => alert('Erreur lors de l\'envoi du commentaire'));
  }

  // ==================== SIGNALEMENT ====================
  openReportModal() {
    const modal = this.getOrCreateReportModal();
    modal.classList.remove('hidden');
  }

  getOrCreateReportModal() {
    let modal = document.getElementById('report-modal');
    if (modal) return modal;

    modal = document.createElement('div');
    modal.id = 'report-modal';
    modal.className = 'modal hidden';
    modal.innerHTML = `
      <div class="modal-overlay"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h2>Signaler cet article</h2>
          <button class="modal-close">✕</button>
        </div>
        <form id="report-form" class="modal-body">
          <div class="form-group">
            <label for="report-reason">Raison du signalement</label>
            <select id="report-reason" name="raison" class="form-control" required>
              <option value="">-- Sélectionnez une raison --</option>
              <option value="spam">Spam</option>
              <option value="offensant">Contenu offensant</option>
              <option value="inexact">Information inexacte</option>
              <option value="publicite">Publicité non autorisée</option>
              <option value="autre">Autre</option>
            </select>
          </div>
          <div class="form-group">
            <label for="report-description">Détails (optionnel)</label>
            <textarea id="report-description" name="description" class="form-control" rows="4" placeholder="Expliquez pourquoi vous signalez cet article..."></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-secondary modal-close">Annuler</button>
            <button type="submit" class="btn-primary">Signaler</button>
          </div>
        </form>
      </div>
    `;

    document.body.appendChild(modal);

    modal.querySelector('.modal-close').addEventListener('click', () => {
      modal.classList.add('hidden');
    });
    modal.querySelector('.modal-overlay').addEventListener('click', () => {
      modal.classList.add('hidden');
    });

    modal.querySelector('#report-form').addEventListener('submit', (e) => {
      e.preventDefault();
      this.submitReport(modal);
    });

    return modal;
  }

  submitReport(modal) {
    const form = modal.querySelector('#report-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    fetch(`/api/article/${this.articleId}/report/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
      },
      body: JSON.stringify(data)
    })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          this.showNotification(data.message);
          modal.classList.add('hidden');
          form.reset();
        }
      })
      .catch(() => alert('Erreur lors du signalement'));
  }

  // ==================== UTILITAIRES ====================
  isAuthenticated() {
    return !!document.querySelector('[data-authenticated="true"]');
  }

  showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'article-notification';
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.classList.add('show');
    }, 10);

    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialiser
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    const articleId = document.querySelector('[data-article-id]')?.dataset.articleId;
    if (articleId) {
      new ArticleInteractions(articleId);
    }
  });
} else {
  const articleId = document.querySelector('[data-article-id]')?.dataset.articleId;
  if (articleId) {
    new ArticleInteractions(articleId);
  }
}
