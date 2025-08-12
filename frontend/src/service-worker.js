/* eslint-disable no-undef */
import { clientsClaim } from 'workbox-core';
import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { NavigationRoute, registerRoute } from 'workbox-routing';
import { NetworkFirst } from 'workbox-strategies';

self.skipWaiting();
clientsClaim();

// This is what CRA's InjectManifest replaces at build time:
precacheAndRoute(self.__WB_MANIFEST || []);
cleanupOutdatedCaches();

// Optional: SPA navigation fallback cached via network-first
registerRoute(
  new NavigationRoute(
    new NetworkFirst({
      cacheName: 'html-cache',
    })
  )
);

// You can add runtime caching here (APIs, images, etc.)
