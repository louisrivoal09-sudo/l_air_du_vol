/**
 * SYSTÈME DE MODE SOMBRE - L'AIR DU VOL
 * Gestion complète du thème sombre avec localStorage
 */

function initializeDarkMode() {
  // Récupérer la préférence sauvegardée ou la préférence système
  const savedTheme = localStorage.getItem('theme') || 'light';
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark = savedTheme === 'dark' || (savedTheme === 'auto' && prefersDark);
  
  // Appliquer le thème
  if (isDark) {
    document.body.classList.add('dark');
  }
  updateThemeButton();
  
  // Event listener pour le bouton de toggle
  const themeToggle = document.getElementById('toggle-theme');
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleDarkMode);
  } else {
    console.warn('Bouton toggle-theme non trouvé');
  }
  
  // Écouter les changements de préférence système
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (localStorage.getItem('theme') === 'auto') {
      e.matches ? document.body.classList.add('dark') : document.body.classList.remove('dark');
      updateThemeButton();
    }
  });
}

function toggleDarkMode() {
  console.log('toggleDarkMode appelé');
  const isDark = document.body.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  updateThemeButton();
  
  // Ajouter une animation de transition
  document.body.style.transition = 'background 0.3s ease, color 0.3s ease';
  setTimeout(() => {
    document.body.style.transition = '';
  }, 300);
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
  document.body.classList.remove('dark');
  localStorage.setItem('theme', 'light');
  updateThemeButton();
}

// Fonction pour forcer le mode sombre
function setDarkMode() {
  document.body.classList.add('dark');
  localStorage.setItem('theme', 'dark');
  updateThemeButton();
}

// Fonction pour définir le mode automatique (selon préférence système)
function setAutoMode() {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  prefersDark ? setDarkMode() : setLightMode();
  localStorage.setItem('theme', 'auto');
}

// Export pour utilisation dans d'autres scripts
window.ThemeManager = {
  toggle: toggleDarkMode,
  setLight: setLightMode,
  setDark: setDarkMode,
  setAuto: setAutoMode,
  isDark: () => document.body.classList.contains('dark')
};

// Initialiser le dark mode au chargement du DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeDarkMode);
} else {
  initializeDarkMode();
}
