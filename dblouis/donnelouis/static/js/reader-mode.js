/**
 * SYSTÈME DE LISEUSE AVANCÉE - L'AIR DU VOL
 * Mode lecture optimisé avec luminosité, polices, tailles, interligne, etc.
 */

class ReaderMode {
  constructor() {
    this.isActive = false;
    this.settings = {
      luminosity: 100,           // 50-150%
      fontFamily: 'system',      // system, serif, sans-serif, mono
      fontSize: 100,             // 80-150%
      lineHeight: 1.6,           // 1.4-2.0
      letterSpacing: 0,          // 0-0.1em
      marginWidth: 2,            // 1-4 (em)
      backgroundColor: '#f5f1e8', // couleur fond
      textColor: '#2c2c2c',      // couleur texte
      focusMode: false,          // met en évidence la ligne en cours
      reduceAnimations: true     // réduit les animations
    };
    this.init();
  }

  init() {
    this.loadSettings();
    this.createUI();
    this.attachListeners();
    console.log('✅ Système de liseuse initialisé');
  }

  loadSettings() {
    const saved = localStorage.getItem('readerSettings');
    if (saved) {
      try {
        this.settings = { ...this.settings, ...JSON.parse(saved) };
        console.log('📚 Paramètres de liseuse restaurés');
      } catch (e) {
        console.error('Erreur lors du chargement des paramètres:', e);
      }
    }
  }

  saveSettings() {
    localStorage.setItem('readerSettings', JSON.stringify(this.settings));
  }

  createUI() {
    // Bouton d'activation dans la topbar
    const topbar = document.querySelector('.topbar');
    if (!topbar) return;

    // Créer le bouton
    const readerBtn = document.createElement('button');
    readerBtn.id = 'reader-mode-btn';
    readerBtn.className = 'reader-mode-btn';
    readerBtn.title = 'Ouvrir les paramètres de liseuse';
    readerBtn.innerHTML = '📖';
    readerBtn.style.cssText = `
      background: none;
      border: none;
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0.5rem;
      margin-right: 1rem;
      transition: all 0.3s ease;
      border-radius: 0.5rem;
    `;

    // Insérer avant le bouton toggle-theme
    const themeBtn = topbar.querySelector('#toggle-theme');
    if (themeBtn) {
      themeBtn.parentNode.insertBefore(readerBtn, themeBtn);
    } else {
      topbar.appendChild(readerBtn);
    }

    readerBtn.addEventListener('click', () => this.openPanel());

    // Créer le panneau de contrôle
    this.createPanel();
  }

