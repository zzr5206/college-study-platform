/* ── 学习笔记系统 ── */
(function() {
    'use strict';

    var NOTES_KEY = 'study_notes';
    var notes = JSON.parse(localStorage.getItem(NOTES_KEY) || '{}');
    var currentSubject = '';
    var currentHeading = '';
    var panel = null;
    var isOpen = false;

    function init() {
        // 检测当前科目（从 URL 路径或页面元素获取）
        var path = window.location.pathname;
        var match = path.match(/\/subject\/([a-z-]+)/);
        if (!match) return;
        currentSubject = match[1];

        createFAB();
        createPanel();
        updateTOCIndicators();
        loadNotesList();
    }

    function createFAB() {
        var fab = document.createElement('button');
        fab.id = 'notes-fab';
        fab.className = 'notes-fab';
        fab.title = '学习笔记';
        fab.innerHTML = '📝';
        fab.onclick = togglePanel;
        document.body.appendChild(fab);
    }

    function createPanel() {
        panel = document.createElement('div');
        panel.id = 'notes-panel';
        panel.className = 'notes-panel';
        panel.innerHTML =
            '<div class="notes-panel-header">' +
            '<h4>📝 学习笔记</h4>' +
            '<button class="notes-close" onclick="document.getElementById(\'notes-panel\').classList.remove(\'open\'); document.getElementById(\'notes-fab\').style.display=\'\';">✕</button>' +
            '</div>' +
            '<div class="notes-current" id="notes-current-heading">点击下方标题添加笔记</div>' +
            '<textarea id="notes-textarea" class="notes-textarea" placeholder="在这里写笔记…支持 Markdown 格式和 LaTeX 公式"></textarea>' +
            '<div class="notes-actions">' +
            '<button onclick="window._notes.save()">💾 保存</button>' +
            '<button onclick="window._notes.deleteNote()" style="background:#fef2f2;border-color:#ef4444;color:#ef4444;">🗑 删除</button>' +
            '</div>' +
            '<div class="notes-list-header">📋 笔记列表</div>' +
            '<div class="notes-list" id="notes-list"></div>' +
            '<div class="notes-export">' +
            '<button onclick="window._notes.exportNotes()" style="font-size:12px;">📥 导出笔记</button>' +
            '</div>';
        document.body.appendChild(panel);
    }

    function togglePanel() {
        isOpen = !isOpen;
        if (isOpen) {
            panel.classList.add('open');
            document.getElementById('notes-fab').style.display = 'none';
            // 尝试获取当前滚动到的标题
            detectCurrentHeading();
        } else {
            panel.classList.remove('open');
            document.getElementById('notes-fab').style.display = '';
        }
    }

    function detectCurrentHeading() {
        var headings = document.querySelectorAll('#article-content h2, #article-content h3');
        var found = '';
        headings.forEach(function(h) {
            if (h.getBoundingClientRect().top < 150) found = h.textContent.trim().substring(0, 60);
        });
        if (found) {
            currentHeading = found;
            document.getElementById('notes-current-heading').textContent = '📍 ' + found;
            loadCurrentNote();
        }
    }

    function loadCurrentNote() {
        if (!notes[currentSubject]) notes[currentSubject] = {};
        var key = currentHeading;
        var note = notes[currentSubject][key];
        document.getElementById('notes-textarea').value = note ? note.text : '';
    }

    function loadNotesList() {
        var list = document.getElementById('notes-list');
        if (!list) return;
        var subjNotes = notes[currentSubject] || {};
        var keys = Object.keys(subjNotes);
        if (!keys.length) {
            list.innerHTML = '<div style="color:var(--text-secondary);font-size:13px;padding:8px;">暂无笔记</div>';
            return;
        }
        // 按更新时间排序
        keys.sort(function(a, b) { return (subjNotes[b].updatedAt || '') > (subjNotes[a].updatedAt || '') ? 1 : -1; });
        list.innerHTML = keys.map(function(k) {
            var n = subjNotes[k];
            return '<div class="notes-list-item" onclick="window._notes.jumpTo(\'' + k.replace(/'/g, "\\'") + '\')">' +
                '<div class="notes-list-title">' + k + '</div>' +
                '<div class="notes-list-meta">' + (n.updatedAt || '') + '</div>' +
            '</div>';
        }).join('');
    }

    // 公开 API
    window._notes = {
        save: function() {
            var text = document.getElementById('notes-textarea').value.trim();
            if (!currentHeading) {
                alert('请先在页面中滚动到一个标题段落，再保存笔记。');
                return;
            }
            if (!text) {
                alert('请输入笔记内容。');
                return;
            }
            if (!notes[currentSubject]) notes[currentSubject] = {};
            notes[currentSubject][currentHeading] = {
                text: text,
                updatedAt: new Date().toISOString().split('T')[0]
            };
            localStorage.setItem(NOTES_KEY, JSON.stringify(notes));
            loadNotesList();
            updateTOCIndicators();
            // 简短反馈
            var ta = document.getElementById('notes-textarea');
            var origBg = ta.style.background;
            ta.style.background = '#f0fdf4';
            setTimeout(function() { ta.style.background = origBg; }, 500);
        },
        deleteNote: function() {
            if (!currentHeading || !notes[currentSubject] || !notes[currentSubject][currentHeading]) {
                alert('当前段落暂无笔记。');
                return;
            }
            if (!confirm('确定删除「' + currentHeading + '」的笔记？')) return;
            delete notes[currentSubject][currentHeading];
            localStorage.setItem(NOTES_KEY, JSON.stringify(notes));
            document.getElementById('notes-textarea').value = '';
            loadNotesList();
            updateTOCIndicators();
        },
        jumpTo: function(heading) {
            currentHeading = heading;
            document.getElementById('notes-current-heading').textContent = '📍 ' + heading;
            loadCurrentNote();
            // 滚动到该标题
            var headings = document.querySelectorAll('#article-content h2, #article-content h3');
            headings.forEach(function(h) {
                if (h.textContent.trim().substring(0, 60) === heading) {
                    h.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
            });
        },
        exportNotes: function() {
            var md = '# ' + currentSubject + ' 学习笔记\n\n';
            var subjNotes = notes[currentSubject] || {};
            var keys = Object.keys(subjNotes);
            keys.sort(function(a, b) { return (subjNotes[b].updatedAt || '') > (subjNotes[a].updatedAt || '') ? 1 : -1; });
            keys.forEach(function(k) {
                md += '## ' + k + '\n\n' + subjNotes[k].text + '\n\n> 更新于 ' + (subjNotes[k].updatedAt || '未知') + '\n\n---\n\n';
            });
            var blob = new Blob([md], {type: 'text/markdown'});
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = currentSubject + '-notes.md';
            a.click();
            URL.revokeObjectURL(url);
        }
    };

    function updateTOCIndicators() {
        // 在 TOC 中标记有笔记的标题
        var subjNotes = notes[currentSubject] || {};
        var noteKeys = Object.keys(subjNotes);
        if (!noteKeys.length) return;
        var tocLinks = document.querySelectorAll('#toc-nav .toc-link');
        tocLinks.forEach(function(link) {
            var text = link.textContent.trim().substring(0, 60);
            if (noteKeys.indexOf(text) >= 0) {
                link.innerHTML += ' 📝';
            }
        });
    }

    // 初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
