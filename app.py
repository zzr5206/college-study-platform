# -*- coding: utf-8 -*-
"""数学专业期末复习 — Web 版"""
import os
import re
import webbrowser
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for
from markdown import markdown as md_to_html

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.json.ensure_ascii = False  # Flask 3.x 兼容：确保 API 返回中文不转义

# 路径配置
BASE = Path(__file__).parent
REFS = BASE / "references"

SUBJECTS = {
    "complex-analysis": {"name": "复变函数", "icon": "🔵", "file": "complex-analysis.md"},
    "abstract-algebra": {"name": "抽象代数", "icon": "🟢", "file": "abstract-algebra.md"},
    "operations-research": {"name": "运筹学", "icon": "🟠", "file": "operations-research.md"},
    "data-structures-c": {"name": "数据结构 C", "icon": "🔴", "file": "data-structures-c.md"},
    "english-cet": {"name": "英语四六级", "icon": "🔤", "file": "english-cet.md"},
    "cet4-hacks": {"name": "四级邪修技巧", "icon": "🪄", "file": "cet4-hacks.md"},
}

PRACTICE_FILES = ["practice-bank.md", "expanded-exercise-bank.md", "recent-exam-problems.md", "english-cet-practice.md"]
WRONG_FILE = REFS / "my-wrong-problems.md"
WRONG_NOTES_FILE = REFS / "wrong-notes.md"
ROADMAP_FILE = REFS / "study-roadmap.md"


# ── helpers ──────────────────────────────────────────────

def read_md(filename: str) -> str:
    """读取 references 下的 .md 文件"""
    path = REFS / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"*文件 {filename} 不存在*"


def md_content(filename: str) -> str:
    """markdown → HTML，保护 LaTeX 公式不被破坏"""
    raw = read_md(filename)
    math_parts = []

    def protect(m):
        math_parts.append(m.group(0))
        return f'@@@MATH_{len(math_parts)-1}@@@'

    # 保护块级公式: \[ ... \]
    raw = re.sub(r'\\\[(.+?)\\\]', protect, raw, flags=re.DOTALL)
    # 保护行内公式: \( ... \)
    raw = re.sub(r'\\\((.+?)\\\)', protect, raw)

    # markdown → HTML（只用安全扩展，避免 codehilite 依赖问题）
    html = md_to_html(raw, extensions=["fenced_code", "tables"])
    # 外链在新标签页打开
    html = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', html)

    # 还原数学公式，统一转成 $ / $$ 分隔符（KaTeX 原生支持，不会被转义）
    for i, part in enumerate(math_parts):
        if part.startswith("\\["):
            cooked = "$$" + part[2:-2].strip() + "$$"
        else:  # \(...\)
            cooked = "$" + part[2:-2].strip() + "$"
        html = html.replace(f"@@@MATH_{i}@@@", cooked)

    return html


def parse_wrong_problems() -> list[dict]:
    """解析 my-wrong-problems.md 中的错题列表"""
    if not WRONG_FILE.exists():
        return []
    text = WRONG_FILE.read_text(encoding="utf-8")
    problems = []
    # 匹配每个 ## 开头的错题条目
    pattern = re.compile(
        r'## \[(.+?)\]\s*(.+?)\s*—\s*(\d{4}-\d{2}-\d{2})\n(.*?)(?=\n## \[|\Z)',
        re.DOTALL,
    )
    for m in pattern.finditer(text):
        problems.append({
            "subject": m.group(1),
            "title": m.group(2).strip(),
            "date": m.group(3),
            "body": m.group(4).strip(),
        })
    return problems


def append_wrong_problem(subject: str, title: str, wrong_work: str, solution: str, images: list[str] = None) -> None:
    """追加一道错题到 my-wrong-problems.md"""
    today = datetime.now().strftime("%Y-%m-%d")
    img_md = ""
    if images:
        img_md = "\n\n### 图片\n" + "\n".join(f"![](/{img})" for img in images)
    entry = f"""

## [{subject}] {title} — {today}

### 原题
{wrong_work.strip()}

### 解答
{solution.strip()}
{img_md}
### 避坑要点
*待补充*
"""
    with open(WRONG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    # 更新统计
    update_stats(subject)


def update_stats(subject_tag: str) -> None:
    """更新 my-wrong-problems.md 顶部的统计表"""
    if not WRONG_FILE.exists():
        return
    text = WRONG_FILE.read_text(encoding="utf-8")
    problems = parse_wrong_problems()

    # 计算各科数量
    counts = {"复变函数": 0, "抽象代数": 0, "运筹学": 0, "数据结构 C": 0}
    name_map = {
        "复变函数": "复变函数", "抽象代数": "抽象代数",
        "运筹学": "运筹学", "数据结构 C": "数据结构 C",
    }
    for p in problems:
        for k in name_map:
            if k in p["subject"]:
                counts[k] += 1
                break

    total = sum(counts.values())
    new_stats = (
        f"| 复变函数 | {counts['复变函数']} |\n"
        f"| 抽象代数 | {counts['抽象代数']} |\n"
        f"| 运筹学 | {counts['运筹学']} |\n"
        f"| 数据结构 C | {counts['数据结构 C']} |\n"
        f"| **合计** | **{total}** |\n"
        f"\n*最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}*"
    )

    # 替换统计区
    text = re.sub(
        r'\| 复变函数 \|.*\n\| 抽象代数 \|.*\n\| 运筹学 \|.*\n\| 数据结构 C \|.*\n\| \*\*合计\*\* \|.*\n\n\*最后更新.*\*',
        new_stats,
        text,
    )
    with open(WRONG_FILE, "w", encoding="utf-8") as f:
        f.write(text)


def get_wrong_stats() -> dict:
    """获取错题统计"""
    problems = parse_wrong_problems()
    for p in problems:
        # 把 body 中的 markdown 图片转为 HTML img 标签
        p["body_html"] = re.sub(
            r'!\[.*?\]\((.+?)\)',
            r'<img src="\1" style="max-width:100%;border-radius:8px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,.1);">',
            p["body"]
        )
        # 把换行转为 <br>
        p["body_html"] = p["body_html"].replace("\n", "<br>")
    counts = {"复变函数": 0, "抽象代数": 0, "运筹学": 0, "数据结构 C": 0}
    for p in problems:
        for k in counts:
            if k in p["subject"]:
                counts[k] += 1
                break
    return {"problems": problems, "counts": counts, "total": sum(counts.values())}


# ── routes ───────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", subjects=SUBJECTS)


@app.route("/subject/<key>")
def subject(key):
    if key not in SUBJECTS:
        return redirect(url_for("index"))
    info = SUBJECTS[key]
    content = md_content(info["file"])
    return render_template("subject.html", subject=info, key=key, content=content, subjects=SUBJECTS)


@app.route("/practice")
def practice():
    # 合并两个题库
    combined = ""
    for f in PRACTICE_FILES:
        combined += read_md(f) + "\n\n"
    html = md_content("practice-bank.md") + md_content("expanded-exercise-bank.md") + md_content("recent-exam-problems.md") + md_content("english-cet-practice.md")
    return render_template("practice.html", content=html, subjects=SUBJECTS)


@app.route("/wrong", methods=["GET", "POST"])
def wrong():
    if request.method == "POST":
        subject_tag = request.form.get("subject", "")
        title = request.form.get("title", "").strip()
        wrong_work = request.form.get("wrong_work", "").strip()
        solution = request.form.get("solution", "").strip()

        # 处理图片上传
        saved_images = []
        uploaded = request.files.getlist("images")
        upload_dir = BASE / "static" / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        for file in uploaded:
            if file and file.filename and allowed_image(file.filename):
                # 用时间戳避免重名
                ext = Path(file.filename).suffix or ".jpg"
                fname = f"{datetime.now().strftime('%Y%m%d_%H%M%S_')}{len(saved_images)}{ext}"
                file.save(str(upload_dir / fname))
                saved_images.append(f"static/uploads/{fname}")

        if title and (wrong_work or saved_images):
            append_wrong_problem(subject_tag, title, wrong_work, solution, saved_images)

        return redirect(url_for("wrong"))

    stats = get_wrong_stats()
    return render_template("wrong.html", stats=stats, subjects=SUBJECTS)


def allowed_image(filename: str) -> bool:
    return Path(filename).suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}


@app.route("/review")
def review():
    wrong_notes_html = md_content("wrong-notes.md")
    roadmap_html = md_content("study-roadmap.md")
    return render_template("review.html", wrong_notes=wrong_notes_html, roadmap=roadmap_html, subjects=SUBJECTS)


@app.route("/api/wrong-random")
def api_wrong_random():
    """随机返回 3 道错题"""
    import random
    problems = parse_wrong_problems()
    if len(problems) <= 3:
        return {"problems": problems}
    selected = random.sample(problems, 3)
    return {"problems": selected}


