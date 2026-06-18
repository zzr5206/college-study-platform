/* ── 大学生智能学习平台 — Service Worker ── */
var CACHE_NAME = 'math-review-v2';
var STATIC_ASSETS = [
    '/',
    '/static/style.css',
    '/static/timer.js',
    '/static/achievements.js',
    '/static/notifications.js',
    '/static/notes.js',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
    'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js',
    'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js',
];

// 安装：缓存静态资源
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(STATIC_ASSETS).catch(function(err) {
                console.log('SW cache install failed (may be offline):', err);
            });
        })
    );
    self.skipWaiting();
});

// 激活：清理旧缓存
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(keys) {
            return Promise.all(
                keys.filter(function(key) { return key !== CACHE_NAME; })
                    .map(function(key) { return caches.delete(key); })
            );
        })
    );
    self.clients.claim();
});

// 请求拦截：缓存优先（静态资源），网络优先（HTML 页面）
self.addEventListener('fetch', function(event) {
    var url = new URL(event.request.url);

    // 跳过非 GET 请求
    if (event.request.method !== 'GET') return;

    // CDN 资源：缓存优先
    if (url.hostname.includes('cdn.jsdelivr.net')) {
        event.respondWith(
            caches.match(event.request).then(function(cached) {
                return cached || fetch(event.request).then(function(response) {
                    var clone = response.clone();
                    caches.open(CACHE_NAME).then(function(cache) { cache.put(event.request, clone); });
                    return response;
                });
            })
        );
        return;
    }

    // 本地静态资源：缓存优先
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(event.request).then(function(cached) {
                return cached || fetch(event.request).then(function(response) {
                    var clone = response.clone();
                    caches.open(CACHE_NAME).then(function(cache) { cache.put(event.request, clone); });
                    return response;
                });
            })
        );
        return;
    }

    // HTML 页面：网络优先，失败时回退缓存
    event.respondWith(
        fetch(event.request).catch(function() {
            return caches.match(event.request);
        })
    );
});
