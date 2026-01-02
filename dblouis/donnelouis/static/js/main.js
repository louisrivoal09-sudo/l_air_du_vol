    /* =====================================================
   L'AIR DU VOL - SCRIPT FUSIONNÉ (TOUT-EN-UN)
   - Filtrage / recherche / tri / vues
   - Read more (affichage article complet)
   - Lightbox image gallery
   - Progression de lecture
   - Table des matières flottante
   - Téléchargement PDF (print window)
   - Partage (Web Share + fallback)
   - Animations, observers, raccourcis clavier
   ===================================================== */

(function () {
  'use strict';

  // ---------------------------
  // Helpers & safe DOM getters
  // ---------------------------
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const elOrNull = (id) => document.getElementById(id) || null;
  const safeText = (node) => (node ? node.textContent.trim() : '');

  // ---------------------------
  // STATE
  // ---------------------------
  let state = {
    currentCategory: 'all',
    currentSort: 'recent',
    currentView: 'grid',
    searchQuery: '',
  };

  // ---------------------------
  // DOM ELEMENTS (some may be missing — we guard)
  // ---------------------------
  const searchInput = elOrNull('search-input');
  const searchClear = elOrNull('search-clear');
  const categoryBtns = $$('.category-btn');
  const sortBtns = $$('.sort-btn');
  const viewToggles = $$('.view-toggle');
  const articlesGrid = elOrNull('articles-grid');
  const resultsCount = elOrNull('results-count');
  const noResults = elOrNull('no-results');
  const resetFiltersBtn = elOrNull('reset-filters');
  const fullArticle = elOrNull('full-article');
  const toggleThemeBtn = elOrNull('toggle-theme');
  const sidebarToggleBtn = elOrNull('toggle-sidebar');
  const sidebar = document.querySelector('.sidebar');
  const body = document.body;

  // Utility: always get up-to-date list of article cards (DOM might change)
  function getArticleCards() {
    return $$('.article-card').filter(c => !c.classList.contains('ad-only-hidden'));
  }

  // ---------------------------
  // FILTER / SEARCH / SORT
  // ---------------------------
  function filterAndSearchArticles() {
    const cards = getArticleCards();
    let visibleCount = 0;
    const q = state.searchQuery.toLowerCase();

    cards.forEach(card => {
      // keep ad cards visible by default (but check class)
      if (card.classList.contains('ad-card')) {
        card.classList.remove('hidden');
        visibleCount++;
        return;
      }

      const category = (card.dataset.category || '').toLowerCase();
      const title = (card.dataset.title || card.querySelector('h3')?.textContent || '').toLowerCase();
      const description = (card.querySelector('p')?.textContent || '').toLowerCase();
      const dateText = (card.dataset.date || card.querySelector('.date')?.textContent || '').toLowerCase();

      const matchCategory = state.currentCategory === 'all' || category === state.currentCategory;
      const matchSearch = !q || title.includes(q) || description.includes(q) || dateText.includes(q);

      if (matchCategory && matchSearch) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    // update UI
    if (resultsCount) {
      resultsCount.textContent = `${visibleCount} article${visibleCount > 1 ? 's' : ''} trouvé${visibleCount > 1 ? 's' : ''}`;
    }

    if (articlesGrid) {
      if (visibleCount === 0) {
        if (noResults) noResults.classList.add('show');
        articlesGrid.style.display = 'none';
      } else {
        if (noResults) noResults.classList.remove('show');
        articlesGrid.style.display = '';
        sortArticles(); // re-sort visible cards after filtering
      }
    }
  }

  function sortArticles() {
    if (!articlesGrid) return;
    const cards = getArticleCards().filter(card => !card.classList.contains('hidden') && !card.classList.contains('ad-card'));
    if (cards.length === 0) return;

    cards.sort((a, b) => {
      const adate = a.dataset.date ? new Date(a.dataset.date) : new Date(safeText(a.querySelector('.date')) || 0);
      const bdate = b.dataset.date ? new Date(b.dataset.date) : new Date(safeText(b.querySelector('.date')) || 0);
      switch (state.currentSort) {
        case 'recent':
          return bdate - adate;
        case 'old':
          return adate - bdate;
        case 'title':
          return (a.dataset.title || safeText(a.querySelector('h3'))).localeCompare(b.dataset.title || safeText(b.querySelector('h3')));
        default:
          return 0;
      }
    });

    // append in order (moves nodes in DOM)
    cards.forEach(card => articlesGrid.appendChild(card));
  }

  function changeView(view) {
    if (!articlesGrid) return;
    state.currentView = view;
    articlesGrid.classList.remove('list-view', 'compact-view', 'grid-view');
    articlesGrid.classList.add(view === 'list' ? 'list-view' : (view === 'compact' ? 'compact-view' : 'grid-view'));
    // store optional preference
    try { localStorage.setItem('articles_view', view); } catch (e) {}
  }

  // ---------------------------
  // READ MORE (delegated)
  // ---------------------------
  function initReadMore() {
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.read-more');
      if (!btn) return;
      e.preventDefault();

      const articleId = btn.dataset.articleId;
      const template = articleId ? elOrNull(`article-${articleId}`) : null;
      const card = btn.closest('.article-card');
      const title = safeText(card?.querySelector('h3'));
      const date = safeText(card?.querySelector('.date')) || (card?.dataset.date || '');

      if (!template || !fullArticle) {
        // ⚠️ DÉSACTIVÉ : On utilise maintenant des vraies pages détails avec onclick
        // alert('Article non disponible');
        return;
      }

      fullArticle.innerHTML = `
  <div class="card" style="max-width: 1200px; margin: 0 auto;">
    <div class="card-content" style="padding: 3rem;">

      <h1>${title}</h1>
      <p class="preview-date">${date}</p>

      <!-- 🔥 ICI : Boutons d’action -->
      <div class="article-actions">
        <button class="download-article-btn" onclick="downloadArticleAsPDF()">📄 Télécharger en PDF</button>
        <button class="share-article-btn" onclick="shareArticle()">📤 Partager</button>
      </div>

      <div id="article-content">${template.innerHTML}</div>

      <button id="close-article" class="btn" style="margin-top: 3rem; background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);">
        ← Retour aux articles
      </button>
    </div>
  </div>
`;

      // hide main areas
      document.querySelectorAll('.filters-section, .articles-hero').forEach(el => el.style.display = 'none');
      if (articlesGrid) articlesGrid.style.display = 'none';
      if (noResults) noResults.style.display = 'none';
      fullArticle.style.display = 'block';
      window.scrollTo({ top: 0, behavior: 'smooth' });

      // attach close handler
      const closeBtn = elOrNull('close-article');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          fullArticle.style.display = 'none';
          document.querySelectorAll('.filters-section, .articles-hero').forEach(el => el.style.display = '');
          if (articlesGrid) articlesGrid.style.display = '';
          filterAndSearchArticles();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }, { once: true });
      }
    });
  }

  // ---------------------------
  // THEME & SIDEBAR
  // ---------------------------
  function initThemeAndSidebar() {
    if (toggleThemeBtn) {
      try {
        if (localStorage.getItem('theme') === 'dark') {
          body.classList.add('dark');
          toggleThemeBtn.textContent = '☀️ Mode Clair';
        }
      } catch (e) {}

      toggleThemeBtn.addEventListener('click', () => {
        body.classList.toggle('dark');
        const isDark = body.classList.contains('dark');
        toggleThemeBtn.textContent = isDark ? '☀️ Mode Clair' : '🌙 Mode Sombre';
        try { localStorage.setItem('theme', isDark ? 'dark' : 'light'); } catch (e) {}
      });
    }

    if (sidebarToggleBtn && sidebar) {
      sidebarToggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        body.classList.toggle('menu-collapsed');
      });
    }
  }

  // ---------------------------
  // LIGHTBOX (class)
  // ---------------------------
  class ImageLightbox {
    constructor() {
      this.currentIndex = 0;
      this.images = [];
      this.lightboxEl = null;
      this.init();
    }

    init() {
      // build markup
      const lightboxHTML = `
        <div class="lightbox" id="lightbox" aria-hidden="true">
          <div class="lightbox-toolbar">
            <button class="lightbox-btn lightbox-download" id="lightbox-download" title="Télécharger">📥</button>
            <button class="lightbox-btn lightbox-close" id="lightbox-close" title="Fermer">×</button>
          </div>
          <button class="lightbox-nav lightbox-prev" id="lightbox-prev" aria-label="Précédent">❮</button>
          <div class="lightbox-content"><img id="lightbox-img" src="" alt=""></div>
          <button class="lightbox-nav lightbox-next" id="lightbox-next" aria-label="Suivant">❯</button>
          <div class="lightbox-caption">
            <div id="lightbox-caption-text"></div>
            <div class="lightbox-counter" id="lightbox-counter"></div>
          </div>
        </div>
      `;
      document.body.insertAdjacentHTML('beforeend', lightboxHTML);
      this.lightboxEl = elOrNull('lightbox');

      // setup images and listeners
      this.setupGalleryImages();
      this.bindEvents();
    }

    setupGalleryImages() {
      const galleryItems = $$('.gallery-item');
      this.images = [];
      galleryItems.forEach((item, index) => {
        const img = item.querySelector('img');
        if (!img) return;
        const caption = item.dataset.caption || img.alt || '';
        this.images.push({ src: img.src, caption });
        item.addEventListener('click', (e) => {
          e.preventDefault();
          this.open(index);
        });
      });
    }

    bindEvents() {
      const close = () => this.close();
      elOrNull('lightbox-close')?.addEventListener('click', close);
      elOrNull('lightbox-prev')?.addEventListener('click', () => this.prev());
      elOrNull('lightbox-next')?.addEventListener('click', () => this.next());
      elOrNull('lightbox-download')?.addEventListener('click', () => this.download());
      this.lightboxEl?.addEventListener('click', (e) => {
        if (e.target === this.lightboxEl) this.close();
      });

      document.addEventListener('keydown', (e) => {
        if (!this.lightboxEl?.classList.contains('show')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') this.prev();
        if (e.key === 'ArrowRight') this.next();
      });
    }

    open(index) {
      this.currentIndex = index;
      this.show();
    }

    show() {
      if (!this.lightboxEl) return;
      const imgEl = elOrNull('lightbox-img');
      const captionEl = elOrNull('lightbox-caption-text');
      const counterEl = elOrNull('lightbox-counter');
      const prevBtn = elOrNull('lightbox-prev');
      const nextBtn = elOrNull('lightbox-next');

      const current = this.images[this.currentIndex];
      if (!current) return;

      imgEl.src = current.src;
      captionEl.textContent = current.caption;
      counterEl.textContent = `${this.currentIndex + 1} / ${this.images.length}`;

      prevBtn.disabled = this.currentIndex === 0;
      nextBtn.disabled = this.currentIndex === this.images.length - 1;

      this.lightboxEl.classList.add('show');
      this.lightboxEl.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    close() {
      this.lightboxEl?.classList.remove('show');
      this.lightboxEl?.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    next() {
      if (this.currentIndex < this.images.length - 1) {
        this.currentIndex++;
        this.show();
      }
    }

    prev() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.show();
      }
    }

    download() {
      const current = this.images[this.currentIndex];
      if (!current) return;
      const link = document.createElement('a');
      link.href = current.src;
      link.download = `lairduvol-image-${this.currentIndex + 1}.jpg`;
      document.body.appendChild(link);
      link.click();
      link.remove();
    }
  }

  // ---------------------------
  // READING PROGRESS
  // ---------------------------
  function initReadingProgress() {
    const progressHTML = `
      <div class="reading-progress" aria-hidden="true">
        <div class="reading-progress-bar" id="reading-progress-bar"></div>
      </div>
    `;
    document.body.insertAdjacentHTML('afterbegin', progressHTML);
    window.addEventListener('scroll', updateReadingProgress);
  }

  function updateReadingProgress() {
    const progressBar = elOrNull('reading-progress-bar');
    if (!progressBar) return;
    const windowHeight = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight - windowHeight;
    const scrollTop = window.scrollY;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = `${Math.min(Math.max(progress, 0), 100)}%`;
  }

  // ---------------------------
  // TABLE OF CONTENTS FOR FULL ARTICLE
  // ---------------------------
  function initTableOfContents() {
    const article = document.querySelector('.full-article') || document.querySelector('.fullArticle') || fullArticle;
    if (!article) return;
    const headings = article.querySelectorAll('h2, h3');
    if (!headings || headings.length === 0) return;

    const tocHTML = `
      <div class="article-toc show" id="article-toc" aria-hidden="false">
        <h4>📑 Sommaire</h4>
        <ul id="toc-list"></ul>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', tocHTML);
    const tocList = elOrNull('toc-list');
    if (!tocList) return;

    headings.forEach((heading, index) => {
      if (!heading.id) heading.id = `heading-${index}`;
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `#${heading.id}`;
      a.textContent = heading.textContent;
      a.addEventListener('click', (e) => {
        e.preventDefault();
        heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      li.appendChild(a);
      tocList.appendChild(li);
    });

    window.addEventListener('scroll', () => updateActiveTocLink(headings));
  }

  function updateActiveTocLink(headings) {
    const tocLinks = $$('#toc-list a');
    if (!tocLinks.length) return;
    let activeIndex = 0;
    for (let i = 0; i < headings.length; i++) {
      if (headings[i].getBoundingClientRect().top < 200) activeIndex = i;
    }
    tocLinks.forEach((link, i) => link.classList.toggle('active', i === activeIndex));
  }

  // ---------------------------
  // DOWNLOAD ARTICLE AS PDF (print window)
  // ---------------------------
  function downloadArticleAsPDF() {
    const article = document.querySelector('.full-article') || fullArticle;
    if (!article) {
      alert('Aucun article à télécharger');
      return;
    }

    const clone = article.cloneNode(true);
    clone.querySelectorAll('.btn, button, .article-actions, .share-article-btn, .download-article-btn').forEach(el => el.remove());

    const printStyles = `
      <style>
        body { font-family: Arial, sans-serif; color: #222; margin: 30px; }
        h1 { color: #0A2463; font-size: 28px; }
        h2 { color: #0A2463; font-size: 22px; margin-top: 20px; }
        h3 { color: #4B5563; font-size: 18px; }
        p { line-height: 1.6; text-align: justify; }
        img { max-width: 100%; height: auto; }
      </style>
    `;

    const fullHTML = `
      <!doctype html>
      <html>
        <head>
          <meta charset="utf-8"/>
          <title>Article - L'Air du Vol</title>
          ${printStyles}
        </head>
        <body>
          <div style="text-align:center; margin-bottom: 30px;">
            <h1>L'Air du Vol®</h1>
            <p style="color:#666;">www.lairduvol.fr</p>
          </div>
          ${clone.innerHTML}
          <div style="margin-top:50px; padding-top:20px; border-top:2px solid #ddd; text-align:center; color:#666;">
            <p>Document généré par L'Air du Vol - ${new Date().toLocaleDateString('fr-FR')}</p>
          </div>
        </body>
      </html>
    `;

    const printWindow = window.open('', '', 'width=900,height=700');
    if (!printWindow) {
      alert('Impossible d\'ouvrir une nouvelle fenêtre pour l\'impression (pop-up bloquée).');
      return;
    }
    printWindow.document.write(fullHTML);
    printWindow.document.close();
    printWindow.onload = function () { printWindow.print(); };
  }

  // ---------------------------
  // SHARE ARTICLE
  // ---------------------------
  function shareArticle() {
    const title = document.querySelector('.full-article h1')?.textContent || document.title || 'Article - L\'Air du Vol';
    const url = window.location.href;
    const text = `Découvrez cet article passionnant sur L'Air du Vol : ${title}`;

    if (navigator.share) {
      navigator.share({ title, text, url }).catch(err => console.log('Erreur de partage:', err));
      return;
    }

    // fallback: copy to clipboard
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(() => showNotification('✓ Lien copié dans le presse-papiers !')).catch(() => showShareModal(title, url));
    } else {
      showShareModal(title, url);
    }
  }

  function showShareModal(title, url) {
    const modal = document.createElement('div');
    modal.className = 'share-modal';
    modal.style.cssText = `
      position: fixed; top:50%; left:50%; transform: translate(-50%,-50%);
      background: white; padding: 2rem; border-radius: .75rem; box-shadow: 0 20px 40px rgba(0,0,0,.2); z-index:10001; min-width:320px;
    `;
    const encodedUrl = encodeURIComponent(url);
    const encodedTitle = encodeURIComponent(title);
    modal.innerHTML = `
      <h3 style="margin-bottom:1rem; color:#0A2463;">Partager cet article</h3>
      <div style="display:flex; flex-direction:column; gap: .6rem;">
        <a href="https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}" target="_blank" style="padding:.8rem; text-align:center; border-radius:.5rem; text-decoration:none; background:#1877F2; color:white;">📘 Facebook</a>
        <a href="https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}" target="_blank" style="padding:.8rem; text-align:center; border-radius:.5rem; text-decoration:none; background:#1DA1F2; color:white;">🐦 Twitter</a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}" target="_blank" style="padding:.8rem; text-align:center; border-radius:.5rem; text-decoration:none; background:#0A66C2; color:white;">💼 LinkedIn</a>
        <button id="close-share-modal" style="padding:.7rem; border-radius:.5rem; background:#E5E7EB; border:none; cursor:pointer;">Fermer</button>
      </div>
    `;
    const overlay = document.createElement('div');
    overlay.className = 'share-overlay';
    overlay.style.cssText = `position:fixed; inset:0; background:rgba(0,0,0,.45); z-index:10000;`;
    overlay.addEventListener('click', () => { modal.remove(); overlay.remove(); });
    modal.querySelector('#close-share-modal')?.addEventListener('click', () => { modal.remove(); overlay.remove(); });

    document.body.appendChild(overlay);
    document.body.appendChild(modal);
  }

  function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'site-notification';
    notification.style.cssText = `
      position: fixed; bottom: 2rem; left:50%; transform: translateX(-50%);
      background: linear-gradient(135deg,#10B981 0%,#059669 100%); color:white; padding:1rem 1.6rem; border-radius:1rem;
      box-shadow:0 20px 30px rgba(0,0,0,0.15); z-index:10002;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  // ---------------------------
  // ADD ARTICLE ACTION BUTTONS (PDF / SHARE)
  // ---------------------------
  function addArticleActions() {
    const article = document.querySelector('.full-article') || fullArticle;
    if (!article) return;
    if (article.querySelector('.article-actions')) return; // already added

    const actionsHTML = `
      <div class="article-actions" style="margin-top:1rem; display:flex; gap:.6rem; flex-wrap:wrap;">
        <button class="download-article-btn btn" type="button">Télécharger en PDF</button>
        <button class="share-article-btn btn" type="button">Partager l'article</button>
      </div>
    `;
    const title = article.querySelector('h1');
    if (title) title.insertAdjacentHTML('afterend', actionsHTML);

    // event delegation for the newly inserted buttons
    article.addEventListener('click', (e) => {
      if (e.target.closest('.download-article-btn')) {
        downloadArticleAsPDF();
      } else if (e.target.closest('.share-article-btn')) {
        shareArticle();
      }
    });
  }

  // ---------------------------
  // INIT ANIMATIONS & OBSERVER
  // ---------------------------
  function initScrollAnimations() {
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      });
    }, observerOptions);

    $$('.card-modern, .stat-card, .review-card, .article-card').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      observer.observe(el);
    });
  }

  // ---------------------------
  // SMOOTH ANCHOR SCROLL
  // ---------------------------
  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        const target = document.querySelector(href);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  // ---------------------------
  // KEYBOARD SHORTCUTS (global)
  // ---------------------------
  function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + K : focus search
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        searchInput?.focus();
        return;
      }
      // Ctrl/Cmd + D : download article
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'd') {
        e.preventDefault();
        downloadArticleAsPDF();
        return;
      }
      // Ctrl/Cmd + Shift + S : share
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 's') {
        e.preventDefault();
        shareArticle();
        return;
      }
    });
  }

  // ---------------------------
  // LISTENERS FOR FILTER UI
  // ---------------------------
  function initFilterUI() {
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        state.searchQuery = e.target.value.toLowerCase().trim();
        if (searchClear) searchClear.classList.toggle('show', state.searchQuery !== '');
        filterAndSearchArticles();
      });
    }
    if (searchClear) {
      searchClear.addEventListener('click', () => {
        if (searchInput) searchInput.value = '';
        state.searchQuery = '';
        searchClear.classList.remove('show');
        filterAndSearchArticles();
      });
    }

    categoryBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        categoryBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.currentCategory = btn.dataset.category || 'all';
        filterAndSearchArticles();
      });
    });

    sortBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        sortBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.currentSort = btn.dataset.sort || 'recent';
        sortArticles();
      });
    });

    viewToggles.forEach(toggle => {
      toggle.addEventListener('click', () => {
        viewToggles.forEach(t => t.classList.remove('active'));
        toggle.classList.add('active');
        changeView(toggle.dataset.view || 'grid');
      });
    });

    if (resetFiltersBtn) {
      resetFiltersBtn.addEventListener('click', () => {
        if (searchInput) searchInput.value = '';
        state.searchQuery = '';
        if (searchClear) searchClear.classList.remove('show');
        state.currentCategory = 'all';
        state.currentSort = 'recent';
        categoryBtns.forEach(btn => btn.classList.toggle('active', (btn.dataset.category || '') === 'all'));
        sortBtns.forEach(btn => btn.classList.toggle('active', (btn.dataset.sort || '') === 'recent'));
        filterAndSearchArticles();
      });
    }
  }

  // ---------------------------
  // INIT
  // ---------------------------
  document.addEventListener('DOMContentLoaded', () => {
    // initial view from storage
    try {
      const v = localStorage.getItem('articles_view');
      if (v) changeView(v);
    } catch (e) {}

    // instantiate lightbox
    const lightbox = new ImageLightbox();

    // setup features
    initFilterUI();
    initReadMore();
    initReadingProgress();
    initTableOfContents(); // if full-article is present it will build TOC
    addArticleActions();
    initThemeAndSidebar();
    initScrollAnimations();
    initSmoothAnchors();
    initKeyboardShortcuts();

    // initial filter pass
    filterAndSearchArticles();

    // re-scan gallery images if dynamic content added later
    // simple mutation observer to refresh lightbox images automatically
    const mo = new MutationObserver(() => lightbox.setupGalleryImages());
    mo.observe(document.body, { childList: true, subtree: true });

    console.log("🚀 L'Air du Vol - Script fusionné chargé !");
  });

})();
