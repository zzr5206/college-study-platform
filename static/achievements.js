/* ── 成就系统 ── */
(function() {
    'use strict';

    var ACHIEVEMENTS = [
        // 里程碑
        {id:'first_quiz', name:'初试锋芒', desc:'完成第一次测验', icon:'🎯', cat:'milestone', check:function(d) { return d.totalQuizzes >= 1; }},
        {id:'quiz_10', name:'题海勇士', desc:'完成 10 次测验', icon:'⚔️', cat:'milestone', check:function(d) { return d.totalQuizzes >= 10; }},
        {id:'quiz_30', name:'考试达人', desc:'完成 30 次测验', icon:'🏅', cat:'milestone', check:function(d) { return d.totalQuizzes >= 30; }},
        {id:'wrong_5', name:'知错能改', desc:'收集 5 道错题', icon:'📝', cat:'milestone', check:function(d) { return d.wrongTotal >= 5; }},
        {id:'wrong_20', name:'错题收集家', desc:'收集 20 道错题', icon:'📚', cat:'milestone', check:function(d) { return d.wrongTotal >= 20; }},

        // 掌握
        {id:'master_complex', name:'复变大师', desc:'复变函数闪卡掌握 80%', icon:'🔵', cat:'mastery', check:function(d) { return (d.flashMastery['complex-analysis'] || 0) >= 0.8; }},
        {id:'master_algebra', name:'代数高手', desc:'抽象代数闪卡掌握 80%', icon:'🟢', cat:'mastery', check:function(d) { return (d.flashMastery['abstract-algebra'] || 0) >= 0.8; }},
        {id:'master_or', name:'运筹帷幄', desc:'运筹学闪卡掌握 80%', icon:'🟠', cat:'mastery', check:function(d) { return (d.flashMastery['operations-research'] || 0) >= 0.8; }},
        {id:'master_ds', name:'数据结构通', desc:'数据结构闪卡掌握 80%', icon:'🔴', cat:'mastery', check:function(d) { return (d.flashMastery['data-structures-c'] || 0) >= 0.8; }},

        // 坚持
        {id:'streak_3', name:'三日之约', desc:'连续学习 3 天', icon:'🔥', cat:'discipline', check:function(d) { return d.streak >= 3; }},
        {id:'streak_7', name:'一周战士', desc:'连续学习 7 天', icon:'💪', cat:'discipline', check:function(d) { return d.streak >= 7; }},
        {id:'streak_14', name:'半月之恒', desc:'连续学习 14 天', icon:'⭐', cat:'discipline', check:function(d) { return d.streak >= 14; }},
        {id:'streak_30', name:'一月学霸', desc:'连续学习 30 天', icon:'👑', cat:'discipline', check:function(d) { return d.streak >= 30; }},

        // 完成度
        {id:'path_100_complex', name:'复变全通', desc:'复变函数学习路径 100%', icon:'🔵', cat:'completion', check:function(d) { return (d.pathProgress['complex-analysis'] || 0) >= 1; }},
        {id:'path_100_algebra', name:'代数全通', desc:'抽象代数学习路径 100%', icon:'🟢', cat:'completion', check:function(d) { return (d.pathProgress['abstract-algebra'] || 0) >= 1; }},
        {id:'path_all_50', name:'四科入门', desc:'四科学习路径均达 50%', icon:'📖', cat:'completion', check:function(d) {
            var subs = ['complex-analysis','abstract-algebra','operations-research','data-structures-c'];
            return subs.every(function(k) { return (d.pathProgress[k] || 0) >= 0.5; });
        }},

        // 番茄
        {id:'pomodoro_10', name:'番茄新手', desc:'完成 10 个番茄钟', icon:'🍅', cat:'pomodoro', check:function(d) { return d.pomodoroTotal >= 10; }},
        {id:'pomodoro_50', name:'番茄达人', desc:'完成 50 个番茄钟', icon:'🍅', cat:'pomodoro', check:function(d) { return d.pomodoroTotal >= 50; }},
    ];

    function gatherData() {
        var qh = JSON.parse(localStorage.getItem('quiz_history') || '[]');
        var dailyActivity = JSON.parse(localStorage.getItem('daily_activity') || '{}');
        var pomodoro = JSON.parse(localStorage.getItem('pomodoro_sessions') || '{}');
        var sm2 = JSON.parse(localStorage.getItem('flashcard_sm2') || '{}');

        // 连续天数
        var streak = 0;
        for (var d = new Date(); ; d.setDate(d.getDate() - 1)) {
            if (dailyActivity[d.toISOString().split('T')[0]]) streak++;
            else break;
        }

        // 闪卡掌握率
        var flashMastery = {};
        for (var subj in sm2) {
            var entries = Object.values(sm2[subj]);
            var known = entries.filter(function(e) { return e.n >= 1; }).length;
            flashMastery[subj] = entries.length ? known / entries.length : 0;
        }

        // 学习路径进度
        var pathProgress = {};
        var subs = ['complex-analysis','abstract-algebra','operations-research','data-structures-c'];
        subs.forEach(function(k) {
            var saved = JSON.parse(localStorage.getItem('learning_path_' + k) || '{}');
            var total = Object.keys(saved).length || 7;
            var done = Object.values(saved).filter(function(v) { return v; }).length;
            pathProgress[k] = total ? done / total : 0;
        });

        // 番茄总数
        var pomodoroTotal = 0;
        for (var day in pomodoro) { pomodoroTotal += Math.floor((pomodoro[day] || 0) / 25); }

        // 错题数 (从仪表盘获取)
        var wrongTotal = 0;
        try {
            var wrongStats = document.getElementById('dash-wrong-total');
            if (wrongStats) wrongTotal = parseInt(wrongStats.textContent) || 0;
        } catch(e) {}

        return {
            totalQuizzes: qh.length,
            wrongTotal: wrongTotal,
            streak: streak,
            flashMastery: flashMastery,
            pathProgress: pathProgress,
            pomodoroTotal: pomodoroTotal
        };
    }

    function checkAndUnlock() {
        var unlocked = JSON.parse(localStorage.getItem('achievements') || '[]');
        var unlockedIds = unlocked.map(function(a) { return a.id; });
        var data = gatherData();
        var newlyUnlocked = [];

        ACHIEVEMENTS.forEach(function(ach) {
            if (unlockedIds.indexOf(ach.id) >= 0) return; // 已解锁
            try {
                if (ach.check(data)) {
                    unlocked.push({id: ach.id, unlockedAt: new Date().toISOString()});
                    newlyUnlocked.push(ach);
                }
            } catch(e) {}
        });

        if (newlyUnlocked.length > 0) {
            localStorage.setItem('achievements', JSON.stringify(unlocked));
            newlyUnlocked.forEach(function(ach) { showToast(ach); });
        }
    }

    function showToast(ach) {
        var toast = document.createElement('div');
        toast.className = 'achievement-toast';
        toast.innerHTML = '<span style="font-size:28px;">' + ach.icon + '</span><div><strong>🏆 成就解锁！</strong><br>' + ach.name + '：' + ach.desc + '</div>';
        document.body.appendChild(toast);
        setTimeout(function() { toast.classList.add('show'); }, 100);
        setTimeout(function() {
            toast.classList.remove('show');
            setTimeout(function() { toast.remove(); }, 400);
        }, 4000);
    }

    // 初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(checkAndUnlock, 1500);
        });
    } else {
        setTimeout(checkAndUnlock, 1500);
    }

    // 暴露给全局
    window._achievements = {
        getAll: function() { return ACHIEVEMENTS; },
        getUnlocked: function() { return JSON.parse(localStorage.getItem('achievements') || '[]'); },
        checkNow: checkAndUnlock
    };
})();