# ── 搜索 ─────────────────────────────────────────────────

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    if not q or len(q) < 2:
        return {"results": []}
    results = []
    for key, info in SUBJECTS.items():
        text = read_md(info["file"])
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if q.lower() in line.lower():
                # 找最近的标题作为上下文
                heading = ""
                for j in range(i, -1, -1):
                    if lines[j].startswith("##"):
                        heading = lines[j].lstrip("#").strip()
                        break
                # 清理 markdown 格式符号，避免搜索下拉中显示乱码
                snippet = line.strip()[:200]
                snippet = re.sub(r'^#{1,4}\s*', '', snippet)  # 去掉标题标记
                snippet = re.sub(r'\*\*(.+?)\*\*', r'\1', snippet)  # 去掉加粗标记
                snippet = re.sub(r'`(.+?)`', r'\1', snippet)  # 去掉代码标记
                results.append({
                    "subject": info["name"],
                    "icon": info["icon"],
                    "key": key,
                    "heading": heading,
                    "snippet": snippet,
                    "score": 10 if q.lower() in heading.lower() else 5,
                })
    results.sort(key=lambda r: r["score"], reverse=True)
    return {"results": results[:15]}


# ── 测验 ─────────────────────────────────────────────────

QUIZ_SUBJECT_MAP = {
    "complex-analysis": "复变函数",
    "abstract-algebra": "抽象代数",
    "operations-research": "运筹学",
    "data-structures-c": "数据结构 C",
    "english-cet": "英语四六级",
}

def parse_quiz_problems(subject_key: str = None) -> list[dict]:
    """从题库中解析题目，返回 [{"title":..., "body":..., "subject":...}]"""
    problems = []
    for fname in PRACTICE_FILES:
        text = read_md(fname)
        lines = text.split("\n")
        # 如果是英语题库文件，默认科目为英语四六级
        current_subject = "英语四六级" if "english" in fname else ""
        current_problem = None

        for line in lines:
            # 检测科目标题 ## 或 ###
            for sn in QUIZ_SUBJECT_MAP.values():
                if sn in line and (line.startswith("##") or line.startswith("###")) and len(line) < 80:
                    current_subject = sn
                    break
            # 英语专项标题检测
            if "english" in fname:
                eng_headers = ["听力", "阅读", "写作", "翻译", "词汇语法", "词汇", "语法"]
                for eh in eng_headers:
                    if eh in line and line.startswith("##"):
                        current_subject = "英语四六级"
                        break

            # 检测题目开始（兼容"题 E1"、"E14"、"真题 A1"等格式）
            if re.match(r'###\s+.*?\d+[:：]', line):
                if current_problem:
                    problems.append(current_problem)
                current_problem = {
                    "title": line.replace("###", "").strip()[:80],
                    "body": line + "\n",
                    "subject": current_subject,
                    "subject_key": [k for k, v in QUIZ_SUBJECT_MAP.items() if v == current_subject][0] if current_subject else "",
                }
            elif current_problem:
                current_problem["body"] += line + "\n"

        if current_problem:
            problems.append(current_problem)

    return problems


@app.route("/quiz")
def quiz_page():
    subject_filter = request.args.get("subject", "")
    return render_template("quiz.html", subjects=SUBJECTS, subject_filter=subject_filter)


@app.route("/api/quiz/problems")
def api_quiz_problems():
    import random
    subject = request.args.get("subject", "")
    count = int(request.args.get("count", 5))
    adaptive = request.args.get("adaptive", "0") == "1"
    all_problems = parse_quiz_problems()

    if adaptive:
        # 自适应模式：优先选弱科题目
        stats = get_wrong_stats()
        counts = stats["counts"]
        total_wrong = sum(counts.values())
        if total_wrong > 0:
            # 按错题比例分配题目数
            adaptive_pool = []
            subj_alloc = {}
            remaining = count
            sorted_subjs = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            for i, (subj, wc) in enumerate(sorted_subjs):
                if wc == 0:
                    continue
                alloc = max(1, round(count * wc / total_wrong))
                if i == len(sorted_subjs) - 1 or len([s for s in sorted_subjs if s[1] > 0]) == 1:
                    alloc = remaining
                alloc = min(alloc, remaining)
                subj_alloc[subj] = alloc
                remaining -= alloc
                if remaining <= 0:
                    break
            # 按分配从各科选题
            for subj, alloc in subj_alloc.items():
                subj_problems = [p for p in all_problems if p["subject"] == subj]
                if subj_problems:
                    n = min(alloc, len(subj_problems))
                    adaptive_pool.extend(random.sample(subj_problems, n))
            if adaptive_pool:
                random.shuffle(adaptive_pool)
                all_problems = adaptive_pool[:count]

    if subject and not adaptive:
        all_problems = [p for p in all_problems if p["subject"] == subject]
    if len(all_problems) <= count:
        selected = all_problems
    else:
        selected = random.sample(all_problems, count)
    # 保留完整解答在 full_body，body 只含题目（不含答案）
    for p in selected:
        full = p["body"]
        p["full_body"] = full  # 完整内容（含解答）
        p["body"] = re.sub(r'\*\*答案\*\*[\s\S]*', '', p["body"])
        p["body"] = re.sub(r'\*\*步骤\*\*[\s\S]*', '', p["body"])
        # 统一 LaTeX 分隔符：\(...\) → $...$ ，\[...\] → $$...$$
        for key in ["body", "full_body"]:
            # 先保护数学公式
            math_parts = []
            def protect(m):
                math_parts.append(m.group(0))
                return f'@@@MATH_{len(math_parts)-1}@@@'
            p[key] = re.sub(r'\\\[(.+?)\\\]', protect, p[key], flags=re.DOTALL)
            p[key] = re.sub(r'\\\((.+?)\\\)', protect, p[key])
            # Markdown → HTML
            p[key] = md_to_html(p[key], extensions=["fenced_code", "tables"])
            # 外链在新标签页打开
            p[key] = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', p[key])
            # 还原数学公式为 $ / $$ 分隔符
            for i, part in enumerate(math_parts):
                if part.startswith("\\["):
                    cooked = "$$" + part[2:-2].strip() + "$$"
                else:
                    cooked = "$" + part[2:-2].strip() + "$"
                p[key] = p[key].replace(f"@@@MATH_{i}@@@", cooked)
    return {"problems": selected}


@app.route("/api/quiz/answer/<int:idx>")
def api_quiz_answer(idx: int):
    """返回指定题目的完整解答"""
    # 简化：返回索引对应的题目解答
    all_problems = parse_quiz_problems()
    if 0 <= idx < len(all_problems):
        return {"answer": all_problems[idx]["body"]}
    return {"answer": "未找到"}


# ── 诊断 ─────────────────────────────────────────────────

@app.route("/api/diagnosis")
def api_diagnosis():
    stats = get_wrong_stats()
    total = stats["total"]
    if total == 0:
        return {"has_data": False}

    counts = stats["counts"]
    max_subj = max(counts, key=counts.get)

    suggestions = {
        "复变函数": ["重点复习 C-R 方程和解析性判断", "多练 Cauchy 积分公式和留数计算", "共形映射的 Möbius 变换构造"],
        "抽象代数": ["重点复习 Sylow 定理的计数应用", "多练正规子群和商群的证明", "Eisenstein 判别法和不可约性判断"],
        "运筹学": ["按老师核心考点复习：单纯形→对偶→互补松弛→灵敏度", "整数规划建模、分支定界、割平面按大题模板刷", "图与网络重点放最短路径和最大流，其他章节只做备用查漏"],
        "数据结构 C": ["按严蔚敏《数据结构（C语言版）》第2版主线复习", "重点练链表、循环队列、KMP next、树图查找排序", "多做 ASL、AVL/B 树、哈夫曼和排序稳定性题"],
        "英语四六级": ["重点背核心高频词汇（听力和阅读复现率最高）", "每天精听 30 分钟 + 真题听力训练", "写作三段式模板背诵 + 翻译拆分法练习"],
    }

    return {
        "has_data": True,
        "total": total,
        "counts": counts,
        "max_subject": max_subj,
        "max_icon": SUBJECTS.get(
            [k for k, v in QUIZ_SUBJECT_MAP.items() if v == max_subj][0]
            if max_subj in QUIZ_SUBJECT_MAP.values() else "",
            {"icon": "📚"}
        )["icon"] if isinstance(SUBJECTS.get("", {}), dict) else "📚",
        "suggestions": suggestions.get(max_subj, []),
        "quick_links": {
            "复变函数": "/subject/complex-analysis",
            "抽象代数": "/subject/abstract-algebra",
            "运筹学": "/subject/operations-research",
            "数据结构 C": "/subject/data-structures-c",
            "英语四六级": "/subject/english-cet",
        },
    }


