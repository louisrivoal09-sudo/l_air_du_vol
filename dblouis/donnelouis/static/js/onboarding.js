/**
 * Système d'Onboarding - Tutoriel pour nouveaux utilisateurs
 * Style jeu vidéo avec étapes guidées
 */

class Onboarding {
  constructor() {
    this.currentStep = 0;
    this.isActive = false;
    this.hasSeenTutorial = localStorage.getItem('onboarding-completed') === 'true';
    
    this.steps = [
      {
        id: 'welcome',
        title: '🎯 Bienvenue dans L\'Air du Vol!',
        description: 'Un espace d\'exploration et de partage sur l\'aéronautique. Laisse-moi te montrer les ropes!',
        target: null,
        position: 'center',
        action: null
      },
      {
        id: 'sidebar',
        title: '📚 Menu de Navigation',
        description: 'Clique sur le menu (☰) pour accéder aux différentes sections : Articles, Médias, Liens, Forum, et bien plus!',
        target: '#toggle-sidebar',
        position: 'right',
        action: null
      },
      {
        id: 'exploration',
        title: '🔍 Section Exploration',
        description: 'Découvre des Articles 📰, des Médias 🖥️ et des Liens 🔗 sur l\'aéronautique. Des contenus incroyables t\'attendent!',
        target: null,
        position: 'center',
        action: null
      },
      {
        id: 'forum',
        title: '💬 Forum Communautaire',
        description: 'Partage tes idées, pose des questions, et discute avec d\'autres passionnés d\'aviation!',
        target: null,
        position: 'center',
        action: null
      },
      {
        id: 'ai-assistant',
        title: '🤖 Assistant IA',
        description: 'Clique sur le bouton 💬 en bas à droite pour poser tes questions et obtenir des réponses instantanées!',
        target: '#ai-chat-btn',
        position: 'left',
        action: null
      },
      {
        id: 'settings-button',
        title: '⚙️ Bouton Paramètres',
        description: 'Vois ce bouton en haut à droite de la barre? C\'est le bouton Paramètres Personnels! Clique dessus pour ouvrir les réglages.',
        target: '#user-config-btn',
        position: 'left',
        action: 'openSettings'
      },
      {
        id: 'settings-appearance',
        title: '🎨 Onglet Apparence',
        description: 'Dans les paramètres, tu trouveras l\'onglet "Apparence" pour activer le Mode Sombre ou choisir différents thèmes.',
        target: null,
        position: 'center',
        action: 'focusAppearanceTab'
      },
      {
        id: 'settings-reader',
        title: '📖 Mode Liseuse',
        description: 'L\'onglet "Liseuse" te permet de personnaliser la taille du texte, la police, l\'espacement... Parfait pour la lecture!',
        target: null,
        position: 'center',
        action: 'focusReaderTab'
      },
      {
        id: 'end',
        title: '🚀 C\'est parti!',
        description: 'Tu es prêt à explorer! Ferme ce tutoriel et commence ton aventure. Bon vol! ✈️',
        target: null,
        position: 'center',
        action: 'closeSettings'
      }
    ];

    this.init();
  }

  init() {
    // Ne montrer le tutoriel que si c'est la première visite
    if (!this.hasSeenTutorial && document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.startTutorial());
    } else if (!this.hasSeenTutorial) {
      // Si le DOM est déjà chargé
      setTimeout(() => this.startTutorial(), 500);
    }

