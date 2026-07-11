// I 'Member Movies — offline shell. Your log is localStorage; search needs network.
// Shell strategy: NETWORK-FIRST for pages (instant updates), cache fallback for offline.
const CACHE = "imember-v23";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;   // cinemeta/posters: straight to network
  const isPage = e.request.mode === "navigate" || url.pathname.endsWith("index.html");
  if (isPage){
    // network-first WITH cache:"no-cache" — GitHub Pages sends max-age=600, and the
    // browser HTTP cache survives app kills; no-cache forces an etag revalidation
    // (cheap 304 when unchanged, fresh HTML the moment a deploy lands).
    e.respondWith(
      fetch(e.request, {cache: "no-cache"}).then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return r;
      }).catch(() => caches.match(e.request).then(hit => hit || caches.match("./index.html")))
    );
  } else {
    e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request)));
  }
});