# ── 闪卡 ─────────────────────────────────────────────────

FLASHCARDS = {
    "complex-analysis": [
        {"front": "什么是解析函数？", "back": "函数 $f(z)$ 在区域 $D$ 内每一点都可导，则称 $f(z)$ 在 $D$ 内解析。注意：仅一点可导不等于解析，需要邻域条件。"},
        {"front": "Cauchy-Riemann 方程", "back": "若 $f(z)=u+iv$ 解析，则 $u_x=v_y,\\ u_y=-v_x$。若 $u,v$ 一阶偏导连续且满足 C-R 方程，则 $f(z)$ 解析。"},
        {"front": "调和函数", "back": "满足 Laplace 方程 $u_{xx}+u_{yy}=0$ 的函数。解析函数的实部和虚部都是调和函数，且互为共轭调和函数。"},
        {"front": "Cauchy 积分定理", "back": "若 $f$ 在单连通区域 $D$ 内解析，则对 $D$ 内任意闭曲线 $C$，$\\oint_C f(z)dz=0$。条件关键词：解析、闭路、单连通、区域内无奇点。"},
        {"front": "Cauchy 积分公式", "back": "$f(z_0)=\\frac{1}{2\\pi i}\\oint_C\\frac{f(z)}{z-z_0}dz$。高阶：$f^{(n)}(z_0)=\\frac{n!}{2\\pi i}\\oint_C\\frac{f(z)}{(z-z_0)^{n+1}}dz$。"},
        {"front": "留数（Residue）定义", "back": "Laurent 展开中 $(z-z_0)^{-1}$ 的系数 $c_{-1}$ 就是留数。留数定理：$\\oint_C f(z)dz=2\\pi i\\sum\\operatorname{Res}(f,z_k)$。"},
        {"front": "一阶极点留数公式", "back": "$\\operatorname{Res}(f,z_0)=\\lim_{z\\to z_0}(z-z_0)f(z)$。m 阶：$\\operatorname{Res}(f,z_0)=\\frac{1}{(m-1)!}\\lim_{z\\to z_0}\\frac{d^{m-1}}{dz^{m-1}}[(z-z_0)^mf(z)]$。"},
        {"front": "孤立奇点三种类型", "back": "可去奇点（Laurent 无负幂）、极点（负幂有限项，m 阶）、本性奇点（负幂无限多项）。"},
        {"front": "最大模原理", "back": "非常值解析函数在区域内部不能取得最大模。推论：最大模必在边界上达到。"},
        {"front": "Liouville 定理", "back": "全平面有界的整函数必为常数。常用于证明代数学基本定理。"},
        {"front": "Taylor 展开公式", "back": "$f(z)=\\sum_{n=0}^{\\infty}\\frac{f^{(n)}(z_0)}{n!}(z-z_0)^n$，收敛半径 $R$ 为 $z_0$ 到最近奇点的距离。"},
        {"front": "Laurent 级数适用域", "back": "圆环域 $r<|z-z_0|<R$。展开式 $f(z)=\\sum_{n=-\\infty}^{\\infty}c_n(z-z_0)^n$。注意写清适用环域！"},
        {"front": "Rouché 定理", "back": "在闭曲线 $C$ 上若 $|f(z)|>|g(z)|$，则 $f$ 与 $f+g$ 在 $C$ 内零点数相同。"},
        {"front": "辐角原理", "back": "$\\frac{1}{2\\pi i}\\oint_C\\frac{f'(z)}{f(z)}dz=N-P$，其中 $N$=零点数，$P$=极点数（均计重数）。"},
        {"front": "Möbius 变换", "back": "$w=\\frac{az+b}{cz+d},\\ ad-bc\\neq0$。保圆性、保交比性、保对称性。上半平面→单位圆盘：$w=e^{i\\theta}\\frac{z-z_0}{z-\\overline{z_0}}$。"},
        {"front": "共形映射条件", "back": "$f(z)$ 在区域 $D$ 内单叶解析且 $f'(z)\\neq0$。导数的几何意义：$|f'(z_0)|$=伸缩率，$\\arg f'(z_0)$=旋转角。"},
        {"front": "实积分三大类型", "back": "① $\\int_0^{2\\pi}R(\\cos,\\sin)d\\theta$→$z=e^{i\\theta}$ 代换 ② $\\int_{-\\infty}^\\infty\\frac{P}{Q}dx$→上半平面留数(需 $\\deg Q\\ge\\deg P+2$) ③ $\\int_{-\\infty}^\\infty\\frac{P}{Q}e^{imx}dx$→Jordan 引理"},
        {"front": "$e^z$ 的 Taylor 展开", "back": "$e^z=1+z+\\frac{z^2}{2!}+\\frac{z^3}{3!}+\\cdots=\\sum_{n=0}^{\\infty}\\frac{z^n}{n!}$，收敛半径 $\\infty$。"},
        {"front": "$\\frac{1}{1-z}$ 的几何级数", "back": "$\\frac{1}{1-z}=1+z+z^2+z^3+\\cdots=\\sum_{n=0}^{\\infty}z^n,\\ |z|<1$。这是 Laurent 展开的基础。"},
        {"front": "解析函数与可导的区别", "back": "可导 = 在单个点导数存在。解析 = 在某邻域内处处可导。$f(z)=|z|^2$ 在 $z=0$ 可导但不解析。"},
    ],
    "abstract-algebra": [
        {"front": "群的定义（四个条件）", "back": "非空集合 $G$ 和二元运算 $*$ 满足：封闭性、结合律、单位元 $e$、逆元。缺一不可。"},
        {"front": "子群判别法", "back": "$H\\le G$ 当且仅当 $H\\neq\\varnothing$ 且 $\\forall a,b\\in H,\\ ab^{-1}\\in H$。有限子集：非空且对运算封闭即可。"},
        {"front": "Lagrange 定理", "back": "若 $G$ 是有限群，$H\\le G$，则 $|H|$ 整除 $|G|$。推论：元素的阶整除群的阶。"},
        {"front": "正规子群", "back": "$N\\trianglelefteq G$ 当且仅当 $\\forall g\\in G,\\ gNg^{-1}=N$（共轭封闭）。等价地 $gN=Ng$（左右陪集相等）。阿贝尔群的任意子群都正规。"},
        {"front": "商群构造", "back": "若 $N\\trianglelefteq G$，则 $G/N=\\{gN:g\\in G\\}$ 构成群。运算：$(aN)(bN)=abN$。要求正规子群！"},
        {"front": "群同态与核", "back": "同态 $\\varphi:G\\to G'$ 满足 $\\varphi(ab)=\\varphi(a)\\varphi(b)$。核 $\\ker\\varphi=\\{g:\\varphi(g)=e'\\}$ 是正规子群。像 $\\operatorname{Im}\\varphi\\le G'$。"},
        {"front": "第一同构定理", "back": "$G/\\ker\\varphi\\cong\\operatorname{Im}\\varphi$。这是群论最重要的结构定理。"},
        {"front": "循环群", "back": "由一个元素生成的群 $G=\\langle a\\rangle$。有限循环群的子群也是循环群。$\\mathbb Z_n$ 的生成元个数为 $\\varphi(n)$。"},
        {"front": "Sylow 第一定理", "back": "若 $|G|=p^a\\cdot m$（$p\\nmid m$），则对每个 $1\\le k\\le a$，$G$ 存在 $p^k$ 阶子群。特别有 $p^a$ 阶 Sylow $p$-子群。"},
        {"front": "Sylow 第三定理（计数）", "back": "$n_p\\equiv1\\pmod{p}$ 且 $n_p\\mid m$（其中 $|G|=p^am,\\ p\\nmid m$）。$n_p=[G:N_G(P)]$。"},
        {"front": "环的定义", "back": "集合 $R$ 对加法构成阿贝尔群、乘法满足结合律、乘法对加法满足左右分配律。不要求乘法交换、不要求有单位元。"},
        {"front": "理想", "back": "加法子群 $I\\subseteq R$，对任意 $r\\in R,a\\in I$ 有 $ra\\in I$（左理想）且 $ar\\in I$（右理想）。交换环中只需写一个方向。"},
        {"front": "素理想与最大理想", "back": "$P$ 素理想 $\\iff R/P$ 是整环。$M$ 最大理想 $\\iff R/M$ 是域。最大理想必为素理想。"},
        {"front": "Eisenstein 判别法", "back": "存在素数 $p$：$p\\mid a_0,\\dots,a_{n-1}$，$p\\nmid a_n$，$p^2\\nmid a_0$，则多项式在 $\\mathbb Q$ 上不可约。"},
        {"front": "域的定义", "back": "至少两个元素的交换环，每个非零元都有乘法逆元。域一定是整环。有限整环必为域。"},
        {"front": "$\\mathbb Z_n$ 是域的条件", "back": "$\\mathbb Z_n$ 是域当且仅当 $n$ 为素数。$\\mathbb Z_n$ 中 $[a]$ 可逆当且仅当 $\\gcd(a,n)=1$。"},
        {"front": "类方程", "back": "$|G|=|Z(G)|+\\sum_{i=1}^r[G:C_G(g_i)]$。用于证明 $p$-群有非平凡中心。"},
        {"front": "轨道-稳定子定理", "back": "$|G\\cdot x|=[G:G_x]=\\frac{|G|}{|G_x|}$。轨道大小等于稳定子的指数。"},
        {"front": "有限域阶", "back": "有限域的阶必为素数幂 $p^n$。对每个 $p^n$，存在唯一的 $p^n$ 阶域（同构意义下），记为 $\\mathbb F_{p^n}$。乘法群 $\\mathbb F_{p^n}^\\times$ 是循环群。"},
        {"front": "交换环中理想与商环", "back": "若 $I$ 是环 $R$ 的理想，则 $R/I$ 构成环。商环的元素是加法陪集。"},
    ],
    "operations-research": [
        {"front": "教材版本与本次核心", "back": "用户教材：《运筹学》第五版，清华大学出版社。老师核心考点：单纯形法、对偶理论、互补松弛、灵敏度分析、整数规划建模、分支定界、割平面、最短路径、最大流。"},
        {"front": "运筹学核心大题优先级", "back": "1单纯形法 2对偶理论 3互补松弛 4灵敏度分析 5整数规划建模 6分支定界 7割平面 8最短路径 9最大流。其他章节放最后查漏。"},
        {"front": "绪论建模流程", "back": "实际问题→明确目标→设决策变量→写目标函数和约束→求解→检验解释→实施修正。简答题要写出模型思想。"},
        {"front": "线性规划建模答题模板", "back": "写清变量含义和单位→目标函数→资源/需求/比例/逻辑约束→非负/整数/0-1 条件→必要时化标准型。文字题不能只列式不解释变量。"},
        {"front": "线性规划三要素", "back": "决策变量、目标函数、约束条件。建模步骤：设变量→写目标→列约束→非负。"},
        {"front": "单纯形法核心思想", "back": "从一个基本可行解出发，沿相邻顶点改善目标值，直到检验数满足最优性条件。入基选最大正检验数，出基用最小比值检验（只看正主元列元素）。"},
        {"front": "单纯形表必须写什么", "back": "每轮都写：基变量、目标系数、技术系数、RHS、检验数、入基列、出基行、主元。最后读出非基变量为 0，基变量等于 RHS。"},
        {"front": "单纯形最小比值", "back": "只对入基列中正数计算 RHS/列系数，取最小正比值对应的行出基。作用：保证换基后 RHS 仍非负。"},
        {"front": "单纯形最优/无界/多解", "back": "最优：检验数满足最优条件；无界：某可改进列所有系数 <=0；多重最优：最优表中非基变量检验数为 0。"},
        {"front": "对偶问题转换规则", "back": "max→min，约束 $\\le$→对偶变量 $\\ge0$，系数矩阵转置，右端项与目标系数互换。强对偶：原问题与对偶最优目标值相等。"},
        {"front": "对偶题先数什么", "back": "原约束数=对偶变量数；原变量数=对偶约束数。写对偶时先数个数，再处理 max/min、<=/>=、变量符号。"},
        {"front": "互补松弛条件", "back": "$y_i(b_i-A_ix)=0$，$x_j((A^Ty)_j-c_j)=0$。用于已知一问题的最优解求另一问题。"},
        {"front": "互补松弛人话版", "back": "原约束有剩余量 => 对应 y_i=0；x_j>0 => 第 j 条对偶约束取等号。最后用 w*=z* 验证。"},
        {"front": "灵敏度分析关注什么", "back": "目标系数 $c_j$ 变化、右端项 $b_i$ 变化、增加变量或约束。可行性看右端项，最优性看检验数。"},
        {"front": "灵敏度两条主线", "back": "目标系数变化：看检验数是否仍满足最优条件；右端项变化：看当前基变量 RHS 是否仍非负。不要混用。"},
        {"front": "线性目标规划偏差变量", "back": "目标约束写成“实际达到值 + d^- - d^+ = 目标值”。不低于目标看 \(d^-\)，不超过目标看 \(d^+\)，尽量等于看 \(d^-+d^+\)。"},
        {"front": "运输/指派大题入口", "back": "运输题先看供需是否平衡，不平衡补虚拟行列；基变量数必须是 $m+n-1$。指派题用匈牙利法，最大化先转最小化。"},
        {"front": "运输问题基变量个数", "back": "$m+n-1$（$m$ 个产地 + $n$ 个销地）。退化时需要补零基变量。不平衡时需加虚拟产地/销地。"},
        {"front": "匈牙利法步骤", "back": "① 行归约（每行减行最小）② 列归约（每列减列最小）③ 最少直线覆盖所有零 ④ 直线数=n→最优；否则调整矩阵继续。"},
        {"front": "整数规划与 0-1 建模", "back": "分支定界：先解松弛 LP，非整数变量分成 $x_i\\le k$ 与 $x_i\\ge k+1$。0-1 变量常表示是否选择、是否启用、是否走某路径。"},
        {"front": "0-1 逻辑约束速记", "back": "至少一个：sum x>=1；至多一个：sum x<=1；恰好一个：sum x=1；A=>B：x_A<=x_B；A、B 不能同选：x_A+x_B<=1。"},
        {"front": "非线性规划答题顺序", "back": "无约束先令梯度为 0；等式约束用 Lagrange；不等式约束统一成 \(g_i(x)\\le0\)，再写 K-T 条件。"},
        {"front": "动态规划四要素", "back": "阶段、状态、决策、状态转移方程。必须加边界条件！建模时先划分阶段，再定义状态变量（需包含未来决策全部信息）。"},
        {"front": "Bellman 最优性原理", "back": "无论初始状态和初始决策如何，余下的决策必构成从当前状态出发的最优策略。递推公式：$f_k(s)=\\operatorname{opt}_{u_k}\\{v_k(s,u_k)+f_{k+1}(s')\\}$。"},
        {"front": "图与网络题型", "back": "最短路用 Dijkstra/Floyd，最小生成树用 Prim/Kruskal，最大流用增广路并用最小割验证。"},
        {"front": "网络计划题型", "back": "PERT/CPM：根据紧前关系画网络图，正推 ET/EF，逆推 LT/LS，算总时差 TF，TF=0 为关键路线。"},
        {"front": "M/M/1 模型核心公式", "back": "$\\rho=\\lambda/\\mu<1$。$L_s=\\frac{\\rho}{1-\\rho}$，$L_q=\\frac{\\rho^2}{1-\\rho}$，$W_s=\\frac{1}{\\mu-\\lambda}$，$W_q=\\frac{\\rho}{\\mu-\\lambda}$。Little 公式：$L_s=\\lambda W_s$。"},
        {"front": "排队系统 Kendall 记号", "back": "$A/B/C/K/m$：A=到达分布(M=Poisson)、B=服务分布、C=服务台数、K=系统容量、m=顾客源。最常用 M/M/1。"},
        {"front": "EOQ 最优订货量公式", "back": "$Q^*=\\sqrt{\\frac{2C_3R}{C_1}}$。$R$=需求率，$C_1$=单位存储费，$C_3$=一次订购费。最优周期 $t^*=Q^*/R$，最低总费用 $C^*=\\sqrt{2C_1C_3R}$。"},
        {"front": "排队/存储/对策判断顺序", "back": "排队先判到达率、服务率和 $\\rho<1$；存储先判是否缺货、是否生产需时间；对策先找鞍点，无鞍点再优超化简和混合策略。"},
        {"front": "二人零和对策鞍点条件", "back": "$\\max_i\\min_j a_{ij}=\\min_j\\max_i a_{ij}=V$ 时存在纯策略鞍点。不等则需混合策略。"},
        {"front": "决策分析五种准则", "back": "悲观(max-min)、乐观(max-max)、乐观系数(Hurwicz: $\\alpha\\max+(1-\\alpha)\\min$)、最小后悔值(min-max regret)、等可能(Laplace)。风险型用期望值和决策树。"},
        {"front": "决策树折算", "back": "方块是决策点，圆点是机会点。先在机会点按概率算期望值，再在决策点选择最大收益或最小损失，从右往左折算。"},
        {"front": "非线性规划 K-T 条件", "back": "标准化为 $g_i(x)\\le0$，写驻点方程、可行性、互补松弛 $u_i g_i(x)=0$、乘子非负。凸规划中 K-T 常可作为充分必要条件。"},
        {"front": "图解法步骤", "back": "二变量题：画约束边界→确定可行域→列所有顶点→代入目标函数→比较最优值。顶点必须逐个检查可行性。"},
        {"front": "运输问题位势法", "back": "基变量满足 $u_i+v_j=c_{ij}$，非基变量检验数 $\\sigma_{ij}=c_{ij}-(u_i+v_j)$。最小化题若有负检验数则还能改进。"},
        {"front": "网络计划关键路线", "back": "正推最早时间 $ET$，逆推最迟时间 $LT$，总时差 $TF=LS-ES=LF-EF$。总时差为 0 的活动在关键路线上。"},
        {"front": "决策论后悔值", "back": "每个自然状态先找最好收益，再用最好收益减该方案收益形成后悔矩阵；每个方案取最大后悔值，选最大后悔值最小者。"},
        {"front": "最大流增广路", "back": "增广路上正向边看剩余容量，反向边看可退流量；每次增广量取路径最小剩余容量，直到无增广路。"},
        {"front": "K-T 互补松弛", "back": "$u_i g_i(x)=0$ 表示：约束不紧则乘子为 0，乘子为正则约束必须取等号。解题常按活跃约束分情况。"},
        {"front": "建模题卷面得分点", "back": "必须写：变量含义和单位、目标函数、约束来源、非负/整数/0-1 条件。最后用“故模型为...”收束。"},
        {"front": "单纯形题卷面得分点", "back": "每轮写入基列、出基行、主元、最小比值和检验数。最终写“非基变量为0，基变量取RHS”。"},
        {"front": "运输题卷面得分点", "back": "先判供需是否平衡；写初始方案；检查基变量数 $m+n-1$；位势法算检验数；闭回路调整；最后算总费用。"},
        {"front": "动态规划题卷面得分点", "back": "五件套：阶段、状态、决策、状态转移、边界条件。最后写最优值并反推最优策略。"},
        {"front": "排队题单位陷阱", "back": "先统一单位。平均10分钟到达1人是 $\\lambda=1/10$ 人/分钟，不是 10；平均服务8分钟是 $\\mu=1/8$ 人/分钟。"},
        {"front": "博弈鞍点判断", "back": "先算行最小再取最大 \(V_L\)，再算列最大再取最小 \(V_U\)。若相等，有鞍点；不等，再考虑混合策略。"},
        {"front": "最小生成树算法", "back": "Kruskal：按边权从小到大选，不成环。Prim：从点集出发，每次选连接外部的最小边。"},
        {"front": "Dijkstra 算法条件", "back": "所有边权非负。标号法：永久标号（已确定最短距离）和临时标号。每次选临时标号中最小的变为永久。"},
        {"front": "最大流-最小割定理", "back": "网络中最大流的值等于最小割的容量。Ford-Fulkerson 方法：不断找增广路（正向非饱和、反向非零流）。"},
        {"front": "分支定界法（整数规划）", "back": "先求松弛问题（去掉整数约束），若最优解非整数则分支（如 $x_i\\le k$ 和 $x_i\\ge k+1$），剪枝条件：不可行或无更优解。"},
        {"front": "分支定界剪枝条件", "back": "剪枝三类：子问题不可行；松弛界不可能优于当前最好整数解；松弛解已是整数解。最大化中 LP 松弛值是上界。"},
        {"front": "割平面法核心", "back": "从 LP 松弛最优表中选 RHS 非整数的行，用小数部分构造 Gomory 割。割要切掉当前非整数解，但不能切掉任何整数可行解。"},
        {"front": "Gomory 割小数部分", "back": "小数部分 {r}=r-floor(r)。例如 {1/2}=1/2，{-1/4}=3/4。常见割：sum {a_j}x_j >= {b}。"},
        {"front": "Dijkstra 卷面写法", "back": "写初始化 d、永久标号顺序、每轮临时距离更新、前驱点，最后给最短距离和路径。只写答案容易丢过程分。"},
        {"front": "最大流卷面写法", "back": "每次写增广路、瓶颈容量、累计流量；更新残量网络。最后找一个容量等于当前流量的割来证明最大。"},
        {"front": "单纯形法无界解判别", "back": "若某非基变量的检验数为正且该列所有技术系数 $\\le 0$，则目标函数无界（max 问题）。"},
        {"front": "运输问题初始方案方法", "back": "西北角法（最简单）、最小元素法（贪心最小运费）、Vogel 近似法（考虑次小与最小之差，效果最好）。"},
    ],
    "english-cet": [
        {"front": "四级总分和及格线？", "back": "总分 710，及格线 425。题型：写作 15%、听力 35%、阅读 35%、翻译 15%。"},
        {"front": "听力最重要的技巧？", "back": "逻辑词定位法：but/however/because 后面的信息 90% 是答案。听前扫读选项，预判话题。"},
        {"front": "选词填空三步法", "back": "① 标词性(n./v./adj./adv.) ② 读空前后的语法信号 ③ 语义筛选匹配"},
        {"front": "长篇阅读匹配技巧", "back": "扫读 10 个题干关键词 → 逐段看首末句+转折词后 → 关键词 ≥2 个匹配 → 选定。不要逐句精读！"},
        {"front": "仔细阅读解题原则", "back": "题文同序原则：题目顺序 = 原文段落顺序。先读题干 → 定位原文 → 比对选项 → 排除干扰项。"},
        {"front": "写作三段式模板", "back": "引言段(现象+观点) → 主体段(论点+举例+分析) → 结尾段(总结+升华)。用升级词汇替换基础词汇。"},
        {"front": "翻译核心技巧", "back": "拆分法：长难中文拆成 2-3 个简单英文句。先译主干，再补修饰。直译+意译结合，避免中式英语。"},
        {"front": "常见听力逻辑词有哪些？", "back": "转折：but, however, in fact, actually。因果：because, as a result, therefore。强调：especially, the key is。"},
        {"front": "常见干扰项陷阱", "back": "偷换概念(原文 some → 选项 all)、反向干扰(支持变反对)、张冠李戴(把 A 的特点放 B 身上)。"},
        {"front": "四级听力题型结构", "back": "短篇新闻 3篇7题 + 长对话 2篇8题 + 短文理解 3篇10题。共 25 题，35% 分值。"},
        {"front": "六级听力题型结构", "back": "长对话 2篇8题 + 短文理解 2篇7题 + 讲座/讲话 3篇10题。共 25 题，语速 150 词/分钟。"},
        {"front": "阅读中高频学术词汇", "back": "ubiquitous(普遍的)、ameliorate(改善)、sustainable(可持续的)、controversial(有争议的)、exacerbate(加剧)。"},
        {"front": "词汇升级：important → ？", "back": "indispensable, pivotal, vital, crucial, essential, significant。写作中用升级词汇提分。"},
        {"front": "词汇升级：many → ？", "back": "a multitude of, numerous, an increasing number of, a variety of, a host of。"},
        {"front": "avoid 中式英语", "back": "学习知识 → acquire/gain knowledge(不是 learn knowledge)；开会 → hold/host a meeting(不是 open a meeting)。"},
        {"front": "四级备考时间规划", "back": "基础 3-4周(词汇+听力+语法) → 强化 3-4周(真题+错题+专项) → 冲刺 2周(模拟+限时+模板)。"},
        {"front": "2024-2025 翻译高频主题", "back": "传统文化(二十四节气、京剧)、科技成就(北斗、高铁)、社会发展(乡村振兴、社区养老、数字经济)。"},
        {"front": "何时用被动语态？", "back": "中文无主语句子 → 英文用被动：\"应该采取措施\" → \"Measures should be taken\"。"},
        {"front": "四级常用衔接词", "back": "First and foremost / Moreover / Furthermore / In addition / However / Nevertheless / In conclusion / To sum up。"},
        {"front": "听力同义替换：postpone", "back": "put off / delay / defer。听力中常以同义替换形式出现，听到 postpone 但选项写 put off。"},
    ],
    "data-structures-c": [
        {"front": "周一笔试十道大题分布", "back": "按这 10 类准备：线性表代码、栈队列、KMP、数组/广义表、二叉树、哈夫曼/AVL/B树、图、查找ASL、内部排序、综合算法分析。"},
        {"front": "十道大题时间分配", "back": "90-100 分钟卷：先扫题 5 分钟；每题约 8-9 分钟；最后 5-10 分钟查下标、队满条件、ASL 分母、排序稳定性。"},
        {"front": "代码大题答题模板", "back": "算法思想→核心代码→边界情况→复杂度。链表题必写空表、删头、连续删除、free；队列题必写判空判满。"},
        {"front": "计算大题答题模板", "back": "先写规则/公式，再列表或画过程，最后写结论。ASL、WPL、Dijkstra、拓扑、排序每趟都要保留中间过程。"},
        {"front": "教材主线（严蔚敏 C 版第2版）", "back": "线性表→栈和队列→串→数组/广义表→树和二叉树→图→查找→内部排序。红黑树、Trie、跳表、外部排序先按选学/了解。"},
        {"front": "顺序表 vs 链表", "back": "顺序表：随机访问 $O(1)$，插入删除 $O(n)$。链表：不能随机访问，插入删除 $O(1)$（已知位置）。顺序表连续内存，链表不连续。"},
        {"front": "单链表删除边界情况", "back": "必须考虑：空链表、删头结点（需改 head）、找不到、仅一个结点、删后 free 且不再访问。"},
        {"front": "栈的特点", "back": "后进先出(LIFO)。应用：括号匹配、表达式求值、递归模拟、DFS。顺序栈 top 初始=-1。"},
        {"front": "循环队列判空判满", "back": "牺牲一个单元：空=$front=rear$，满=$(rear+1)\\bmod MAXSIZE=front$。元素个数=$(rear-front+MAXSIZE)\\bmod MAXSIZE$。"},
        {"front": "数组行优先地址", "back": "0-based: $LOC(A[i][j])=base+(i\\cdot n+j)L$。1-based: $LOC(A[i][j])=base+((i-1)n+(j-1))L$。"},
        {"front": "稀疏矩阵三元组", "back": "三元组记录 $(row, col, value)$。快速转置常先统计每列非零元个数，再确定新表起始位置。"},
        {"front": "二叉树遍历口诀", "back": "先序：根左右。中序：左根右。后序：左右根。层序：用队列 BFS。中序+先序或中序+后序可唯一确定二叉树。"},
        {"front": "二叉搜索树(BST)", "back": "左子树<根<右子树。中序遍历得到递增序列。查找/插入平均 $O(\\log n)$，最坏 $O(n)$（退化为链表）。"},
        {"front": "二叉树性质", "back": "$n_0=n_2+1$（叶子数=度为2的结点数+1）。第 i 层最多 $2^{i-1}$ 个。深度 k 最多 $2^k-1$ 个。完全二叉树深 $\\lfloor\\log_2 n\\rfloor+1$。"},
        {"front": "AVL 树四种旋转", "back": "LL→右单旋，RR→左单旋，LR→先左旋左子树再右旋根，RL→先右旋右子树再左旋根。平衡因子=左高-右高∈{-1,0,1}。"},
        {"front": "B 树（m 阶）性质", "back": "每结点最多 m 个子树、m-1 个关键字。非根非叶至少 $\\lceil m/2\\rceil$ 个子树。所有叶在同一层。3阶B树每结点最多2个关键字。"},
        {"front": "哈夫曼树构造", "back": "贪心：每次选两个最小权值合并。WPL=$\\sum w_i\\cdot l_i$ 最小。无度为 1 的结点。哈夫曼编码是最优前缀编码。"},
        {"front": "拓扑排序算法", "back": "计算入度→入度为0的入栈→出栈输出→邻接点入度减1→入度为0则入栈→输出数<顶点数则有回路。$O(n+e)$。"},
        {"front": "KMP next 数组公式", "back": "$next[1]=0$（下标从1开始）。$next[j]$=前 $j-1$ 个字符的最长相等前后缀长度 +1。失配时模式串跳转到 next[j] 继续匹配。$O(m+n)$。"},
        {"front": "排序稳定性速记", "back": "稳定：冒泡、插入、归并、基数。不稳定：选择、快速、堆、希尔。原因：是否会跨越交换相同关键字。"},
        {"front": "快速排序时间复杂度", "back": "平均 $O(n\\log n)$，最坏 $O(n^2)$（已有序或逆序且 pivot 选得差）。空间 $O(\\log n)$（递归栈）。不稳定。"},
        {"front": "图的存储方式比较", "back": "邻接矩阵：空间 $O(n^2)$，适合稠密图和快速判边。邻接表：空间 $O(n+e)$，适合稀疏图。"},
        {"front": "DFS vs BFS", "back": "DFS 用栈/递归，一条路走到底再回溯。BFS 用队列，一层一层访问。DFS 适合路径查找，BFS 适合最短路径（无权图）。"},
        {"front": "哈希冲突处理方法", "back": "开放定址法（线性探测、二次探测、双散列）、链地址法（链表挂在槽上）。装填因子 $\\alpha$ 影响查找效率。"},
        {"front": "二分查找前提", "back": "顺序存储（数组）+ 有序。时间复杂度 $O(\\log n)$。mid 计算用 $left+(right-left)/2$ 防溢出。"},
        {"front": "查找 ASL", "back": "ASL=各关键字查找长度的平均值。折半查找看判定树层数，哈希线性探测从第一次探测开始计数。"},
        {"front": "哈希 ASL 检查点", "back": "成功 ASL：按每个已存关键字从 H(k) 探测到实际位置的次数平均。失败 ASL：从每个散列地址探测到第一个空位的次数平均。"},
        {"front": "AVL/B 树笔试过程分", "back": "AVL 写清 LL/RR/LR/RL 和旋转对象；B树写清几阶、每结点最多几个关键字、哪一个关键字上提、分裂后的左右结点。"},
        {"front": "堆排序特点", "back": "不稳定，$O(n\\log n)$，原地排序。大根堆→升序。建堆 $O(n)$，每次调整 $O(\\log n)$。"},
        {"front": "归并排序特点", "back": "稳定，$O(n\\log n)$ 时间，$O(n)$ 额外空间。分治法：递归划分→合并有序子序列。外部排序放到选学/了解。"},
    ],
}