  createPanel() {
    // Vérifier si le panneau existe déjà
    if (document.getElementById('reader-panel')) {
      return;
    }

    const panel = document.createElement('div');
    panel.id = 'reader-panel';
    panel.className = 'reader-panel';
    panel.innerHTML = `
      <div class="reader-panel-header">
        <h3>📖 Mode Liseuse</h3>
        <button class="reader-close-btn">✕</button>
      </div>

      <div class="reader-panel-content">
        <!-- Toggle du mode liseuse -->
        <div class="reader-setting">
          <label>
            <input type="checkbox" id="reader-toggle" class="reader-checkbox" ${this.isActive ? 'checked' : ''}>
            Activer le mode liseuse
          </label>
        </div>

        <!-- Luminosité -->
        <div class="reader-setting">
          <label for="luminosity">
            💡 Luminosité: <span id="luminosity-value">${this.settings.luminosity}%</span>
          </label>
          <input 
            type="range" 
            id="luminosity" 
            min="50" 
            max="150" 
            value="${this.settings.luminosity}"
            class="reader-slider"
          >
        </div>

        <!-- Taille de police -->
        <div class="reader-setting">
          <label for="fontSize">
            🔤 Taille du texte: <span id="fontSize-value">${this.settings.fontSize}%</span>
          </label>
          <input 
            type="range" 
            id="fontSize" 
            min="80" 
            max="150" 
            value="${this.settings.fontSize}"
            class="reader-slider"
          >
        </div>

        <!-- Police -->
        <div class="reader-setting">
          <label for="fontFamily">
            ✍️ Police
          </label>
          <select id="fontFamily" class="reader-select">
            <option value="system" ${this.settings.fontFamily === 'system' ? 'selected' : ''}>Système</option>
            <option value="serif" ${this.settings.fontFamily === 'serif' ? 'selected' : ''}>Serif (Classique)</option>
            <option value="sans-serif" ${this.settings.fontFamily === 'sans-serif' ? 'selected' : ''}>Sans-serif (Moderne)</option>
            <option value="mono" ${this.settings.fontFamily === 'mono' ? 'selected' : ''}>Monospace (Code)</option>
            <option value="georgia" ${this.settings.fontFamily === 'georgia' ? 'selected' : ''}>Georgia</option>
            <option value="verdana" ${this.settings.fontFamily === 'verdana' ? 'selected' : ''}>Verdana</option>
          </select>
        </div>

        <!-- Interligne -->
        <div class="reader-setting">
          <label for="lineHeight">
            📏 Interligne: <span id="lineHeight-value">${this.settings.lineHeight}</span>
          </label>
          <input 
            type="range" 
            id="lineHeight" 
            min="1.4" 
            max="2.0" 
            step="0.1"
            value="${this.settings.lineHeight}"
            class="reader-slider"
          >
        </div>

        <!-- Espacement lettres -->
        <div class="reader-setting">
          <label for="letterSpacing">
            ⎸ Espacement: <span id="letterSpacing-value">${(this.settings.letterSpacing * 100).toFixed(0)}%</span>
          </label>
          <input 
            type="range" 
            id="letterSpacing" 
            min="0" 
            max="0.1" 
            step="0.01"
            value="${this.settings.letterSpacing}"
            class="reader-slider"
          >
        </div>

        <!-- Marges -->
        <div class="reader-setting">
          <label for="marginWidth">
            📐 Largeur contenu: <span id="marginWidth-value">${this.settings.marginWidth}em</span>
          </label>
          <input 
            type="range" 
            id="marginWidth" 
            min="1" 
            max="4" 
            step="0.5"
            value="${this.settings.marginWidth}"
            class="reader-slider"
          >
        </div>

        <!-- Thèmes prédéfinis -->
        <div class="reader-setting">
          <label>🎨 Thèmes</label>
          <div class="reader-themes">
            <button class="reader-theme-btn" data-theme="warm" title="Chaud">☀️</button>
            <button class="reader-theme-btn" data-theme="cool" title="Froid">❄️</button>
            <button class="reader-theme-btn" data-theme="dark" title="Sombre">🌙</button>
            <button class="reader-theme-btn" data-theme="sepia" title="Sépia">📖</button>
            <button class="reader-theme-btn" data-theme="hc" title="Contraste">⚫</button>
          </div>
        </div>

        <!-- Options avancées -->
        <div class="reader-setting">
          <label>
            <input type="checkbox" id="focus-mode" class="reader-checkbox" ${this.settings.focusMode ? 'checked' : ''}>
            Mode focus (surligner la ligne en cours)
          </label>
        </div>

        <div class="reader-setting">
          <label>
            <input type="checkbox" id="reduce-animations" class="reader-checkbox" ${this.settings.reduceAnimations ? 'checked' : ''}>
            Réduire les animations
          </label>
        </div>

        <!-- Boutons d'action -->
        <div class="reader-actions">
          <button class="reader-reset-btn">↺ Réinitialiser</button>
        </div>
      </div>
    `;

    document.body.appendChild(panel);

    // Attacher les événements
    this.attachPanelListeners();
  }

  attachListeners() {
    const btn = document.getElementById('reader-mode-btn');
    if (btn) {
      btn.addEventListener('click', () => this.openPanel());
    }
  }

