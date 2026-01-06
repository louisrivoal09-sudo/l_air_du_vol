/**
 * SYSTÈME DE CONFIGURATION UTILISATEUR UNIFIÉ - L'AIR DU VOL
 * Mode sombre + Liseuse + Paramètres utilisateur en une modale
 */

class UserSettings {
  constructor() {
    this.settings = {
      // Dark mode
      theme: localStorage.getItem('theme') || 'auto',
      
      // Reader mode
      readerEnabled: localStorage.getItem('readerEnabled') === 'true',
      luminosity: parseInt(localStorage.getItem('luminosity')) || 100,
      fontFamily: localStorage.getItem('fontFamily') || 'system',
      fontSize: parseInt(localStorage.getItem('fontSize')) || 100,
      lineHeight: parseFloat(localStorage.getItem('lineHeight')) || 1.6,
      letterSpacing: parseFloat(localStorage.getItem('letterSpacing')) || 0,
      marginWidth: parseFloat(localStorage.getItem('marginWidth')) || 2,
      backgroundColor: localStorage.getItem('backgroundColor') || '#f5f1e8',
      textColor: localStorage.getItem('textColor') || '#2c2c2c',
      focusMode: localStorage.getItem('focusMode') === 'true',
      reduceAnimations: localStorage.getItem('reduceAnimations') !== 'false'
    };
    
    this.modalOpen = false;
    this.init();
  }

  init() {
    console.log('✅ Système de configuration utilisateur initialisé');
    this.createButton();
    this.createModal();
    this.attachListeners();
    this.applyTheme();
    this.applyReaderMode(); // Apply reader mode on page load
  }

  createButton() {
    const topbar = document.querySelector('.topbar');
    if (!topbar) return;

    // Créer le bouton de configuration
    const configBtn = document.createElement('button');
    configBtn.id = 'user-config-btn';
    configBtn.className = 'user-config-btn';
    configBtn.title = 'Paramètres utilisateur';
    configBtn.innerHTML = '⚙️';
    configBtn.style.cssText = `
      background: none;
      border: none;
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0.5rem;
      margin-right: 1rem;
      transition: all 0.3s ease;
      border-radius: 0.5rem;
    `;

    configBtn.addEventListener('click', () => this.openModal());

    // Insérer dans la topbar
    topbar.appendChild(configBtn);
  }

