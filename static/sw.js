if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('static/sw.js')
    .then(registration => {
      console.log('Service worker registered successfully:', registration);
    })
    .catch(error => {
      console.error('Service worker registration failed:', error);
    });
}


// Define the cache name
const CACHE_NAME = 'actsautoproject-cache';

// List the files to cache
const FILES_TO_CACHE = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/images/logo.png',
  'https://fonts.googleapis.com/css?family=Open+Sans&display=swap'
];

// Install the Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

// Intercept network requests
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      if (response) {
        return response;
      } else {
        return fetch(event.request);
      }
    })
  );
});

// Delete outdated caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          return cacheName.startsWith('actsautoproject-') &&
            cacheName !== CACHE_NAME;
        }).map(function(cacheName) {
          return caches.delete(cacheName);
        })
      );
    })
  );
});