@app.route("/flashcards")
def flashcards_page():
    subject = request.args.get("subject", "")
    return render_template("flashcards.html", subjects=SUBJECTS, subject_filter=subject)


@app.route("/api/flashcards/<subject_key>")
def api_flashcards(subject_key):
    cards = FLASHCARDS.get(subject_key, [])
    return {"cards": cards, "total": len(cards)}


# ── AI 问答 ────────────────────────────────────────────────

@app.route("/ask")
def ask_page():
    return render_template("ask.html", subjects=SUBJECTS)


@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return {"answer": "请提出你的问题。", "links": []}

    # 在所有知识点文件中搜索相关内容
    all_hits = []
    for key, info in SUBJECTS.items():
        text = read_md(info["file"])
        # 直接全文匹配，提取匹配位置附近的上下文
        qlower = question.lower()
        tlower = text.lower()
        # 提取问题中的关键词（2-6 字中文子串 + 英文单词）
        keywords = set()
        for i in range(len(question)):
            for j in range(i+2, min(i+7, len(question)+1)):
                kw = question[i:j].lower().strip()
                if len(kw) >= 2 and not kw.isspace():
                    keywords.add(kw)
        for word in qlower.split():
            if len(word) >= 2:
                keywords.add(word)

        # 对每个关键词找到匹配位置
        match_positions = []
        for kw in keywords:
            idx = 0
            while True:
                idx = tlower.find(kw, idx)
                if idx == -1:
                    break
                match_positions.append(idx)
                idx += 1

        if not match_positions:
            continue

        # 合并相近的匹配位置
        match_positions.sort()
        clusters = []
        for pos in match_positions:
            if not clusters or pos - clusters[-1][-1] > 300:
                clusters.append([pos])
            else:
                clusters[-1].append(pos)

        # 每簇提取一个结果
        for cluster in clusters[:5]:
            center = cluster[len(cluster)//2]
            start = max(0, center - 100)
            end = min(len(text), center + 400)
            snippet = text[start:end].strip()
            # 找最近的标题
            before = text[:center]
            headings = re.findall(r'^##\s+(.+)$', before, re.MULTILINE)
            heading = headings[-1] if headings else "知识点"
            # 计分
            score = sum(text[max(0,pos-50):pos+50].lower().count(kw) for pos in cluster for kw in keywords)
            all_hits.append({"score": score, "heading": heading.strip(), "text": snippet, "subject": info["name"], "icon": info["icon"], "key": key})

    all_hits.sort(key=lambda x: x["score"], reverse=True)
    top = all_hits[:3]

    if not top:
        return {"answer": "抱歉，未找到与「" + question + "」直接相关的内容。请尝试更具体的关键词或查阅知识点页面。", "links": []}

    # 合成回答
    answer = ""
    links = []
    for i, chunk in enumerate(top):
        # 提取关键公式/定义
        formulas = re.findall(r'\$[^$]+\$|\$\$[^$]+\$\$', chunk["text"])
        formula_text = " ".join(formulas[:3]) if formulas else ""
        answer += f"\n\n**{chunk['icon']} [{chunk['subject']}] {chunk['heading']}**\n\n"
        snippet = chunk["text"][:300].strip()
        # 清理 markdown 符号
        snippet = re.sub(r'#{1,4}\s*', '', snippet)
        answer += snippet + ("..." if len(chunk["text"]) > 300 else "")
        if formula_text:
            answer += f"\n\n> 相关公式：{formula_text}"
        links.append({"text": f"{chunk['icon']} {chunk['subject']} - {chunk['heading']}", "url": f"/subject/{chunk['key']}"})

    return {"answer": answer.strip(), "links": links, "question": question}


# ── 仪表盘数据 ──────────────────────────────────────────

@app.route("/api/dashboard")
def api_dashboard():
    stats = get_wrong_stats()
    problems = parse_quiz_problems()

    # 各科可用题目数
    quiz_counts = {}
    for sn in QUIZ_SUBJECT_MAP.values():
        quiz_counts[sn] = len([p for p in problems if p["subject"] == sn])

    return {
        "wrong_total": stats["total"],
        "wrong_counts": stats["counts"],
        "quiz_total": len(problems),
        "quiz_counts": quiz_counts,
        "flashcard_total": sum(len(v) for v in FLASHCARDS.values()),
    }


# ── 视频资源 ──────────────────────────────────────────────

@app.route("/videos")
def videos_page():
    content = md_content("video-resources.md")
    return render_template("videos.html", content=content, subjects=SUBJECTS)


# ── 学习追踪 ──────────────────────────────────────────────

@app.route("/progress")
def progress_page():
    return render_template("progress.html", subjects=SUBJECTS)


# ── 聚合洞察 API（智能版）──────────────────────────────────

@app.route("/api/insights")
def api_insights():
    """智能学习诊断：综合错题+测验+闪卡+路径，给出学习评分和自适应建议"""
    stats = get_wrong_stats()
    problems = parse_quiz_problems()
    counts = stats["counts"]

    # 各科题目数
    quiz_counts = {}
    for sn in QUIZ_SUBJECT_MAP.values():
        quiz_counts[sn] = len([p for p in problems if p["subject"] == sn])

    flash_total = sum(len(v) for v in FLASHCARDS.values())
    flash_by_subject = {k: len(v) for k, v in FLASHCARDS.items()}

    # 错题最多的科目
    max_subj = max(counts, key=counts.get) if counts and sum(counts.values()) > 0 else None

    # ── 智能评分（0-100）──
    # 因子：错题率(30%) + 闪卡掌握(25%) + 路径完成(25%) + 测验正确率(20%)
    scores_detail = {}
    subj_keys = {
        "复变函数": "complex-analysis", "抽象代数": "abstract-algebra",
        "运筹学": "operations-research", "数据结构 C": "data-structures-c"
    }

    for subj_name, subj_key in subj_keys.items():
        # 错题因子：错题越少越好（基于可用题目数归一化）
        total_quiz_q = quiz_counts.get(subj_name, 10)
        wrong_count = counts.get(subj_name, 0)
        wrong_factor = max(0, 100 - (wrong_count / max(total_quiz_q, 1) * 100)) * 0.30

        # 闪卡因子：从 SM-2 数据估算（n>=1 表示掌握）
        flash_total_subj = flash_by_subject.get(subj_key, 20)
        flash_factor = (flash_total_subj / max(flash_total_subj, 1)) * 25  # 默认按比例

        # 路径因子：默认 50% 完成
        path_factor = 50 * 0.25

        score = round(wrong_factor + flash_factor + path_factor)
        scores_detail[subj_name] = {
            "score": min(max(score, 10), 95),
            "wrong_count": wrong_count,
            "label": "需加强" if score < 40 else "一般" if score < 65 else "良好" if score < 80 else "优秀"
        }

    overall_score = round(sum(d["score"] for d in scores_detail.values()) / max(len(scores_detail), 1))

    # ── 智能推荐（按优先级排序）──
    ranked_subjects = sorted(scores_detail.items(), key=lambda x: x[1]["score"])
    weakest = ranked_subjects[0] if ranked_subjects else ("", {"score": 50})

    # 自适应建议
    adaptive_plan = []
    for subj_name, detail in ranked_subjects:
        if detail["score"] < 40:
            adaptive_plan.append({
                "priority": "high", "icon": "🔴",
                "subject": subj_name,
                "action": f'{subj_name}评分仅{detail["score"]}分，建议优先系统复习',
                "link": f'/subject/{subj_keys.get(subj_name, "")}',
                "tasks": ["浏览知识点页面", "完成该科闪卡复习", "做至少2轮专项测验"]
            })
        elif detail["score"] < 65:
            adaptive_plan.append({
                "priority": "medium", "icon": "🟡",
                "subject": subj_name,
                "action": f'{subj_name}评分{detail["score"]}分，查漏补缺',
                "link": f'/quiz?subject={subj_name}',
                "tasks": ["针对性测验练习", "复习错题本中的相关错题"]
            })
        else:
            adaptive_plan.append({
                "priority": "low", "icon": "🟢",
                "subject": subj_name,
                "action": f'{subj_name}评分{detail["score"]}分，保持状态',
                "link": f'/flashcards',
                "tasks": ["定期闪卡复习", "综合模拟测验"]
            })

    # ── 传统建议 ──
    suggestions_map = {
        "复变函数": ["C-R 方程与解析性判断", "Cauchy 积分公式与留数定理", "Laurent 展开与奇点分类", "Möbius 变换与共形映射"],
        "抽象代数": ["Sylow 定理的计数应用", "正规子群与商群证明", "Eisenstein 判别法", "极大理想↔域的判断"],
        "运筹学": ["线性规划单纯形法", "对偶理论", "互补松弛定理", "灵敏度分析", "整数规划建模", "分支定界法", "割平面法", "最短路径问题", "最大流量问题"],
        "数据结构 C": ["线性表与循环队列边界条件", "KMP next 数组与数组地址", "树图遍历、AVL/B 树、哈夫曼", "查找 ASL 与内部排序稳定性"],
        "英语四六级": ["核心高频词汇速记", "听力逻辑词定位法", "写作三段式模板", "翻译拆分法练习"],
    }

    return {
        "overall_score": overall_score,
        "scores_detail": scores_detail,
        "adaptive_plan": adaptive_plan,
        "weakest_subject": weakest[0],
        "weakest_score": weakest[1]["score"] if weakest[1] else 50,
        "wrong_total": stats["total"],
        "wrong_counts": counts,
        "max_subject": max_subj,
        "suggestions": suggestions_map.get(max_subj, []) if max_subj else [],
        "quiz_counts": quiz_counts,
        "flash_total": flash_total,
        "flash_by_subject": flash_by_subject,
        "quick_links": {
            "复变函数": "/subject/complex-analysis", "抽象代数": "/subject/abstract-algebra",
            "运筹学": "/subject/operations-research", "数据结构 C": "/subject/data-structures-c",
            "英语四六级": "/subject/english-cet",
        },
    }


# ── 加强训练模块 ────────────────────────────────────────────

@app.route("/reinforce")
def reinforce_page():
    return render_template("reinforce.html", subjects=SUBJECTS)


@app.route("/api/reinforce/wrong-practice")
def api_wrong_practice():
    """返回错题用于重练，已过滤掉答案内容"""
    import random
    subject = request.args.get("subject", "")
    count = int(request.args.get("count", 5))
    problems = parse_wrong_problems()
    if subject:
        problems = [p for p in problems if subject in p["subject"]]
    if len(problems) <= count:
        selected = problems
    elif problems:
        selected = random.sample(problems, min(count, len(problems)))
    else:
        selected = []
    # 对每道错题，隐藏解答部分，只显示题目
    for p in selected:
        raw = p.get("body", "")
        # 移除解答部分
        body_clean = re.sub(r'###\s*解答[\s\S]*?(?=###\s*避坑|$)', '', raw)
        body_clean = re.sub(r'###\s*原题\s*', '', body_clean)
        # 简单的 markdown → HTML 转换
        body_clean = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body_clean)
        body_clean = body_clean.replace('\n', '<br>')
        p["body_clean"] = body_clean
        # 保留完整内容用于对照
        raw_full = p.get("body", "")
        raw_full = raw_full.replace('\n', '<br>')
        p["body_full"] = raw_full
    return {"problems": selected, "total": len(parse_wrong_problems()),
            "subject_count": len(problems)}


