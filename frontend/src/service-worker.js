// Basic offline cache (dev/demo)
self.addEventListener('install', event => {
  event.waitUntil(caches.open('tsembwog-v1').then(cache => cache.addAll(['/'])));
});
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(resp => resp || fetch(event.request))
  );
});
