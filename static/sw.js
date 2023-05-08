if (typeof navigator.serviceWorker !== 'undefined') {
    navigator.serviceWorker.register('static/sw.js');
    navigator.serviceWorker.ready.then(function(registration) {
        // Register the service worker for push
        registration.pushManager.subscribe({userVisibleOnly: true})
            .then(function(subscription) {
                console.log('Push subscribed:', subscription.endpoint);
                // Store the subscription endpoint on your server and send it to the client if needed
            })
            .catch(function(error) {
                console.error('Push subscription error:', error);
            });
    });
}

const CACHE_NAME = 'cool-cache';

// Add whichever assets you want to pre-cache here:
const PRECACHE_ASSETS = [
    'static/assets/',
    'static/files-dashboard/',
    'static/files-login/',
    'static/img/',
    'static/library/'
]

// Listener for the install event - pre-caches our assets list on service worker install.
self.addEventListener('install', event => {
    event.waitUntil((async () => {
        const cache = await caches.open(CACHE_NAME);
        cache.addAll(PRECACHE_ASSETS);
    })());
});

self.addEventListener('install', event => {
    event.waitUntil((async () => {
        const cache = await caches.open(CACHE_NAME);
        cache.addAll(PRECACHE_ASSETS);
    })());
});

self.addEventListener('activate', event => {
  event.waitUntil(clients.claim());
});

self.addEventListener('fetch', event => {
  event.respondWith(async () => {
      const cache = await caches.open(CACHE_NAME);

      // match the request to our cache
      const cachedResponse = await cache.match(event.request);

      // check if we got a valid response
      if (cachedResponse !== undefined) {
          // Cache hit, return the resource
          return cachedResponse;
      } else {
        // Otherwise, go to the network
          return fetch(event.request)
      };
  });
});