  attachPanelListeners() {
    // Fermer le panneau
    const closeBtn = document.querySelector('.reader-close-btn');
    closeBtn?.addEventListener('click', () => this.closePanel());

    // Toggle du mode liseuse
    const toggle = document.getElementById('reader-toggle');
    toggle?.addEventListener('change', (e) => {
      this.toggleReaderMode(e.target.checked);
    });

    // Luminosité
    const luminosity = document.getElementById('luminosity');
    luminosity?.addEventListener('input', (e) => {
      this.settings.luminosity = parseInt(e.target.value);
      document.getElementById('luminosity-value').textContent = e.target.value + '%';
      this.applySettings();
      this.saveSettings();
    });

    // Taille police
    const fontSize = document.getElementById('fontSize');
    fontSize?.addEventListener('input', (e) => {
      this.settings.fontSize = parseInt(e.target.value);
      document.getElementById('fontSize-value').textContent = e.target.value + '%';
      this.applySettings();
      this.saveSettings();
    });

    // Police
    const fontFamily = document.getElementById('fontFamily');
    fontFamily?.addEventListener('change', (e) => {
      this.settings.fontFamily = e.target.value;
      this.applySettings();
      this.saveSettings();
    });

    // Interligne
    const lineHeight = document.getElementById('lineHeight');
    lineHeight?.addEventListener('input', (e) => {
      this.settings.lineHeight = parseFloat(e.target.value);
      document.getElementById('lineHeight-value').textContent = parseFloat(e.target.value).toFixed(1);
      this.applySettings();
      this.saveSettings();
    });

    // Espacement lettres
    const letterSpacing = document.getElementById('letterSpacing');
    letterSpacing?.addEventListener('input', (e) => {
      this.settings.letterSpacing = parseFloat(e.target.value);
      document.getElementById('letterSpacing-value').textContent = (parseFloat(e.target.value) * 100).toFixed(0) + '%';
      this.applySettings();
      this.saveSettings();
    });

    // Marges
    const marginWidth = document.getElementById('marginWidth');
    marginWidth?.addEventListener('input', (e) => {
      this.settings.marginWidth = parseFloat(e.target.value);
      document.getElementById('marginWidth-value').textContent = parseFloat(e.target.value).toFixed(1) + 'em';
      this.applySettings();
      this.saveSettings();
    });

    // Focus mode
    const focusMode = document.getElementById('focus-mode');
    focusMode?.addEventListener('change', (e) => {
      this.settings.focusMode = e.target.checked;
      if (e.target.checked) {
        this.enableFocusMode();
      } else {
        this.disableFocusMode();
      }
      this.saveSettings();
    });

    // Reduce animations
    const reduceAnimations = document.getElementById('reduce-animations');
    reduceAnimations?.addEventListener('change', (e) => {
      this.settings.reduceAnimations = e.target.checked;
      this.applySettings();
      this.saveSettings();
    });

    // Thèmes prédéfinis
    document.querySelectorAll('.reader-theme-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const theme = e.target.dataset.theme;
        this.applyTheme(theme);
        // Mettre à jour l'affichage
        document.querySelectorAll('.reader-theme-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
      });
    });

    // Réinitialiser
    const resetBtn = document.querySelector('.reader-reset-btn');
    resetBtn?.addEventListener('click', () => {
      this.resetSettings();
    });
  }

  toggleReaderMode(enabled) {
    this.isActive = enabled;
    if (enabled) {
      document.documentElement.classList.add('reader-mode');
      document.body.classList.add('reader-mode');
      this.applySettings();
      console.log('📖 Mode liseuse activé');
    } else {
      document.documentElement.classList.remove('reader-mode');
      document.body.classList.remove('reader-mode');
      this.disableFocusMode();
      console.log('📖 Mode liseuse désactivé');
    }
    this.saveSettings();
  }

  applySettings() {
    if (!this.isActive) return;

    const root = document.documentElement;
    const style = document.getElementById('reader-mode-style') || document.createElement('style');
    style.id = 'reader-mode-style';

    let fontFamilyValue = 'inherit';
    switch (this.settings.fontFamily) {
      case 'serif':
        fontFamilyValue = 'Georgia, "Times New Roman", serif';
        break;
      case 'sans-serif':
        fontFamilyValue = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
        break;
      case 'mono':
        fontFamilyValue = '"Courier New", monospace';
        break;
      case 'georgia':
        fontFamilyValue = 'Georgia, serif';
        break;
      case 'verdana':
        fontFamilyValue = 'Verdana, sans-serif';
        break;
    }

    style.textContent = `
      html.reader-mode {
        font-size: calc(16px * ${this.settings.fontSize / 100});
      }

      body.reader-mode,
      body.reader-mode * {
        font-family: ${fontFamilyValue};
        line-height: ${this.settings.lineHeight};
        letter-spacing: ${this.settings.letterSpacing}em;
      }

      body.reader-mode {
        background-color: ${this.settings.backgroundColor};
        color: ${this.settings.textColor};
        filter: brightness(${this.settings.luminosity / 100});
      }

      body.reader-mode .main-content,
      body.reader-mode article,
      body.reader-mode .article-detail,
      body.reader-mode .media-detail {
        max-width: ${this.settings.marginWidth * 20}em;
        margin-left: auto;
        margin-right: auto;
        padding: 2rem ${this.settings.marginWidth}em;
      }

      body.reader-mode .sidebar {
        display: none;
      }

      body.reader-mode .topbar {
        position: sticky;
        top: 0;
        z-index: 1000;
        background-color: ${this.settings.backgroundColor};
        border-bottom: 2px solid rgba(0, 0, 0, 0.1);
      }

      body.reader-mode .footer {
        display: none;
      }

      ${this.settings.reduceAnimations ? `
        body.reader-mode * {
          animation: none !important;
          transition: none !important;
        }
      ` : ''}

      body.reader-mode p {
        margin: 1.5em 0;
      }

      body.reader-mode h1, body.reader-mode h2, body.reader-mode h3,
      body.reader-mode h4, body.reader-mode h5, body.reader-mode h6 {
        margin: 1.5em 0 0.5em;
        line-height: ${this.settings.lineHeight * 0.9};
      }

      body.reader-mode img {
        max-width: 100%;
        height: auto;
        margin: 1em 0;
      }

      body.reader-mode code, body.reader-mode pre {
        background-color: rgba(0, 0, 0, 0.05);
        padding: 0.2em 0.4em;
        border-radius: 0.3em;
      }

      body.reader-mode blockquote {
        border-left: 4px solid rgba(0, 0, 0, 0.3);
        padding-left: ${this.settings.marginWidth}em;
        margin-left: 0;
        opacity: 0.8;
      }
    `;

    if (!document.getElementById('reader-mode-style')) {
      document.head.appendChild(style);
    }
  }

  applyTheme(theme) {
    const themes = {
      warm: {
        backgroundColor: '#f5f1e8',
        textColor: '#2c2c2c',
        luminosity: 100
      },
      cool: {
        backgroundColor: '#e8f4f8',
        textColor: '#1a1a2e',
        luminosity: 100
      },
      dark: {
        backgroundColor: '#1a1a1a',
        textColor: '#e0e0e0',
        luminosity: 100
      },
      sepia: {
        backgroundColor: '#fef9e7',
        textColor: '#5c4033',
        luminosity: 95
      },
      hc: {
        backgroundColor: '#ffffff',
        textColor: '#000000',
        luminosity: 120
      }
    };

    const selectedTheme = themes[theme];
    if (selectedTheme) {
      this.settings = { ...this.settings, ...selectedTheme };
      this.applySettings();
      this.saveSettings();
      
      // Mettre à jour les sliders
      document.getElementById('luminosity').value = this.settings.luminosity;
      document.getElementById('luminosity-value').textContent = this.settings.luminosity + '%';
    }
  }

  enableFocusMode() {
    const style = document.getElementById('focus-mode-style') || document.createElement('style');
    style.id = 'focus-mode-style';
    style.textContent = `
      body.reader-mode.focus-mode p {
        opacity: 0.4;
        transition: opacity 0.3s ease;
      }

      body.reader-mode.focus-mode p:hover {
        opacity: 1;
        background-color: rgba(255, 255, 0, 0.1);
        padding: 0.5em;
        margin: 0.5em 0;
      }
    `;

    if (!document.getElementById('focus-mode-style')) {
      document.head.appendChild(style);
    }

    document.body.classList.add('focus-mode');
  }

  disableFocusMode() {
    document.body.classList.remove('focus-mode');
  }

  openPanel() {
    const panel = document.getElementById('reader-panel');
    if (panel) {
      panel.classList.add('active');
      // Mettre à jour le statut du toggle
      document.getElementById('reader-toggle').checked = this.isActive;
    }
  }

  closePanel() {
    const panel = document.getElementById('reader-panel');
    if (panel) {
      panel.classList.remove('active');
    }
  }

  resetSettings() {
    this.settings = {
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

    this.saveSettings();
    this.applySettings();

    // Réinitialiser l'UI
    document.getElementById('luminosity').value = 100;
    document.getElementById('fontSize').value = 100;
    document.getElementById('fontFamily').value = 'system';
    document.getElementById('lineHeight').value = 1.6;
    document.getElementById('letterSpacing').value = 0;
    document.getElementById('marginWidth').value = 2;
    document.getElementById('focus-mode').checked = false;
    document.getElementById('reduce-animations').checked = true;

    document.getElementById('luminosity-value').textContent = '100%';
    document.getElementById('fontSize-value').textContent = '100%';
    document.getElementById('lineHeight-value').textContent = '1.6';
    document.getElementById('letterSpacing-value').textContent = '0%';
    document.getElementById('marginWidth-value').textContent = '2.0em';

    console.log('↺ Paramètres réinitialisés');
  }
}

// Initialiser au chargement du DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.ReaderMode = new ReaderMode();
  });
} else {
  window.ReaderMode = new ReaderMode();
}
