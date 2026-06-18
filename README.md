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

## 部署到 Render

仓库已经包含 `render.yaml`，可以在 Render 上作为 Python Web Service 部署。

1. 打开 [Render Dashboard](https://dashboard.render.com/)。
2. 选择 `New` -> `Blueprint` 或 `Web Service`。
3. 连接 GitHub 仓库 `zzr5206/college-study-platform`。
4. 如果手动填写配置，使用：

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

部署成功后，Render 会生成一个 `onrender.com` 网址。以后推送到 GitHub 的 `main` 分支，Render 会自动重新部署。

注意：免费 Web Service 的本地文件系统不适合作为长期存储，`static/uploads/` 中用户上传的图片可能在重启或重新部署后丢失。正式多人使用时，建议后续接入对象存储或数据库。

## 数据说明

- `references/` 中的 Markdown 文件是应用读取的知识库和题库。
- 错题图片会保存到 `static/uploads/`，该目录默认不提交个人上传内容。
- 学习计时、闪卡等前端进度主要保存在浏览器本地存储中。

## 开源说明

本项目适合作为大学课程设计、学习工具原型或个人复习系统继续扩展。欢迎根据自己的专业课程替换 `references/` 中的资料。

## License

MIT
