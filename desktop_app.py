"""
数学专业期末复习 — 桌面版
启动 Flask 服务，然后用 Chrome/Edge 的 app 模式打开（无地址栏，像原生应用）
"""
import os
import sys
import threading
import time
import subprocess
import requests
from app import app

def start_flask():
    app.run(debug=False, host="127.0.0.1", port=5000, use_reloader=False)

def open_app_window():
    """尝试用 Chrome/Edge app 模式打开，不行就用默认浏览器"""
    url = "http://127.0.0.1:5000"

    # 等 Flask 就绪
    for _ in range(40):
        try:
            requests.get(url, timeout=1)
            break
        except requests.ConnectionError:
            time.sleep(0.25)

    # 按优先级尝试：Chrome app 模式 → Edge app 模式 → 默认浏览器
    browsers = [
        # Chrome app 模式（无标签栏/地址栏，像桌面应用）
        ["chrome", f"--app={url}", "--window-size=1200,800"],
        [r"C:\Program Files\Google\Chrome\Application\chrome.exe", f"--app={url}", "--window-size=1200,800"],
        [r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", f"--app={url}", "--window-size=1200,800"],
        # Edge app 模式
        ["msedge", f"--app={url}", "--window-size=1200,800"],
        [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", f"--app={url}", "--window-size=1200,800"],
        [r"C:\Program Files\Microsoft\Edge\Application\msedge.exe", f"--app={url}", "--window-size=1200,800"],
    ]

    for cmd in browsers:
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return  # 成功打开
        except (FileNotFoundError, OSError):
            continue

    # 都不行就用系统默认浏览器
    import webbrowser
    webbrowser.open(url)
    print("已用默认浏览器打开: " + url)

if __name__ == "__main__":
    # 后台启动 Flask
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # 打开应用窗口
    open_app_window()

    # 保持主线程存活
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
