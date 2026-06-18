/* ── 学习提醒系统 ── */
(function() {
    'use strict';

    var defaultReminders = {enabled: true, times: ['09:00', '14:00', '20:00']};
    var settings = JSON.parse(localStorage.getItem('study_reminders') || JSON.stringify(defaultReminders));
    var lastFired = {};

    function checkReminders() {
        if (!settings.enabled) return;
        var now = new Date();
        var currentTime = ('0' + now.getHours()).slice(-2) + ':' + ('0' + now.getMinutes()).slice(-2);

        settings.times.forEach(function(t) {
            if (t === currentTime && lastFired[t] !== now.toDateString()) {
                lastFired[t] = now.toDateString();
                fireReminder();
            }
        });
    }

    function fireReminder() {
        // 检查今天是否已有学习记录
        var today = new Date().toISOString().split('T')[0];
        var activity = JSON.parse(localStorage.getItem('daily_activity') || '{}');
        if (activity[today]) return; // 今天已经学过了

        // 浏览器通知
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('📚 学习时间到！', {
                body: '别忘了今天的复习计划，打开应用开始学习吧。',
                icon: '📚',
                tag: 'study-reminder'
            });
        }

        // 页面内提示
        showInAppToast();
    }

    function showInAppToast() {
        var toast = document.createElement('div');
        toast.className = 'achievement-toast';
        toast.style.cssText = 'position:fixed;top:16px;right:16px;z-index:999;background:var(--surface);border:2px solid var(--blue);border-radius:12px;padding:12px 20px;display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(0,0,0,.15);font-size:14px;transition:transform .4s;transform:translateX(120%);max-width:360px;';
        toast.innerHTML = '<span style="font-size:28px;">📚</span><div><strong>学习提醒</strong><br>到了预设的学习时间，开始今天的复习吧！</div>';
        document.body.appendChild(toast);
        setTimeout(function() { toast.style.transform = 'translateX(0)'; }, 100);
        setTimeout(function() {
            toast.style.transform = 'translateX(120%)';
            setTimeout(function() { toast.remove(); }, 400);
        }, 5000);
    }

    // 每分钟检查一次
    setInterval(checkReminders, 60000);
    // 页面加载时检查
    checkReminders();

    // 公共 API
    window._reminders = {
        getSettings: function() { return settings; },
        updateSettings: function(newSettings) {
            settings = Object.assign(settings, newSettings);
            localStorage.setItem('study_reminders', JSON.stringify(settings));
        }
    };

})();