  createModal() {
    // Vérifier si la modale existe
    if (document.getElementById('user-settings-modal')) {
      return;
    }

    const modal = document.createElement('div');
    modal.id = 'user-settings-modal';
    modal.className = 'user-settings-modal';
    modal.innerHTML = `
      <div class="settings-modal-overlay"></div>
      <div class="settings-modal-content">
        <div class="settings-modal-header">
          <h2>⚙️ Paramètres Utilisateur</h2>
          <button class="settings-close-btn" title="Fermer">✕</button>
        </div>

        <div class="settings-modal-body">
          <!-- Onglets -->
          <div class="settings-tabs">
            <button class="settings-tab-btn active" data-tab="appearance">🌓 Apparence</button>
            <button class="settings-tab-btn" data-tab="reader">📖 Liseuse</button>
          </div>

          <!-- Contenu des onglets -->
          <div class="settings-tabs-content">
            
            <!-- Onglet Apparence (Dark Mode) -->
            <div class="settings-tab-content active" data-tab="appearance">
              <div class="settings-group">
                <h3>Thème</h3>
                <div class="theme-options">
                  <label class="radio-option">
                    <input type="radio" name="theme" value="auto" ${this.settings.theme === 'auto' ? 'checked' : ''}>
                    <span>🔄 Automatique</span>
                  </label>
                  <label class="radio-option">
                    <input type="radio" name="theme" value="light" ${this.settings.theme === 'light' ? 'checked' : ''}>
                    <span>☀️ Clair</span>
                  </label>
                  <label class="radio-option">
                    <input type="radio" name="theme" value="dark" ${this.settings.theme === 'dark' ? 'checked' : ''}>
                    <span>🌙 Sombre</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Onglet Liseuse -->
            <div class="settings-tab-content" data-tab="reader">
              
              <!-- Toggle Liseuse -->
              <div class="settings-group">
                <label class="toggle-label">
                  <input type="checkbox" id="reader-toggle" class="toggle-input" ${this.settings.readerEnabled ? 'checked' : ''}>
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Activer le mode liseuse</span>
                </label>
              </div>

              <!-- Luminosité -->
              <div class="settings-group">
                <label for="setting-luminosity">💡 Luminosité</label>
                <div class="slider-container">
                  <input type="range" id="setting-luminosity" min="50" max="150" value="${this.settings.luminosity}" class="settings-slider">
                  <span class="slider-value" id="luminosity-value">${this.settings.luminosity}%</span>
                </div>
              </div>

              <!-- Taille Police -->
              <div class="settings-group">
                <label for="setting-fontSize">🔤 Taille du texte</label>
                <div class="slider-container">
                  <input type="range" id="setting-fontSize" min="80" max="150" value="${this.settings.fontSize}" class="settings-slider">
                  <span class="slider-value" id="fontSize-value">${this.settings.fontSize}%</span>
                </div>
              </div>

              <!-- Police -->
              <div class="settings-group">
                <label for="setting-fontFamily">✍️ Police</label>
                <select id="setting-fontFamily" class="settings-select">
                  <option value="system" ${this.settings.fontFamily === 'system' ? 'selected' : ''}>Système</option>
                  <option value="serif" ${this.settings.fontFamily === 'serif' ? 'selected' : ''}>Serif</option>
                  <option value="sans-serif" ${this.settings.fontFamily === 'sans-serif' ? 'selected' : ''}>Sans-serif</option>
                  <option value="mono" ${this.settings.fontFamily === 'mono' ? 'selected' : ''}>Monospace</option>
                  <option value="georgia" ${this.settings.fontFamily === 'georgia' ? 'selected' : ''}>Georgia</option>
                  <option value="verdana" ${this.settings.fontFamily === 'verdana' ? 'selected' : ''}>Verdana</option>
                </select>
              </div>

              <!-- Interligne -->
              <div class="settings-group">
                <label for="setting-lineHeight">📏 Interligne</label>
                <div class="slider-container">
                  <input type="range" id="setting-lineHeight" min="1.4" max="2.0" step="0.1" value="${this.settings.lineHeight}" class="settings-slider">
                  <span class="slider-value" id="lineHeight-value">${this.settings.lineHeight}</span>
                </div>
              </div>

              <!-- Espacement -->
              <div class="settings-group">
                <label for="setting-letterSpacing">⎸ Espacement lettres</label>
                <div class="slider-container">
                  <input type="range" id="setting-letterSpacing" min="0" max="0.1" step="0.01" value="${this.settings.letterSpacing}" class="settings-slider">
                  <span class="slider-value" id="letterSpacing-value">${(this.settings.letterSpacing * 100).toFixed(0)}%</span>
                </div>
              </div>

              <!-- Marges -->
              <div class="settings-group">
                <label for="setting-marginWidth">📐 Largeur contenu</label>
                <div class="slider-container">
                  <input type="range" id="setting-marginWidth" min="1" max="4" step="0.5" value="${this.settings.marginWidth}" class="settings-slider">
                  <span class="slider-value" id="marginWidth-value">${this.settings.marginWidth}em</span>
                </div>
              </div>

              <!-- Thèmes prédéfinis -->
              <div class="settings-group">
                <label>🎨 Thèmes rapides</label>
                <div class="theme-quick-buttons">
                  <button class="quick-theme-btn" data-theme="warm" title="Chaud">☀️</button>
                  <button class="quick-theme-btn" data-theme="cool" title="Froid">❄️</button>
                  <button class="quick-theme-btn" data-theme="dark" title="Sombre">🌙</button>
                  <button class="quick-theme-btn" data-theme="sepia" title="Sépia">📖</button>
                  <button class="quick-theme-btn" data-theme="hc" title="Contraste">⚫</button>
                </div>
              </div>

              <!-- Options avancées -->
              <div class="settings-group">
                <label class="toggle-label">
                  <input type="checkbox" id="setting-focusMode" class="toggle-input" ${this.settings.focusMode ? 'checked' : ''}>
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Mode focus</span>
                </label>
              </div>

              <div class="settings-group">
                <label class="toggle-label">
                  <input type="checkbox" id="setting-reduceAnimations" class="toggle-input" ${this.settings.reduceAnimations ? 'checked' : ''}>
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Réduire animations</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="settings-modal-footer">
          <button class="btn-reset">↺ Réinitialiser</button>
          <button class="btn-close">Fermer</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);
  }

  attachListeners() {
    // Bouton config
    document.getElementById('user-config-btn')?.addEventListener('click', () => this.openModal());

    // Close buttons
    document.querySelector('.settings-close-btn')?.addEventListener('click', () => this.closeModal());
    document.querySelector('.btn-close')?.addEventListener('click', () => this.closeModal());
    document.querySelector('.settings-modal-overlay')?.addEventListener('click', () => this.closeModal());

    // Onglets
    document.querySelectorAll('.settings-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
    });

    // Dark Mode (Theme)
    document.querySelectorAll('input[name="theme"]').forEach(radio => {
      radio.addEventListener('change', (e) => {
        this.settings.theme = e.target.value;
        this.applyTheme();
        this.save();
      });
    });

    // Reader Toggle
    document.getElementById('reader-toggle')?.addEventListener('change', (e) => {
      this.settings.readerEnabled = e.target.checked;
      this.applyReaderMode();
      this.save();
    });

    // Luminosité
    document.getElementById('setting-luminosity')?.addEventListener('input', (e) => {
      this.settings.luminosity = parseInt(e.target.value);
      document.getElementById('luminosity-value').textContent = e.target.value + '%';
      this.applyReaderMode();
      this.save();
    });

    // Taille police
    document.getElementById('setting-fontSize')?.addEventListener('input', (e) => {
      this.settings.fontSize = parseInt(e.target.value);
      document.getElementById('fontSize-value').textContent = e.target.value + '%';
      this.applyReaderMode();
      this.save();
    });

    // Police
    document.getElementById('setting-fontFamily')?.addEventListener('change', (e) => {
      this.settings.fontFamily = e.target.value;
      this.applyReaderMode();
      this.save();
    });

    // Interligne
    document.getElementById('setting-lineHeight')?.addEventListener('input', (e) => {
      this.settings.lineHeight = parseFloat(e.target.value);
      document.getElementById('lineHeight-value').textContent = parseFloat(e.target.value).toFixed(1);
      this.applyReaderMode();
      this.save();
    });

    // Espacement
    document.getElementById('setting-letterSpacing')?.addEventListener('input', (e) => {
      this.settings.letterSpacing = parseFloat(e.target.value);
      document.getElementById('letterSpacing-value').textContent = (parseFloat(e.target.value) * 100).toFixed(0) + '%';
      this.applyReaderMode();
      this.save();
    });

    // Marges
    document.getElementById('setting-marginWidth')?.addEventListener('input', (e) => {
      this.settings.marginWidth = parseFloat(e.target.value);
      document.getElementById('marginWidth-value').textContent = parseFloat(e.target.value).toFixed(1) + 'em';
      this.applyReaderMode();
      this.save();
    });

    // Thèmes rapides
    document.querySelectorAll('.quick-theme-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.applyQuickTheme(e.target.dataset.theme);
      });
    });

    // Focus mode
    document.getElementById('setting-focusMode')?.addEventListener('change', (e) => {
      this.settings.focusMode = e.target.checked;
      this.applyReaderMode();
      this.save();
    });

    // Reduce animations
    document.getElementById('setting-reduceAnimations')?.addEventListener('change', (e) => {
      this.settings.reduceAnimations = e.target.checked;
      this.applyReaderMode();
      this.save();
    });

    // Réinitialiser
    document.querySelector('.btn-reset')?.addEventListener('click', () => this.reset());
  }

  switchTab(tabName) {
    // Désactiver tous les onglets
    document.querySelectorAll('.settings-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.settings-tab-content').forEach(content => content.classList.remove('active'));

    // Activer l'onglet sélectionné
    document.querySelector(`[data-tab="${tabName}"].settings-tab-btn`)?.classList.add('active');
    document.querySelector(`[data-tab="${tabName}"].settings-tab-content`)?.classList.add('active');
  }

  applyTheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = this.settings.theme === 'dark' || (this.settings.theme === 'auto' && prefersDark);

    if (isDark) {
      document.documentElement.classList.add('dark');
      document.body.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
      document.body.classList.remove('dark');
    }

    localStorage.setItem('theme', this.settings.theme);
    console.log('🌓 Thème appliqué:', this.settings.theme);
  }

  applyReaderMode() {
    const html = document.documentElement;
    const body = document.body;
    
    if (!this.settings.readerEnabled) {
      html.classList.remove('reader-mode');
      body.classList.remove('reader-mode');
      const oldStyle = document.getElementById('reader-style');
      if (oldStyle) oldStyle.remove();
      return;
    }

    html.classList.add('reader-mode');
    body.classList.add('reader-mode');

    let styleEl = document.getElementById('reader-style');
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = 'reader-style';
      document.head.appendChild(styleEl);
    }

    let fontFamily = 'inherit';
    const fontMap = {
      serif: 'Georgia, "Times New Roman", serif',
      'sans-serif': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      mono: '"Courier New", monospace',
      georgia: 'Georgia, serif',
      verdana: 'Verdana, sans-serif'
    };
    fontFamily = fontMap[this.settings.fontFamily] || 'inherit';

    let css = `
      html.reader-mode {
        font-size: calc(16px * ${this.settings.fontSize / 100}) !important;
      }

      body.reader-mode {
        background-color: ${this.settings.backgroundColor} !important;
        color: ${this.settings.textColor} !important;
        font-family: ${fontFamily} !important;
        line-height: ${this.settings.lineHeight} !important;
        letter-spacing: ${this.settings.letterSpacing}em !important;
      }

      body.reader-mode * {
        font-family: ${fontFamily} !important;
        line-height: ${this.settings.lineHeight} !important;
        letter-spacing: ${this.settings.letterSpacing}em !important;
      }

      body.reader-mode .sidebar {
        display: none !important;
      }

      body.reader-mode .main-content {
        max-width: ${this.settings.marginWidth * 20}em !important;
        margin: 0 auto !important;
        padding: 2rem ${this.settings.marginWidth}em !important;
      }

      body.reader-mode article {
        max-width: 100% !important;
        padding: 0 !important;
      }

      body.reader-mode .article-detail,
      body.reader-mode .media-detail {
        max-width: 100% !important;
        padding: 0 !important;
      }

      ${this.settings.reduceAnimations ? `
        body.reader-mode * {
          animation: none !important;
          transition: none !important;
        }
      ` : ''}

      ${this.settings.focusMode ? `
        body.reader-mode p {
          opacity: 0.5;
          transition: opacity 0.2s;
        }
        body.reader-mode p:hover {
          opacity: 1;
          background: rgba(255, 255, 0, 0.15);
          padding: 0.5em;
        }
      ` : ''}
    `;

    styleEl.textContent = css;
  }

  applyQuickTheme(theme) {
    const themes = {
      warm: { bg: '#f5f1e8', text: '#2c2c2c', lum: 100 },
      cool: { bg: '#e8f4f8', text: '#1a1a2e', lum: 100 },
      dark: { bg: '#1a1a1a', text: '#e0e0e0', lum: 100 },
      sepia: { bg: '#fef9e7', text: '#5c4033', lum: 95 },
      hc: { bg: '#ffffff', text: '#000000', lum: 120 }
    };

    const t = themes[theme];
    if (t) {
      this.settings.backgroundColor = t.bg;
      this.settings.textColor = t.text;
      this.settings.luminosity = t.lum;
      this.applyReaderMode();
      document.getElementById('setting-luminosity').value = t.lum;
      document.getElementById('luminosity-value').textContent = t.lum + '%';
      this.save();
    }
  }

  openModal() {
    const modal = document.getElementById('user-settings-modal');
    if (modal) {
      modal.classList.add('active');
      this.modalOpen = true;
    }
  }

  closeModal() {
    const modal = document.getElementById('user-settings-modal');
    if (modal) {
      modal.classList.remove('active');
      this.modalOpen = false;
    }
  }

  reset() {
    this.settings = {
      theme: 'auto',
      readerEnabled: false,
      luminosity: 100,
      fontFamily: 'system',
      fontSize: 100,
      lineHeight: 1.6,
      letterSpacing: 0,
      marginWidth: 2,
      backgroundColor: '#f5f1e8',
      textColor: '#2c2c2c',
      focusMode: false,
      reduceAnimations: true
    };

    this.save();
    this.applyTheme();
    this.applyReaderMode();
    this.createModal();
    this.attachListeners();
    console.log('↺ Paramètres réinitialisés');
  }

  save() {
    localStorage.setItem('theme', this.settings.theme);
    localStorage.setItem('readerEnabled', this.settings.readerEnabled);
    localStorage.setItem('luminosity', this.settings.luminosity);
    localStorage.setItem('fontFamily', this.settings.fontFamily);
    localStorage.setItem('fontSize', this.settings.fontSize);
    localStorage.setItem('lineHeight', this.settings.lineHeight);
    localStorage.setItem('letterSpacing', this.settings.letterSpacing);
    localStorage.setItem('marginWidth', this.settings.marginWidth);
    localStorage.setItem('backgroundColor', this.settings.backgroundColor);
    localStorage.setItem('textColor', this.settings.textColor);
    localStorage.setItem('focusMode', this.settings.focusMode);
    localStorage.setItem('reduceAnimations', this.settings.reduceAnimations);
  }
}

// Initialiser au chargement
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.UserSettings = new UserSettings();
    
    // Ajouter l'event listener pour le bouton tutoriel
    document.getElementById('tutorial-btn')?.addEventListener('click', () => {
      if (window.Onboarding) {
        window.Onboarding.start();
      }
    });
    
    // Ajouter l'event listener pour le bouton settings (la topbar)
    document.getElementById('settings-btn')?.addEventListener('click', () => {
      if (window.UserSettings) {
        window.UserSettings.openModal();
      }
    });
  });
} else {
  window.UserSettings = new UserSettings();
  
  // Ajouter les event listeners
  document.getElementById('tutorial-btn')?.addEventListener('click', () => {
    if (window.Onboarding) {
      window.Onboarding.start();
    }
  });
  
  document.getElementById('settings-btn')?.addEventListener('click', () => {
    if (window.UserSettings) {
      window.UserSettings.openModal();
    }
  });
}
