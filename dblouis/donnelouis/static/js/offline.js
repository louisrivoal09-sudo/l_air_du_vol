/**
 * Gestion du mode offline et du service worker
 */

class OfflineManager {
  constructor() {
    this.isOnline = navigator.onLine;
    this.swRegistration = null;
    this.init();
  }

  async init() {
    // Vérifier le support des service workers
    if (!('serviceWorker' in navigator)) {
      console.warn('❌ Service Workers non supportés');
      return;
    }

    // Enregistrer le service worker
    try {
      this.swRegistration = await navigator.serviceWorker.register(
        '/static/js/service-worker.js',
        { scope: '/' }
      );
      console.log('✅ Service Worker enregistré');
      this.setupServiceWorkerUpdates();
    } catch (err) {
      console.error('❌ Erreur lors de l\'enregistrement du Service Worker:', err);
    }

    // Écouter les changements de connectivité
    window.addEventListener('online', () => this.handleOnline());
    window.addEventListener('offline', () => this.handleOffline());

    // Vérifier l'état initial
    if (!this.isOnline) {
      this.handleOffline();
    }

    // Interface offline
    this.createOfflineUI();
    this.attachListeners();
  }

  setupServiceWorkerUpdates() {
    if (!this.swRegistration) return;

    // Vérifier les mises à jour
    setInterval(() => {
      this.swRegistration.update();
    }, 60000); // Toutes les minutes

    // Notifier si une nouvelle version est disponible
    this.swRegistration.addEventListener('updatefound', () => {
      const newWorker = this.swRegistration.installing;
      newWorker.addEventListener('statechange', () => {
        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
          this.showUpdateNotification();
        }
      });
    });
  }

  createOfflineUI() {
    // Barre offline
    const offlineBar = document.createElement('div');
    offlineBar.id = 'offline-indicator';
    offlineBar.className = 'offline-indicator hidden';
    offlineBar.innerHTML = `
      <div class="offline-content">
        <span class="offline-icon">📡</span>
        <span class="offline-text">Mode offline - Vous consultez les contenus en cache</span>
        <button class="offline-close" title="Fermer">✕</button>
      </div>
    `;
    document.body.appendChild(offlineBar);

    // Modale des paramètres offline
    const modal = document.createElement('div');
    modal.id = 'offline-settings-modal';
    modal.className = 'offline-modal hidden';
    modal.innerHTML = `
      <div class="offline-overlay"></div>
      <div class="offline-modal-content">
        <div class="offline-modal-header">
          <h2>⚙️ Paramètres Offline</h2>
          <button class="offline-modal-close" title="Fermer">✕</button>
        </div>
        
        <div class="offline-modal-body">
          <div class="offline-section">
            <h3>État de la connexion</h3>
            <p class="offline-status">
              <span class="status-indicator online"></span>
              <span id="offline-status-text">Connecté</span>
            </p>
          </div>

          <div class="offline-section">
            <h3>📦 Cache Local</h3>
            <p id="offline-cache-info">Calcul en cours...</p>
            <button id="offline-cache-clear" class="btn-offline">Vider le cache</button>
          </div>

          <div class="offline-section">
            <h3>💾 Contenu en cache</h3>
            <div id="offline-cached-list" class="offline-list">
              <p>Chargement...</p>
            </div>
          </div>

          <div class="offline-section">
            <h3>ℹ️ Information</h3>
            <p>Le mode offline permet de consulter les articles et avions que vous avez mis en cache, sans connexion Internet.</p>
            <p>Cliquez sur l'icône 📥 à côté d'un article pour le mettre en cache.</p>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    // Ajouter le bouton offline à la topbar
    this.createOfflineButton();
  }

  createOfflineButton() {
    const topbar = document.querySelector('.topbar');
    if (!topbar) return;

    const btn = document.createElement('button');
    btn.id = 'offline-btn';
    btn.className = 'offline-btn';
    btn.title = 'Paramètres offline';
    btn.innerHTML = '📡';
    btn.addEventListener('click', () => this.openOfflineSettings());

    // Ajouter avant la fin de la topbar
    const logoDiv = topbar.querySelector('.logo-site');
    if (logoDiv) {
      logoDiv.parentElement.appendChild(btn);
    }
  }

  attachListeners() {
    // Fermer la barre offline
    const closeBtn = document.querySelector('.offline-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        document.getElementById('offline-indicator').classList.add('hidden');
      });
    }

    // Fermer la modale
    const closeModal = document.querySelector('.offline-modal-close');
    if (closeModal) {
      closeModal.addEventListener('click', () => this.closeOfflineSettings());
    }

    const overlay = document.querySelector('.offline-overlay');
    if (overlay) {
      overlay.addEventListener('click', () => this.closeOfflineSettings());
    }

    // Vider le cache
    const clearBtn = document.getElementById('offline-cache-clear');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => this.clearCache());
    }

    // Charger les infos du cache quand la modale s'ouvre
    document.addEventListener('offline-settings-opened', () => {
      this.loadCacheInfo();
    });
  }

  handleOnline() {
    this.isOnline = true;
    document.getElementById('offline-indicator').classList.add('hidden');
    const statusText = document.getElementById('offline-status-text');
    if (statusText) statusText.textContent = 'Connecté';
    const indicator = document.querySelector('.status-indicator');
    if (indicator) {
      indicator.classList.remove('offline');
      indicator.classList.add('online');
    }
  }

  handleOffline() {
    this.isOnline = false;
    document.getElementById('offline-indicator').classList.remove('hidden');
    const statusText = document.getElementById('offline-status-text');
    if (statusText) statusText.textContent = 'Hors ligne';
    const indicator = document.querySelector('.status-indicator');
    if (indicator) {
      indicator.classList.remove('online');
      indicator.classList.add('offline');
    }
  }

  openOfflineSettings() {
    document.getElementById('offline-settings-modal').classList.remove('hidden');
    document.dispatchEvent(new Event('offline-settings-opened'));
  }

  closeOfflineSettings() {
    document.getElementById('offline-settings-modal').classList.add('hidden');
  }

  async loadCacheInfo() {
    try {
      // Taille du cache
      const response = await fetch('/api/offline/cache/');
      if (!response.ok) {
        document.getElementById('offline-cache-info').textContent =
          'Erreur lors du chargement des infos';
        return;
      }

      const data = await response.json();
      const cachedItems = data.cached_items || [];

      document.getElementById('offline-cache-info').textContent =
        `${cachedItems.length} élément(s) en cache`;

      // Afficher la liste
      const list = document.getElementById('offline-cached-list');
      if (cachedItems.length === 0) {
        list.innerHTML = '<p>Aucun contenu en cache</p>';
      } else {
        list.innerHTML = cachedItems.map(item => `
          <div class="offline-item">
            <img src="${item.image}" alt="" class="offline-item-img">
            <div class="offline-item-info">
              <strong>${item.titre || item.nom}</strong>
              <p>${item.resume || item.description || ''}</p>
            </div>
          </div>
        `).join('');
      }
    } catch (err) {
      console.error('Erreur lors du chargement du cache:', err);
      document.getElementById('offline-cached-list').innerHTML =
        '<p>Erreur lors du chargement</p>';
    }
  }

  async clearCache() {
    if (!confirm('Êtes-vous sûr de vouloir vider le cache offline?')) {
      return;
    }

    try {
      const response = await fetch('/api/offline/clear/', { method: 'POST' });
      if (response.ok) {
        alert('Cache vidé avec succès');
        this.loadCacheInfo();
      } else {
        alert('Erreur lors du vidage du cache');
      }
    } catch (err) {
      console.error('Erreur lors du vidage du cache:', err);
    }
  }

  showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'update-notification';
    notification.innerHTML = `
      <div class="update-notification-content">
        <p>Une nouvelle version est disponible!</p>
        <button id="update-btn">Mettre à jour</button>
      </div>
    `;
    document.body.appendChild(notification);

    document.getElementById('update-btn').addEventListener('click', () => {
      if (this.swRegistration && this.swRegistration.waiting) {
        this.swRegistration.waiting.postMessage({ type: 'SKIP_WAITING' });
        window.location.reload();
      }
    });
  }
}

// Initialiser quand le DOM est prêt
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new OfflineManager();
  });
} else {
  new OfflineManager();
}