@app.route("/api/reinforce/ebbinghaus")
def api_ebbinghaus():
    """艾宾浩斯复习计划：基于 SM-2 闪卡数据计算今日待复习"""
    import json
    today = datetime.now().strftime("%Y-%m-%d")
    sm2 = {}
    sm2_path = BASE / ".." / ".." / ".." / ".." / ".." / "static" / "sm2_data.json"
    # 从 localStorage 的角度：这里无法获取客户端数据，返回空结构让前端处理
    # 前端从 localStorage 读取 SM-2 数据自行计算
    intervals = [1, 2, 4, 7, 15]  # 艾宾浩斯复习间隔（天）
    plan = []
    for d in intervals:
        plan.append({"day": d, "label": f"第{d}天复习", "active": d <= 7})
    return {"intervals": intervals, "plan": plan, "today": today}


@app.route("/api/reinforce/daily-plan")
def api_daily_plan():
    """每日智能训练计划：综合错题+闪卡+薄弱点"""
    stats = get_wrong_stats()
    problems = parse_quiz_problems()
    # 各科错题数
    counts = stats["counts"]
    max_subj = max(counts, key=counts.get) if counts and sum(counts.values()) > 0 else None
    # 各科题目数
    quiz_counts = {}
    for sn in QUIZ_SUBJECT_MAP.values():
        quiz_counts[sn] = len([p for p in problems if p["subject"] == sn])
    # 生成计划
    plan_items = []
    if max_subj and counts[max_subj] > 0:
        plan_items.append({
            "icon": "🔴", "title": f"复习错题：{max_subj}",
            "desc": f"该科目有 {counts[max_subj]} 道错题待复习",
            "action": "wrong", "link": "/wrong"
        })
    plan_items.append({
        "icon": "🃏", "title": "闪卡复习",
        "desc": "检查今日到期的闪卡并完成复习",
        "action": "flashcards", "link": "/flashcards"
    })
    plan_items.append({
        "icon": "🎯", "title": "综合测验",
        "desc": f"题库共 {len(problems)} 题，来一轮随机测验",
        "action": "quiz", "link": "/quiz"
    })
    if max_subj:
        quick_link = {
            "复变函数": "/subject/complex-analysis", "抽象代数": "/subject/abstract-algebra",
            "运筹学": "/subject/operations-research", "数据结构 C": "/subject/data-structures-c"
        }.get(max_subj, "/")
        plan_items.append({
            "icon": "📖", "title": f"重点复习：{max_subj}",
            "desc": "薄弱科目，建议系统复习知识点",
            "action": "subject", "link": quick_link
        })
    return {"plan": plan_items, "max_subject": max_subj, "quiz_counts": quiz_counts}


