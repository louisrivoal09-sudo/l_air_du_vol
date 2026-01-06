/**
 * Service Worker pour le mode offline
 * Permet de consulter les articles/avions en cache sans connexion
 */

const CACHE_NAME = 'air-du-vol-v1';
const URLS_TO_CACHE = [
  '/',
  '/static/css/style.css',
  '/static/css/dark-mode-complete.css',
  '/static/js/user-settings.js',
  '/static/js/main.js',
  '/static/images/logo.png'
];

// Installation du service worker
self.addEventListener('install', event => {
  console.log('🔧 Service Worker: Installation en cours...');
  
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('📦 Mise en cache des ressources');
      return cache.addAll(URLS_TO_CACHE).catch(err => {
        console.warn('⚠️ Erreur lors de la mise en cache:', err);
      });
    })
  );
  
  self.skipWaiting();
});

// Activation du service worker
self.addEventListener('activate', event => {
  console.log('✨ Service Worker: Activation');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('🧹 Suppression du cache ancien:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  self.clients.claim();
});

// Stratégie network-first avec fallback au cache
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Ignorer les requêtes non-HTTP
  if (!url.protocol.startsWith('http')) {
    return;
  }

  // API requests - try network first, fallback to cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Mettre en cache les réponses réussies
          if (response.ok && request.method === 'GET') {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // Fallback au cache si pas de réseau
          return caches.match(request).then(cachedResponse => {
            return cachedResponse || new Response('Mode offline - Données non disponibles', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({
                'Content-Type': 'text/plain'
              })
            });
          });
        })
    );
    return;
  }

  // Cache first pour les assets statiques
  if (request.method === 'GET' && 
      (request.url.includes('/static/') || 
       request.url.includes('/media/'))) {
    event.respondWith(
      caches.match(request).then(cachedResponse => {
        return cachedResponse || fetch(request).then(response => {
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, responseClone);
            });
          }
          return response;
        }).catch(() => {
          // Placeholder si asset pas en cache
          if (request.destination === 'image') {
            return new Response(
              '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect fill="#ddd" width="200" height="200"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="14" fill="#999">Image non disponible</text></svg>',
              { headers: { 'Content-Type': 'image/svg+xml' } }
            );
          }
          return new Response('Asset non disponible', { status: 404 });
        });
      })
    );
    return;
  }

  // Network first pour les pages HTML
  event.respondWith(
    fetch(request)
      .then(response => {
        // Ne mettre en cache que les réponses valides
        if (response.ok && request.method === 'GET') {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Fallback au cache
        return caches.match(request).then(cachedResponse => {
          return cachedResponse || new Response(
            '<!DOCTYPE html><html><body><h1>Mode Offline</h1><p>Cette page n\'est pas disponible hors ligne.</p></body></html>',
            {
              status: 503,
              headers: { 'Content-Type': 'text/html; charset=utf-8' }
            }
          );
        });
      })
  );
});

// Message handler pour les événements depuis le client
self.addEventListener('message', event => {
  const { type, payload } = event.data;

  if (type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.delete(CACHE_NAME).then(() => {
        console.log('🧹 Cache cleared');
        event.ports[0].postMessage({ success: true });
      })
    );
  }

  if (type === 'GET_CACHE_SIZE') {
    event.waitUntil(
      caches.open(CACHE_NAME).then(cache => {
        return cache.keys().then(requests => {
          event.ports[0].postMessage({ 
            success: true, 
            size: requests.length 
          });
        });
      })
    );
  }
});

// Événements de synchronisation en arrière-plan (pour iOS/Android)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-offline-cache') {
    event.waitUntil(
      syncOfflineCache()
    );
  }
});

async function syncOfflineCache() {
  try {
    const response = await fetch('/api/offline/cache/');
    if (response.ok) {
      console.log('✅ Synchronisation offline réussie');
    }
  } catch (err) {
    console.error('❌ Erreur de synchronisation:', err);
  }
}