    // Créer la modale de tutoriel
    this.createTutorialModal();
    this.createTutorialButton();
  }

  createTutorialModal() {
    const modal = document.createElement('div');
    modal.id = 'onboarding-modal';
    modal.className = 'onboarding-modal hidden';
    modal.innerHTML = `
      <div class="onboarding-overlay"></div>
      <div class="onboarding-spotlight"></div>
      <div class="onboarding-card">
        <div class="onboarding-header">
          <div class="onboarding-progress">
            <div class="onboarding-progress-bar">
              <div class="onboarding-progress-fill"></div>
            </div>
            <span class="onboarding-step-count"><span class="current">1</span>/<span class="total">${this.steps.length}</span></span>
          </div>
          <button class="onboarding-close" title="Sauter le tutoriel">✕</button>
        </div>
        
        <div class="onboarding-content">
          <h2 class="onboarding-title"></h2>
          <p class="onboarding-description"></p>
        </div>
        
        <div class="onboarding-footer">
          <button class="onboarding-btn onboarding-skip">Passer</button>
          <div class="onboarding-dots"></div>
          <button class="onboarding-btn onboarding-next">Suivant</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    this.attachListeners();
  }

  createTutorialButton() {
    // Récupérer le bouton tutoriel du template (maintenant dans la modale IA)
    const btn = document.getElementById('restart-tutorial-btn');
    if (btn) {
      btn.addEventListener('click', () => {
        this.resetAndStart();
      });
    }
  }

  attachListeners() {
    const modal = document.getElementById('onboarding-modal');
    const nextBtn = modal.querySelector('.onboarding-next');
    const skipBtn = modal.querySelector('.onboarding-skip');
    const closeBtn = modal.querySelector('.onboarding-close');

    nextBtn.addEventListener('click', () => this.nextStep());
    skipBtn.addEventListener('click', () => this.skipTutorial());
    closeBtn.addEventListener('click', () => this.skipTutorial());

    // Clavier: Flèches et Entrée
    document.addEventListener('keydown', (e) => {
      if (!this.isActive) return;
      if (e.key === 'ArrowRight' || e.key === 'Enter') this.nextStep();
      if (e.key === 'ArrowLeft') this.prevStep();
      if (e.key === 'Escape') this.skipTutorial();
    });
  }

  startTutorial() {
    if (this.isActive) return;
    this.isActive = true;
    this.currentStep = 0;
    document.getElementById('onboarding-modal').classList.remove('hidden');
    this.showStep(0);
  }

  resetAndStart() {
    localStorage.removeItem('onboarding-completed');
    this.hasSeenTutorial = false;
    this.startTutorial();
  }

  showStep(stepIndex) {
    if (stepIndex < 0 || stepIndex >= this.steps.length) return;

    this.currentStep = stepIndex;
    const step = this.steps[stepIndex];
    const modal = document.getElementById('onboarding-modal');

    // Mettre à jour le contenu
    modal.querySelector('.onboarding-title').textContent = step.title;
    modal.querySelector('.onboarding-description').textContent = step.description;
    modal.querySelector('.onboarding-step-count .current').textContent = stepIndex + 1;

    // Mettre à jour la barre de progression
    const progressFill = modal.querySelector('.onboarding-progress-fill');
    const progress = ((stepIndex + 1) / this.steps.length) * 100;
    progressFill.style.width = progress + '%';

    // Mettre à jour les points de progression
    this.updateProgressDots(stepIndex);

    // Mettre à jour les boutons
    const nextBtn = modal.querySelector('.onboarding-next');
    const skipBtn = modal.querySelector('.onboarding-skip');
    
    if (stepIndex === this.steps.length - 1) {
      nextBtn.textContent = '✨ Terminer';
    } else {
      nextBtn.textContent = 'Suivant';
    }

    // Positionner le spotlight si target
    this.updateSpotlight(step);

    // Positionner la card
    this.updateCardPosition(step);

    // Exécuter l'action si elle existe
    if (step.action) {
      this.executeAction(step.action);
    }
  }

  executeAction(action) {
    switch(action) {
      case 'openSettings':
        setTimeout(() => {
          const settingsBtn = document.getElementById('user-config-btn');
          if (settingsBtn) {
            settingsBtn.click();
          }
        }, 300);
        break;
      
      case 'focusAppearanceTab':
        setTimeout(() => {
          const appearanceBtn = document.querySelector('.settings-tab-btn[data-tab="appearance"]');
          if (appearanceBtn) {
            appearanceBtn.click();
          }
        }, 300);
        break;
      
      case 'focusReaderTab':
        setTimeout(() => {
          const readerBtn = document.querySelector('.settings-tab-btn[data-tab="reader"]');
          if (readerBtn) {
            readerBtn.click();
          }
        }, 300);
        break;
      
      case 'closeSettings':
        setTimeout(() => {
          const closeBtn = document.querySelector('.settings-modal-close');
          if (closeBtn) {
            closeBtn.click();
          }
        }, 300);
        break;
    }
  }

  updateProgressDots(currentStep) {
    const container = document.querySelector('.onboarding-dots');
    container.innerHTML = '';

    for (let i = 0; i < this.steps.length; i++) {
      const dot = document.createElement('span');
      dot.className = `onboarding-dot ${i === currentStep ? 'active' : ''}`;
      dot.addEventListener('click', () => this.showStep(i));
      container.appendChild(dot);
    }
  }

  updateSpotlight(step) {
    const spotlight = document.querySelector('.onboarding-spotlight');
    const overlay = document.querySelector('.onboarding-overlay');

    if (!step.target) {
      spotlight.style.display = 'none';
      overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
      return;
    }

    const target = document.querySelector(step.target);
    if (!target) {
      spotlight.style.display = 'none';
      return;
    }

    const rect = target.getBoundingClientRect();
    const padding = 8;

    spotlight.style.display = 'block';
    spotlight.style.left = (rect.left - padding) + 'px';
    spotlight.style.top = (rect.top - padding) + 'px';
    spotlight.style.width = (rect.width + padding * 2) + 'px';
    spotlight.style.height = (rect.height + padding * 2) + 'px';
    spotlight.style.borderRadius = '8px';

    // Overlay semi-transparent
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
  }

  updateCardPosition(step) {
    const card = document.querySelector('.onboarding-card');
    const modal = document.getElementById('onboarding-modal');

    // Par défaut, centrer
    if (!step.target || step.position === 'center') {
      card.style.position = 'fixed';
      card.style.left = '50%';
      card.style.top = '50%';
      card.style.transform = 'translate(-50%, -50%)';
      return;
    }

    const target = document.querySelector(step.target);
    if (!target) {
      card.style.position = 'fixed';
      card.style.left = '50%';
      card.style.top = '50%';
      card.style.transform = 'translate(-50%, -50%)';
      return;
    }

    const rect = target.getBoundingClientRect();
    const cardWidth = card.offsetWidth;
    const cardHeight = card.offsetHeight;
    const gap = 20;

    card.style.position = 'fixed';
    card.style.transform = 'none';

    // Position selon la direction
    if (step.position === 'right') {
      card.style.left = (rect.right + gap) + 'px';
      card.style.top = (rect.top - cardHeight / 2 + rect.height / 2) + 'px';
    } else if (step.position === 'left') {
      card.style.left = (rect.left - cardWidth - gap) + 'px';
      card.style.top = (rect.top - cardHeight / 2 + rect.height / 2) + 'px';
    } else if (step.position === 'bottom') {
      card.style.left = (rect.left - cardWidth / 2 + rect.width / 2) + 'px';
      card.style.top = (rect.bottom + gap) + 'px';
    } else if (step.position === 'top') {
      card.style.left = (rect.left - cardWidth / 2 + rect.width / 2) + 'px';
      card.style.top = (rect.top - cardHeight - gap) + 'px';
    }

    // Vérifier que la card ne dépasse pas l'écran
    const finalRect = card.getBoundingClientRect();
    if (finalRect.left < 10) {
      card.style.left = '10px';
    }
    if (finalRect.right > window.innerWidth - 10) {
      card.style.left = (window.innerWidth - cardWidth - 10) + 'px';
    }
    if (finalRect.top < 10) {
      card.style.top = '10px';
    }
  }

  nextStep() {
    if (this.currentStep < this.steps.length - 1) {
      this.showStep(this.currentStep + 1);
    } else {
      this.completeTutorial();
    }
  }

  prevStep() {
    if (this.currentStep > 0) {
      this.showStep(this.currentStep - 1);
    }
  }

  skipTutorial() {
    this.completeTutorial();
  }

  completeTutorial() {
    localStorage.setItem('onboarding-completed', 'true');
    this.hasSeenTutorial = true;
    this.isActive = false;
    
    const modal = document.getElementById('onboarding-modal');
    modal.classList.add('fade-out');
    
    setTimeout(() => {
      modal.classList.add('hidden');
      modal.classList.remove('fade-out');
      
      // Afficher le bouton pour redémarrer
      const restartBtn = document.getElementById('restart-tutorial-btn');
      if (restartBtn) {
        restartBtn.style.display = 'block';
      }
    }, 300);
  }
}

// Initialiser le tutoriel quand le DOM est prêt
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new Onboarding();
  });
} else {
  new Onboarding();
}
