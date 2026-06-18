# 大学生智能学习平台

一个面向大学生期末复习和日常学习的本地 Web 应用，基于 Flask 构建。项目内置数学专业课、数据结构、英语四六级等复习资料，并提供错题本、题库练习、闪卡复习、每日计划、拍题检索等学习工具。

## 功能

- 多学科复习资料：复变函数、抽象代数、运筹学、数据结构 C、英语四六级。
- 题库练习：整合知识点题库、扩展练习、近年题型和英语练习。
- 错题本：支持记录错题、答案、避坑要点和图片上传。
- 闪卡与强化复习：支持前端本地存储学习进度，辅助间隔复习。
- PWA 支持：包含 manifest 和 service worker，可作为浏览器应用安装。
- 桌面启动器：`desktop_app.py` 可用浏览器 app 模式打开本地服务。

## 项目结构

```text
college-study-platform/
  app.py                 # Flask Web 应用入口
  desktop_app.py         # 桌面模式启动入口
  requirements.txt       # Python 依赖
  references/            # 内置复习资料和题库
  static/                # CSS、JS、PWA 文件和上传目录
  templates/             # Flask 页面模板
```

## 快速开始

需要 Python 3.10 或更高版本。

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

启动后打开：

```text
http://127.0.0.1:5000
```

如果想以类似桌面应用的方式打开：

```bash
python desktop_app.py
```

## 数据说明

- `references/` 中的 Markdown 文件是应用读取的知识库和题库。
- 错题图片会保存到 `static/uploads/`，该目录默认不提交个人上传内容。
- 学习计时、闪卡等前端进度主要保存在浏览器本地存储中。

## 开源说明

本项目适合作为大学课程设计、学习工具原型或个人复习系统继续扩展。欢迎根据自己的专业课程替换 `references/` 中的资料。

## License

MIT
