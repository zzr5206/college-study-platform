/* ── 番茄钟学习计时器 ── */
(function() {
    'use strict';

    var state = {
        running: false,
        paused: false,
        focusMinutes: 25,
        breakMinutes: 5,
        longBreakMinutes: 15,
        cyclesBeforeLongBreak: 4,
        secondsLeft: 25 * 60,
        totalSeconds: 25 * 60,
        isBreak: false,
        cycleCount: 0,
        intervalId: null
    };

    // 从 localStorage 读取设置
    var saved = JSON.parse(localStorage.getItem('pomodoro_settings') || '{}');
    if (saved.focusMinutes) state.focusMinutes = saved.focusMinutes;
    if (saved.breakMinutes) state.breakMinutes = saved.breakMinutes;
    if (saved.longBreakMinutes) state.longBreakMinutes = saved.longBreakMinutes;
    state.secondsLeft = state.focusMinutes * 60;
    state.totalSeconds = state.secondsLeft;

    var container = null;
    var displayEl = null;
    var panelEl = null;
    var cycleEl = null;
    var labelEl = null;

    function createUI() {
        // 在导航栏创建计时器挂件
        container = document.createElement('div');
        container.className = 'pomodoro-wrap';
        container.innerHTML =
            '<button class="pomodoro-pill" id="pomodoro-pill" title="番茄钟">' +
            '🍅 <span id="pomodoro-time">' + formatTime(state.secondsLeft) + '</span>' +
            '</button>' +
            '<div class="pomodoro-panel" id="pomodoro-panel" style="display:none;">' +
            '<div class="pomodoro-label" id="pomodoro-label">🎯 专注 ' + state.focusMinutes + ' 分钟</div>' +
            '<div class="pomodoro-display" id="pomodoro-display">' + formatTime(state.secondsLeft) + '</div>' +
            '<div class="pomodoro-cycle" id="pomodoro-cycle">🍅 ' + (state.cycleCount % state.cyclesBeforeLongBreak) + '/' + state.cyclesBeforeLongBreak + '</div>' +
            '<div class="pomodoro-progress"><div class="pomodoro-progress-fill" id="pomodoro-progress-fill" style="width:100%"></div></div>' +
            '<div class="pomodoro-btns">' +
            '<button id="pomodoro-start" onclick="window._pomodoro.toggle()">▶ 开始</button>' +
            '<button id="pomodoro-reset" onclick="window._pomodoro.reset()">↺ 重置</button>' +
            '<button id="pomodoro-settings" onclick="window._pomodoro.showSettings()">⚙</button>' +
            '</div>' +
            '</div>';
        document.body.appendChild(container);

        displayEl = document.getElementById('pomodoro-display');
        panelEl = document.getElementById('pomodoro-panel');
        cycleEl = document.getElementById('pomodoro-cycle');
        labelEl = document.getElementById('pomodoro-label');

        // 点击挂件展开面板
        document.getElementById('pomodoro-pill').addEventListener('click', function(e) {
            e.stopPropagation();
            panelEl.style.display = panelEl.style.display === 'none' ? 'block' : 'none';
        });

        // 点击外部关闭面板
        document.addEventListener('click', function(e) {
            if (panelEl && !container.contains(e.target)) {
                panelEl.style.display = 'none';
            }
        });
    }

    function formatTime(secs) {
        var m = Math.floor(secs / 60);
        var s = secs % 60;
        return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    }

    function updateDisplay() {
        if (displayEl) displayEl.textContent = formatTime(state.secondsLeft);
        var pillTime = document.getElementById('pomodoro-time');
        if (pillTime) pillTime.textContent = formatTime(state.secondsLeft);
        var fill = document.getElementById('pomodoro-progress-fill');
        if (fill) fill.style.width = (state.secondsLeft / state.totalSeconds * 100) + '%';
    }

    function tick() {
        if (state.secondsLeft <= 0) {
            complete();
            return;
        }
        state.secondsLeft--;
        updateDisplay();
    }

    function complete() {
        stopTimer();
        var audioCtx = null;
        try {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = audioCtx.createOscillator();
            var gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.frequency.value = 800;
            gain.gain.value = 0.3;
            osc.start();
            osc.stop(audioCtx.currentTime + 0.2);
            setTimeout(function() {
                var osc2 = audioCtx.createOscillator();
                osc2.connect(gain);
                osc2.frequency.value = 1000;
                osc2.start();
                osc2.stop(audioCtx.currentTime + 0.3);
            }, 250);
        } catch(e) {}

        if (!state.isBreak) {
            // 专注完成 → 休息
            state.cycleCount++;
            var isLongBreak = (state.cycleCount % state.cyclesBeforeLongBreak === 0);
            state.isBreak = true;
            state.secondsLeft = (isLongBreak ? state.longBreakMinutes : state.breakMinutes) * 60;
            state.totalSeconds = state.secondsLeft;
            labelEl.textContent = isLongBreak ? ('☕ 长休息 ' + state.longBreakMinutes + ' 分钟') : ('☕ 休息 ' + state.breakMinutes + ' 分钟');
            cycleEl.textContent = '🍅 ' + (state.cycleCount % state.cyclesBeforeLongBreak) + '/' + state.cyclesBeforeLongBreak;

            // 记录专注分钟
            var today = new Date().toISOString().split('T')[0];
            var sessions = JSON.parse(localStorage.getItem('pomodoro_sessions') || '{}');
            sessions[today] = (sessions[today] || 0) + state.focusMinutes;
            localStorage.setItem('pomodoro_sessions', JSON.stringify(sessions));

            // 每日活跃
            var activity = JSON.parse(localStorage.getItem('daily_activity') || '{}');
            activity[today] = (activity[today] || 0) + 1;
            localStorage.setItem('daily_activity', JSON.stringify(activity));

            // 浏览器通知
            if ('Notification' in window && Notification.permission === 'granted') {
                new Notification('🍅 专注完成！', {body: '休息 ' + state.secondsLeft / 60 + ' 分钟吧', icon: '🍅'});
            }
        } else {
            // 休息完成 → 专注
            state.isBreak = false;
            state.secondsLeft = state.focusMinutes * 60;
            state.totalSeconds = state.secondsLeft;
            labelEl.textContent = '🎯 专注 ' + state.focusMinutes + ' 分钟';

            if ('Notification' in window && Notification.permission === 'granted') {
                new Notification('☕ 休息结束！', {body: '开始新的专注时段', icon: '🎯'});
            }
        }
        updateDisplay();
        autoStart();
    }

    function autoStart() {
        state.running = true;
        var btn = document.getElementById('pomodoro-start');
        if (btn) btn.textContent = '⏸ 暂停';
        var pill = document.getElementById('pomodoro-pill');
        if (pill) pill.classList.add('running');
        state.intervalId = setInterval(tick, 1000);
    }

    function stopTimer() {
        state.running = false;
        if (state.intervalId) { clearInterval(state.intervalId); state.intervalId = null; }
        var btn = document.getElementById('pomodoro-start');
        if (btn) btn.textContent = '▶ 开始';
        var pill = document.getElementById('pomodoro-pill');
        if (pill) pill.classList.remove('running');
    }

    // 公开 API
    window._pomodoro = {
        toggle: function() {
            if (state.running) {
                stopTimer();
            } else {
                autoStart();
            }
        },
        reset: function() {
            stopTimer();
            state.isBreak = false;
            state.secondsLeft = state.focusMinutes * 60;
            state.totalSeconds = state.secondsLeft;
            state.cycleCount = 0;
            labelEl.textContent = '🎯 专注 ' + state.focusMinutes + ' 分钟';
            cycleEl.textContent = '🍅 0/' + state.cyclesBeforeLongBreak;
            updateDisplay();
        },
        showSettings: function() {
            var f = prompt('专注时长（分钟）：', state.focusMinutes);
            var b = prompt('短休息时长（分钟）：', state.breakMinutes);
            var lb = prompt('长休息时长（分钟）：', state.longBreakMinutes);
            if (f) state.focusMinutes = parseInt(f) || 25;
            if (b) state.breakMinutes = parseInt(b) || 5;
            if (lb) state.longBreakMinutes = parseInt(lb) || 15;
            localStorage.setItem('pomodoro_settings', JSON.stringify({
                focusMinutes: state.focusMinutes,
                breakMinutes: state.breakMinutes,
                longBreakMinutes: state.longBreakMinutes
            }));
            this.reset();
        },
        getState: function() { return state; }
    };

    // 初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            createUI();
            if ('Notification' in window && Notification.permission === 'default') {
                setTimeout(function() { Notification.requestPermission(); }, 5000);
            }
        });
    } else {
        createUI();
        if ('Notification' in window && Notification.permission === 'default') {
            setTimeout(function() { Notification.requestPermission(); }, 5000);
        }
    }
})();