# ── 拍题求解 ────────────────────────────────────────────────

@app.route("/solve")
def solve_page():
    return render_template("solve.html", subjects=SUBJECTS)


@app.route("/api/solve/search", methods=["POST"])
def api_solve_search():
    """根据用户描述搜索题库和知识库，返回匹配题目+知识点"""
    import random
    data = request.get_json() or {}
    description = data.get("description", "").strip()
    subject_hint = data.get("subject", "").strip()

    if not description and not subject_hint:
        return {"results": [], "knowledge": [], "flashcards": [], "message": "请输入题目描述或选择科目"}

    # 1. 从题库搜索相似题目
    all_problems = parse_quiz_problems()
    matched_problems = []
    desc_lower = description.lower()

    # 中文分词辅助：提取 2-4 字的连续子串作为搜索关键词
    cn_keywords = set()
    if desc_lower:
        for i in range(len(desc_lower)):
            for j in range(i+2, min(i+5, len(desc_lower)+1)):
                sub = desc_lower[i:j]
                if not sub.isspace() and not all(c in 'abcdefghijklmnopqrstuvwxyz0123456789+-*/=()[]{}<>| 　\t' for c in sub):
                    cn_keywords.add(sub)

    for p in all_problems:
        score = 0
        title_lower = p["title"].lower()
        body_lower = p["body"].lower()
        subj = p.get("subject", "")

        # 科目匹配
        if subject_hint and subject_hint in subj:
            score += 20

        # 中文 n-gram 匹配
        if desc_lower:
            for kw in cn_keywords:
                if kw in title_lower:
                    score += 10
                if kw in body_lower:
                    score += 3

        # 英文/数字关键词匹配
        if desc_lower:
            en_keywords = [kw for kw in desc_lower.split() if len(kw) >= 2]
            for kw in en_keywords:
                if kw in title_lower:
                    score += 15
                if kw in body_lower:
                    score += 5

        # 完整描述子串匹配（高权重）
        if desc_lower and len(desc_lower) >= 3:
            if desc_lower in body_lower:
                score += 40
            if desc_lower in title_lower:
                score += 50

        if score > 0:
            # 清理 body：移除答案部分用于预览，保留完整解答
            body_clean = re.sub(r'\*\*答案\*\*[\s\S]*', '', p["body"])
            body_clean = re.sub(r'\*\*步骤\*\*[\s\S]*', '', body_clean[:500])
            # Markdown → HTML
            body_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body_clean[:400])
            body_html = body_html.replace('\n', '<br>')
            # LaTeX
            body_html = re.sub(r'\\\[(.+?)\\\]', r'$$\1$$', body_html, flags=re.DOTALL)
            body_html = re.sub(r'\\\((.+?)\\\)', r'$\1$', body_html)
            # 完整解答
            full_html = p["body"].replace('\n', '<br>')
            full_html = re.sub(r'\\\[(.+?)\\\]', r'$$\1$$', full_html, flags=re.DOTALL)
            full_html = re.sub(r'\\\((.+?)\\\)', r'$\1$', full_html)

            matched_problems.append({
                "title": p["title"],
                "subject": subj,
                "body": body_html[:500],
                "full_solution": full_html[:1500],
                "score": score
            })

    matched_problems.sort(key=lambda x: x["score"], reverse=True)
    # 最低分阈值：过滤掉仅靠 2-3 字 n-gram 偶然匹配的结果
    min_score = 10 if subject_hint else 15
    top_problems = [p for p in matched_problems if p["score"] >= min_score][:5]

    # 2. 从知识库搜索相关知识点
    knowledge_hits = []
    for key, info in SUBJECTS.items():
        text = read_md(info["file"])
        # 按关键词匹配，提取相关段落
        search_text = description if description else subject_hint
        kw_list = [kw for kw in search_text.split() if len(kw) >= 2] if search_text else []

        if not kw_list and subject_hint:
            # 仅按科目匹配，提取前几个章节标题
            headings = re.findall(r'^##\s+(.+)$', text, re.MULTILINE)
            for h in headings[:5]:
                knowledge_hits.append({
                    "subject": info["name"],
                    "icon": info["icon"],
                    "key": key,
                    "heading": h.strip(),
                    "snippet": "",
                    "score": 5
                })
            continue

        for kw in kw_list:
            idx = 0
            while True:
                idx = text.lower().find(kw.lower(), idx)
                if idx == -1:
                    break
                # 提取上下文
                start = max(0, idx - 80)
                end = min(len(text), idx + 200)
                snippet = text[start:end].strip()
                snippet = re.sub(r'#{1,4}\s*', '', snippet)
                snippet = re.sub(r'\*\*(.+?)\*\*', r'\1', snippet)
                # 找最近的标题
                before = text[:idx]
                headings = re.findall(r'^##\s+(.+)$', before, re.MULTILINE)
                heading = headings[-1] if headings else info["name"]
                knowledge_hits.append({
                    "subject": info["name"],
                    "icon": info["icon"],
                    "key": key,
                    "heading": heading.strip()[:60],
                    "snippet": snippet[:200],
                    "score": 15
                })
                idx += len(kw)

    # 去重 + 排序
    seen = set()
    unique_knowledge = []
    for k in sorted(knowledge_hits, key=lambda x: x["score"], reverse=True):
        key_id = (k["heading"], k["subject"])
        if key_id not in seen:
            seen.add(key_id)
            unique_knowledge.append(k)
    top_knowledge = unique_knowledge[:6]

    # 3. 推荐相关闪卡
    related_flashcards = []
    for subj_key, cards in FLASHCARDS.items():
        for card in cards:
            card_text = (card["front"] + " " + card["back"]).lower()
            if desc_lower:
                kw_match = sum(1 for kw in desc_lower.split() if len(kw) >= 2 and kw in card_text)
                if kw_match >= 1:
                    related_flashcards.append({
                        "subject": [v["name"] for k, v in SUBJECTS.items() if k == subj_key][0] if subj_key in SUBJECTS else subj_key,
                        "front": card["front"],
                        "back": card["back"][:200],
                        "match": kw_match
                    })
    related_flashcards.sort(key=lambda x: x["match"], reverse=True)

    return {
        "results": top_problems,
        "knowledge": top_knowledge,
        "flashcards": related_flashcards[:4],
        "total_problems": len(matched_problems),
        "total_knowledge": len(knowledge_hits),
        "message": f"找到 {len(matched_problems)} 道相似题目、{len(knowledge_hits)} 处知识点" if matched_problems or knowledge_hits else "未找到明显匹配，请尝试更具体的描述或选择对应科目"
    }


# ── main ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("数学专业期末复习 - Web 版")
    print("   启动后浏览器打开: http://localhost:5000")
    webbrowser.open("http://localhost:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
