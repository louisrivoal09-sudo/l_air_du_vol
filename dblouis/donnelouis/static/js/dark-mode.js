/**
 * SYSTÈME DE MODE SOMBRE - L'AIR DU VOL (CORRIGÉ)
 * Gestion complète du thème sombre avec localStorage
 */

let themeToggleButton = null;

function initializeDarkMode() {
  console.log('🌙 Initialisation du mode sombre...');
  
  // Récupérer la préférence sauvegardée ou la préférence système
  const savedTheme = localStorage.getItem('theme') || 'auto';
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark = savedTheme === 'dark' || (savedTheme === 'auto' && prefersDark);
  
  // Appliquer le thème sur html et body
  if (isDark) {
    document.documentElement.classList.add('dark');
    document.body.classList.add('dark');
    console.log('✅ Mode sombre activé');
  } else {
    document.documentElement.classList.remove('dark');
    document.body.classList.remove('dark');
    console.log('☀️ Mode clair activé');
  }
  
  updateThemeButton();
  
  // Attacher le listener au bouton
  attachThemeToggleListener();
  
  // Écouter les changements de préférence système
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (localStorage.getItem('theme') === 'auto') {
      e.matches ? applyDarkMode() : applyLightMode();
      console.log('🔄 Changement de préférence système détecté');
    }
  });
}

function attachThemeToggleListener() {
  // Chercher le bouton avec plusieurs tentatives
  const themeToggle = document.getElementById('toggle-theme');
  
  if (themeToggle) {
    themeToggleButton = themeToggle;
    // Supprimer les anciens listeners pour éviter les doublons
    themeToggle.onclick = null;
    themeToggle.removeEventListener('click', toggleDarkMode);
    
    // Ajouter le nouveau listener
    themeToggle.addEventListener('click', toggleDarkMode, false);
    console.log('✅ Bouton toggle trouvé et écouteur attaché');
  } else {
    console.warn('⚠️ Bouton toggle-theme non trouvé - réessai dans 500ms');
    setTimeout(attachThemeToggleListener, 500);
  }
}

function toggleDarkMode(e) {
  e.preventDefault();
  e.stopPropagation();
  console.log('🔄 toggleDarkMode appelé');
  
  // Toggle sur html et body
  const isDark = document.body.classList.contains('dark');
  
  if (isDark) {
    applyLightMode();
    localStorage.setItem('theme', 'light');
    console.log('☀️ Mode clair');
  } else {
    applyDarkMode();
    localStorage.setItem('theme', 'dark');
    console.log('🌙 Mode sombre');
  }
  
  updateThemeButton();
}

function applyDarkMode() {
  document.documentElement.classList.add('dark');
  document.body.classList.add('dark');
}

function applyLightMode() {
  document.documentElement.classList.remove('dark');
  document.body.classList.remove('dark');
}

function updateThemeButton() {
  const button = document.getElementById('toggle-theme');
  if (button) {
    const isDark = document.body.classList.contains('dark');
    const icon = button.querySelector('.theme-icon');
    const text = button.querySelector('.theme-text');
    
    if (isDark) {
      if (icon) icon.textContent = '☀️';
      if (text) text.textContent = 'Mode Clair';
    } else {
      if (icon) icon.textContent = '🌙';
      if (text) text.textContent = 'Mode Sombre';
    }
  }
}

// Fonction pour forcer le mode clair
function setLightMode() {
  document.documentElement.classList.remove('dark');
  document.body.classList.remove('dark');
  localStorage.setItem('theme', 'light');
  updateThemeButton();
  console.log('☀️ Mode clair forcé');
}

// Fonction pour forcer le mode sombre
function setDarkMode() {
  document.documentElement.classList.add('dark');
  document.body.classList.add('dark');
  localStorage.setItem('theme', 'dark');
  updateThemeButton();
  console.log('🌙 Mode sombre forcé');
}

// Fonction pour définir le mode automatique (selon préférence système)
function setAutoMode() {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  prefersDark ? setDarkMode() : setLightMode();
  localStorage.setItem('theme', 'auto');
  console.log('🔄 Mode automatique défini');
}

// Export pour utilisation dans d'autres scripts
window.ThemeManager = {
  toggle: toggleDarkMode,
  setLight: setLightMode,
  setDark: setDarkMode,
  setAuto: setAutoMode,
  isDark: () => document.body.classList.contains('dark'),
  isHtmlDark: () => document.documentElement.classList.contains('dark')
};

// Initialiser le dark mode au chargement du DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeDarkMode);
} else {
  initializeDarkMode();
}
