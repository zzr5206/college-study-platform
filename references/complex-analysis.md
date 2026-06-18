# 复变函数期末复习

## 核心定义

复函数：
- 设 \(w=f(z)=u(x,y)+iv(x,y)\)，其中 \(z=x+iy\)。
- 复变函数的极限与连续通常转化为二元实函数处理，但要注意路径任意性。

解析函数：
- 函数在点 \(z_0\) 的某邻域内处处可导，称在 \(z_0\) 解析。
- 只在一点可导不等于解析。

Cauchy-Riemann 方程：
- 若 \(f(z)=u+iv\) 在点处可导，且 \(u,v\) 可微，则
  \[
  u_x=v_y,\quad u_y=-v_x.
  \]
- 若 \(u,v\) 一阶偏导连续且满足 C-R 方程，则函数解析。

调和函数：
- 若 \(u_{xx}+u_{yy}=0\)，则 \(u\) 为调和函数。
- 解析函数的实部和虚部都是调和函数。

## 高频定理

Cauchy 积分定理：
- 若 \(f\) 在单连通区域内解析，则任意闭路积分为 0。
- 条件关键词：解析、闭路、区域内无奇点。

Cauchy 积分公式：
\[
f(z_0)=\frac{1}{2\pi i}\int_C \frac{f(z)}{z-z_0}\,dz
\]
推广：
\[
f^{(n)}(z_0)=\frac{n!}{2\pi i}\int_C \frac{f(z)}{(z-z_0)^{n+1}}\,dz
\]

最大模原理：
- 非常值解析函数在区域内部不能取得最大模。

Liouville 定理：
- 全平面有界整函数必为常数。

## 典型题型

### 判断解析性

步骤：
1. 写出 \(u(x,y),v(x,y)\)。
2. 求偏导。
3. 检查 C-R 方程。
4. 若偏导连续，则可说明解析区域。

---

**题目 1**：判断 \(f(z)=z^2\) 的解析性，并指出解析区域。

**解**：
1. \(f(z)=z^2=(x+iy)^2=x^2-y^2+2ixy\)。
2. \(u=x^2-y^2,\ v=2xy\)。
3. 求偏导：
   \[
   u_x=2x,\quad u_y=-2y,\quad v_x=2y,\quad v_y=2x
   \]
4. 验证 C-R 方程：\(u_x=v_y=2x\)，\(u_y=-v_x=-2y\)，处处成立。
5. 四个偏导在全平面连续。

**答案**：\(f(z)=z^2\) 在全复平面解析。

---

**题目 2**：判断 \(f(z)=\bar z=x-iy\) 的解析性。

**解**：
1. \(u=x,\ v=-y\)。
2. 求偏导：\(u_x=1,\ u_y=0,\ v_x=0,\ v_y=-1\)。
3. 验证 C-R 方程：\(u_x=1\neq v_y=-1\)，处处不成立。

**答案**：\(f(z)=\bar z\) 在复平面上处处不解析。

---

**题目 3**：判断 \(f(z)=|z|^2=x^2+y^2\) 的解析性。

**解**：
1. \(u=x^2+y^2,\ v=0\)。
2. 求偏导：\(u_x=2x,\ u_y=2y,\ v_x=0,\ v_y=0\)。
3. C-R 方程：\(u_x=v_y\Rightarrow 2x=0\Rightarrow x=0\)，\(u_y=-v_x\Rightarrow 2y=0\Rightarrow y=0\)。
4. 仅在 \(z=0\) 一点满足 C-R 方程。

**答案**：\(f(z)=|z|^2\) 仅在 \(z=0\) 可导但不解析（不存在邻域使处处可导）。

---

易错点：
- 只验证某一点满足 C-R 方程，不能得出在邻域解析的结论（如题 3）。
- \(f(z)=\bar z,\ |z|^2\) 都是常见非解析函数的典型反例考试必记。

### 求闭路积分

判断入口：
- 被积函数在曲线内部解析：积分为 0（Cauchy 积分定理）。
- 有 \((z-z_0)^{-1}\)：用 Cauchy 积分公式 \(f(z_0)=\frac{1}{2\pi i}\oint\frac{f(z)}{z-z_0}dz\)。
- 有 \((z-z_0)^{-(n+1)}\)：用高阶导数公式。
- 有多个奇点：用留数定理。

---

**题目 1**：计算 \(\displaystyle\int_{|z|=1}\frac{e^z}{z}\,dz\)。

**解**：\(z=0\) 在 \(|z|=1\) 内。被积函数为 \(\frac{e^z}{z}=\frac{f(z)}{z-0}\)，其中 \(f(z)=e^z\) 解析。
由 Cauchy 积分公式（一阶）：\(\oint_{|z|=1}\frac{e^z}{z}dz=2\pi i\cdot e^0=2\pi i\)。

**答案**：\(2\pi i\)。

---

**题目 2**：计算 \(\displaystyle\int_{|z|=2}\frac{e^z}{(z-1)^3}\,dz\)。

**解**：\(z_0=1\) 在 \(|z|=2\) 内。分母 \((z-1)^3\) 对应 \(n=2\) 的高阶公式。
\[
\oint\frac{f(z)}{(z-z_0)^{n+1}}dz=\frac{2\pi i}{n!}f^{(n)}(z_0)
\]
\(f(z)=e^z\)，\(f''(z)=e^z\)，\(f''(1)=e\)。
积分 = \(\frac{2\pi i}{2!}\cdot e=\pi i e\)。

**答案**：\(\pi i e\)。

---

**题目 3**：计算 \(\displaystyle\int_{|z|=1}\frac{\sin z}{z^2+4}\,dz\)。

**解**：\(z^2+4=0\Rightarrow z=\pm2i\)，均在 \(|z|=1\) 外部。被积函数在 \(|z|\le1\) 上解析。
由 Cauchy 积分定理，闭路积分为 0。

**答案**：\(0\)。

---

**题目 4**：计算 \(\displaystyle\int_{|z|=3}\frac{1}{z^2+1}\,dz\)。

**解**：奇点 \(z=i,-i\) 均在 \(|z|=3\) 内。
\(\frac{1}{z^2+1}=\frac{1}{(z-i)(z+i)}=\frac{1}{2i}\left(\frac{1}{z-i}-\frac{1}{z+i}\right)\)。
由 Cauchy 积分公式：
\[
\oint\frac{1}{z-i}dz=2\pi i,\quad \oint\frac{1}{z+i}dz=2\pi i
\]
积分 = \(\frac{1}{2i}(2\pi i-2\pi i)=0\)。

**答案**：\(0\)。

### Taylor 与 Laurent 展开

常用展开：
\[
e^z=\sum_{n=0}^{\infty}\frac{z^n}{n!}
\]
\[
\frac{1}{1-z}=\sum_{n=0}^{\infty}z^n,\quad |z|<1
\]
\[
\frac{1}{1+z}=\sum_{n=0}^{\infty}(-1)^n z^n,\quad |z|<1
\]

展开技巧：
- 先化成几何级数形式。
- 注意展开中心和收敛范围。
- Laurent 展开中负幂部分称为主要部分。

**例 1**：将 \(f(z)=\frac{1}{z(z-2)}\) 在 \(0<|z|<2\) 展开为 Laurent 级数。

1. 部分分式分解：\(\frac{1}{z(z-2)}=-\frac{1}{2z}+\frac{1}{2(z-2)}\)

2. 环域 \(0<|z|<2\)：\(|z/2|<1\)，用几何级数：
   \[
   \frac{1}{z-2}=-\frac{1}{2}\cdot\frac{1}{1-z/2}=-\frac{1}{2}\sum_{n=0}^{\infty}\left(\frac{z}{2}\right)^n
   \]

3. 代入：
   \[
   \frac{1}{z(z-2)}=-\frac{1}{2z}-\frac{1}{4}\sum_{n=0}^{\infty}\frac{z^n}{2^n}
   =-\frac{1}{2}z^{-1}-\frac{1}{4}-\frac{1}{8}z-\frac{1}{16}z^2-\cdots
   \]

4. 适用域：\(0<|z|<2\)。

**例 2**：将同一函数在 \(|z|>2\) 展开为 Laurent 级数。

此时 \(|2/z|<1\)：
\[
\frac{1}{z-2}=\frac{1}{z}\cdot\frac{1}{1-2/z}=\frac{1}{z}\sum_{n=0}^{\infty}\left(\frac{2}{z}\right)^n
\]
\[
\frac{1}{z(z-2)}=-\frac{1}{2z}+\frac{1}{2}\cdot\frac{1}{z}\sum_{n=0}^{\infty}\frac{2^n}{z^n}
=\frac{1}{2}\sum_{n=2}^{\infty}\frac{2^{n-1}}{z^n}
=\frac{1}{z^2}+\frac{2}{z^3}+\frac{4}{z^4}+\cdots
\]
适用域：\(|z|>2\)（无正幂项，因无穷远点为可去奇点）。

**关键点**：同一函数在不同环域展开，级数形式完全不同。必须写清适用域！

### 孤立奇点分类

设 \(z_0\) 为孤立奇点。

**可去奇点**：
- Laurent 展开无负幂项。
- \(\lim_{z\to z_0}f(z)\) 有限。

**例**：\(f(z)=\frac{\sin z}{z}\)，\(z=0\)。
\[
\frac{\sin z}{z}=\frac{z-z^3/3!+z^5/5!-\cdots}{z}=1-\frac{z^2}{6}+\frac{z^4}{120}-\cdots
\]
无负幂项，\(\lim_{z\to0}\frac{\sin z}{z}=1\)（有限），故 \(z=0\) 为可去奇点。

**极点**：
- Laurent 展开负幂有限项（最多到 \(m\) 次）。
- 若 \(f(z)=\frac{g(z)}{(z-z_0)^m}\)，且 \(g(z_0)\ne0\)，则为 \(m\) 阶极点。

**例**：\(f(z)=\frac{1}{z^2(z-1)}\)。
- \(z=0\)：分母 \(z^2\)，分子在 \(z=0\) 处为 1（非零）→ **2 阶极点**。
- \(z=1\)：写成 \(\frac{1/(z^2)}{z-1}\)，分子在 \(z=1\) 处为 1（非零）→ **1 阶极点**。

**本性奇点**：
- Laurent 展开负幂无限多项。

**例**：\(f(z)=e^{1/z}=1+\frac{1}{z}+\frac{1}{2!z^2}+\frac{1}{3!z^3}+\cdots\)
负幂无限多项，\(z=0\) 为本性奇点。

**快速判别口诀**：
- \(\lim f(z)\) 有限→可去；\(\lim f(z)=\infty\)→极点；\(\lim f(z)\) 不存在（振荡）→本性。

### 留数

定义：
- Laurent 展开中 \((z-z_0)^{-1}\) 的系数就是留数。

**一阶极点**：
\[
\operatorname{Res}(f,z_0)=\lim_{z\to z_0}(z-z_0)f(z)
\]

**例 1**：求 \(f(z)=\frac{e^z}{z-1}\) 在 \(z=1\) 的留数。
\[
\operatorname{Res}(f,1)=\lim_{z\to1}(z-1)\frac{e^z}{z-1}=e^1=e
\]

**例 2**：求 \(f(z)=\frac{1}{z^2+1}\) 在 \(z=i\) 的留数。
\[
\operatorname{Res}(f,i)=\lim_{z\to i}(z-i)\frac{1}{(z-i)(z+i)}=\frac{1}{2i}
\]

**m 阶极点**：
\[
\operatorname{Res}(f,z_0)=\frac{1}{(m-1)!}\lim_{z\to z_0}\frac{d^{m-1}}{dz^{m-1}}\left[(z-z_0)^m f(z)\right]
\]

**例 3**：求 \(f(z)=\frac{e^z}{z^3}\) 在 \(z=0\) 的留数（3 阶极点）。
\[
\operatorname{Res}(f,0)=\frac{1}{2!}\lim_{z\to0}\frac{d^2}{dz^2}\left[z^3\cdot\frac{e^z}{z^3}\right]
=\frac{1}{2}\lim_{z\to0}\frac{d^2}{dz^2}[e^z]=\frac{1}{2}e^0=\frac{1}{2}
\]

验证：\(e^z/z^3=(1+z+z^2/2+z^3/6+\cdots)/z^3=z^{-3}+z^{-2}+\frac{1}{2}z^{-1}+\cdots\)，\(c_{-1}=1/2\) ✓。

**留数定理**：
\[
\int_C f(z)\,dz=2\pi i\sum \operatorname{Res}(f,z_k)
\]

**例 4**：计算 \(\int_{|z|=2}\frac{e^z}{z(z-1)}\,dz\)。

- 奇点：\(z=0\)（1阶）、\(z=1\)（1阶），均在 \(|z|=2\) 内。
- \(\operatorname{Res}(f,0)=\lim_{z\to0}z\cdot\frac{e^z}{z(z-1)}=\frac{1}{-1}=-1\)
- \(\operatorname{Res}(f,1)=\lim_{z\to1}(z-1)\cdot\frac{e^z}{z(z-1)}=\frac{e}{1}=e\)
- 积分 = \(2\pi i(-1+e)=2\pi i(e-1)\)

## 考前易错点

- 解析比可导更强，要有邻域条件。
- Cauchy 积分定理不能跨过奇点。
- 曲线方向默认正向为逆时针；顺时针要加负号。
- Laurent 展开必须写清适用环域。
- 留数只取 \((z-z_0)^{-1}\) 系数，不是所有负幂。

## 速记清单

- C-R 方程：\(u_x=v_y,u_y=-v_x\)。
- Cauchy 积分公式：核心识别 \(\frac{f(z)}{z-z_0}\)。
- 高阶公式：分母 \((z-z_0)^{n+1}\) 对应 \(f^{(n)}(z_0)\)。
- 留数定理：闭路积分等于 \(2\pi i\) 乘内部留数和。

## 留数计算实积分的三大类型

### 类型一：\(\int_0^{2\pi}R(\cos\theta,\sin\theta)\,d\theta\)

方法：
1. 令 \(z=e^{i\theta}\)，则 \(d\theta=\frac{dz}{iz}\)。
2. 代换：
   \[
   \cos\theta=\frac{z+z^{-1}}{2},\quad \sin\theta=\frac{z-z^{-1}}{2i}.
   \]
3. 积分变为单位圆 \(|z|=1\) 上的复积分。
4. 求出单位圆内所有奇点的留数和，乘以 \(2\pi i\)。

例：
\[
\int_0^{2\pi}\frac{d\theta}{5+3\cos\theta}.
\]
- 代换后：\(\displaystyle\oint_{|z|=1}\frac{2}{3z^2+10z+3}\,dz\)。
- 分母因式分解：\(3z^2+10z+3=(3z+1)(z+3)\)。
- 仅 \(z=-1/3\) 在单位圆内。
- \(\operatorname{Res}(f,-1/3)=\frac{2}{3(-1/3+3)}=\frac{1}{4}\)。
- 积分等于 \(2\pi i\cdot\frac{1}{4}=\frac{\pi}{2}\)。

易错点：
- 代换时 \(dz=ie^{i\theta}d\theta=iz\,d\theta\)，不要漏掉 \(dz\)。
- 算完留数后别忘了乘 \(2\pi i\)。

### 类型二：\(\int_{-\infty}^{+\infty}\frac{P(x)}{Q(x)}\,dx\)

条件：
- \(P,Q\) 为多项式。
- \(Q(x)\ne0\) 对所有实数 \(x\)。
- \(\deg Q\ge\deg P+2\)（保证反常积分收敛）。

方法：
1. 取上半平面 \((\Im z>0)\) 的所有奇点。
2. 计算每个奇点的留数和。
3. 积分等于 \(2\pi i\) 乘留数和。

例：
\[
\int_{-\infty}^{+\infty}\frac{dx}{x^2+1}.
\]
- 奇点：\(z=i,-i\)。上半平面仅有 \(z=i\)。
- \(\operatorname{Res}(f,i)=\frac{1}{2i}\)。
- 积分为 \(2\pi i\cdot\frac{1}{2i}=\pi\)。

易错点：
- 只取上半平面奇点，下半平面不算。
- 若实轴上有奇点，需用 Cauchy 主值积分，取上半小半圆绕过。

### 类型三：\(\int_{-\infty}^{+\infty}\frac{P(x)}{Q(x)}e^{imx}\,dx\)（Jordan 引理）

条件同类型二，但被积函数含有 \(e^{imx}(m>0)\)。

Jordan 引理：
- 当 \(R\to\infty\) 时，上半大圆弧上的积分趋于 0。
- 因此原积分等于 \(2\pi i\) 乘上半平面留数和。

例：
\[
\int_{-\infty}^{+\infty}\frac{\cos x}{x^2+1}\,dx.
\]
- 考虑 \(f(z)=\frac{e^{iz}}{z^2+1}\)，在上半平面奇点 \(z=i\)。
- \(\operatorname{Res}(f,i)=\frac{e^{-1}}{2i}\)。
- \(\int_{-\infty}^{+\infty}\frac{e^{ix}}{x^2+1}\,dx=2\pi i\cdot\frac{e^{-1}}{2i}=\frac{\pi}{e}\)。
- 取实部得 \(\int_{-\infty}^{+\infty}\frac{\cos x}{x^2+1}\,dx=\frac{\pi}{e}\)。

易错点：
- 原函数是 \(\frac{P}{Q}e^{imx}\)，不是单独 \(\frac{P}{Q}\)。
- 最后要根据 \(e^{imx}=\cos mx+i\sin mx\) 取实部或虚部对应原题。

## 辐角原理与 Rouché 定理

### 辐角原理

设 \(f\) 在简单闭曲线 \(C\) 上解析且不为零，在 \(C\) 内亚纯。则：
\[
\frac{1}{2\pi i}\oint_C\frac{f'(z)}{f(z)}\,dz = N - P
\]
其中 \(N\) 为 \(f\) 在 \(C\) 内的零点个数（计重数），\(P\) 为极点个数（计重数）。

几何意义：
- \(\Delta_C\arg f(z)\) 是当 \(z\) 绕 \(C\) 一周时，\(f(z)\) 的辐角变化量。
- \(N-P=\frac{1}{2\pi}\Delta_C\arg f(z)\)。

用途：
- 判断某区域内方程 \(f(z)=0\) 解的个数。

### Rouché 定理

设 \(f,g\) 在简单闭曲线 \(C\) 上及其内部解析，且在 \(C\) 上满足：
\[
|f(z)|>|g(z)|,\quad\forall z\in C.
\]
则 \(f\) 与 \(f+g\) 在 \(C\) 内有相同个数的零点（计重数）。

典型应用：
证明 \(z^5+3z+1=0\) 在 \(|z|<1\) 内有多少根。
- 取 \(f(z)=3z\)，\(g(z)=z^5+1\)。
- 在 \(|z|=1\) 上，\(|f(z)|=3\)，\(|g(z)|\le|z|^5+1=2\)。
- \(|f(z)|>|g(z)|\) 成立。
- \(f(z)=3z\) 在单位圆内恰有 1 个零点（\(z=0\)）。
- 因此原方程在 \(|z|<1\) 内也恰有 1 个根。

易错点：
- 必须验证 \(|f(z)|>|g(z)|\) 在边界上每点都成立。
- \(f,g\) 需要在曲线上及其内部解析，不能有奇点。

## 共形映射

### 基本概念

共形映射（保形映射/保角映射）：
- 若 \(f(z)\) 在区域 \(D\) 内单叶解析，且 \(f'(z)\ne0\)，则 \(f\) 是 \(D\) 上的共形映射。
- 共形映射保持两条曲线交点处的夹角（大小和方向）。

导数的几何意义：
- \(|f'(z_0)|\)：映射在 \(z_0\) 处的伸缩率。
- \(\arg f'(z_0)\)：映射在 \(z_0\) 处的旋转角。

### 分式线性变换（Möbius 变换）

\[
w=\frac{az+b}{cz+d},\quad ad-bc\ne0.
\]

核心性质：
1. **保圆性**：将圆周映射为圆周（直线视为半径无穷大的圆）。
2. **保交比性**：任意四点的交比在映射下不变：
   \[
   \frac{(w-w_1)(w_3-w_2)}{(w-w_2)(w_3-w_1)}=\frac{(z-z_1)(z_3-z_2)}{(z-z_2)(z_3-z_1)}.
   \]
3. **保对称性**：关于圆或直线的对称点映射后仍对称。
4. **群性质**：全体 Möbius 变换构成群。

两个重要特殊映射：
- **上半平面 → 单位圆盘**：
  \[
  w=e^{i\theta}\frac{z-z_0}{z-\overline{z_0}}\quad(\Im z_0>0).
  \]
- **单位圆盘 → 单位圆盘**：
  \[
  w=e^{i\theta}\frac{z-z_0}{1-\overline{z_0}z}\quad(|z_0|<1).
  \]
  （将 \(z_0\) 映为原点）

三步构造法（上半平面 → 单位圆盘）：
1. 找到将区域边界映射为另一区域边界的 Möbius 变换。
2. 用边界上一个检验点确定内部映射方向。
3. 利用对称点或交比确定未知参数。

### 初等函数构成的共形映射

| 函数 | 映射特点 | 典型区域变换 |
|------|----------|-------------|
| \(w=z^n\) | 角度放大 \(n\) 倍 | 角形域 → 角形域（张角乘 \(n\)） |
| \(w=e^z\) | 水平带形 → 角形域 | 带形 \(\{0<\Im z<h\}\) → 角形 \(\{0<\arg w<h\}\) |
| \(w=\sin z\) | 半带形 → 上半平面 | \(\{-\pi/2<\Re z<\pi/2,\Im z>0\}\) → 上半平面 |
| \(w=z+\frac{1}{z}\) | Joukowski 变换 | 圆外 → 椭圆外（空气动力学翼型） |
| \(w=\operatorname{Ln}z\) | 角形域 → 带形域 | 上半平面 → 带形 \(\{0<\Im w<\pi\}\) |

### 多步映射合成

实际问题常需将复杂区域经过 2 到 4 步映射变换到目标区域：
```
原区域 →(第1步)→ 标准区域（半平面/圆盘/带形/角形）→(第2步)→ 目标区域
```

考试重点：
- 给定两个区域，构造 Möbius 变换将一区域映为另一区域。
- 利用初等函数的映射性质处理角形域、带形域等非圆边界区域。
- 多个映射复合时，写清每一步的函数和区域变化。

易错点：
- Möbius 变换要求 \(ad-bc\neq0\)，否则退化为常数。
- 分式线性变换中，极点（分母为零的点）映射到 \(\infty\)。
- 初等函数映射通常不是一对一的，要说明是哪个分支。

## 经典例题精讲

### 例 1：已知实部求解析函数

已知 \(u(x,y)=x^3-3xy^2\) 为调和函数，求其共轭调和函数 \(v(x,y)\)，并写出解析函数 \(f(z)=u+iv\)。

**步骤**：
1. 由 C-R 方程 \(u_x=v_y\)：
   \[
   u_x=3x^2-3y^2=v_y
   \]
   积分得：
   \[
   v=\int(3x^2-3y^2)\,dy=3x^2y-y^3+\varphi(x)
   \]

2. 由 C-R 方程 \(u_y=-v_x\)：
   \[
   u_y=-6xy=-v_x,\quad v_x=6xy
   \]
   对 \(v\) 求偏导：
   \[
   v_x=6xy+\varphi'(x)=6xy\quad\Rightarrow\quad\varphi'(x)=0\quad\Rightarrow\quad\varphi(x)=C
   \]

3. 所以 \(v(x,y)=3x^2y-y^3+C\)。
   取 \(C=0\)，则：
   \[
   f(z)=u+iv=(x^3-3xy^2)+i(3x^2y-y^3)=z^3
   \]

**验证**：\(f(z)=z^3\) 在全平面解析，实部虚部均为调和函数。

### 例 2：计算 \(\int_{|z|=2}\frac{e^z}{(z-1)^3}\,dz\)

**思路**：分母 \((z-1)^3\) 对应 \(n=2\) 的高阶 Cauchy 公式。

**步骤**：
1. 设 \(f(z)=e^z\)。奇点 \(z_0=1\) 在 \(|z|=2\) 内。
2. 高阶公式（\(n=2\)）：
   \[
   \int_C\frac{f(z)}{(z-z_0)^{n+1}}\,dz=\frac{2\pi i}{n!}f^{(n)}(z_0)
   \]
3. \(f''(z)=e^z\)，\(f''(1)=e\)。
4. 积分 = \(\frac{2\pi i}{2!}\cdot e=\pi i e\)。

**答案**：\(\pi i e\)。

### 例 3：将 \(\frac{1}{z(z-2)}\) 在 \(0<|z|<2\) 展开为 Laurent 级数

**步骤**：
1. 部分分式分解：
   \[
   \frac{1}{z(z-2)}=\frac{A}{z}+\frac{B}{z-2}
   \]
   解得 \(A=-\frac{1}{2},\ B=\frac{1}{2}\)。
   \[
   \frac{1}{z(z-2)}=-\frac{1}{2z}+\frac{1}{2(z-2)}
   \]

2. 环域 \(0<|z|<2\)：\(|z/2|<1\)，可用几何级数展开 \(\frac{1}{z-2}\)：
   \[
   \frac{1}{z-2}=-\frac{1}{2}\cdot\frac{1}{1-z/2}=-\frac{1}{2}\sum_{n=0}^{\infty}\left(\frac{z}{2}\right)^n
   \]

3. 代入：
   \[
   \begin{aligned}
   \frac{1}{z(z-2)}&=-\frac{1}{2z}+\frac{1}{2}\cdot\left(-\frac{1}{2}\sum_{n=0}^{\infty}\frac{z^n}{2^n}\right)\\
   &=-\frac{1}{2z}-\frac{1}{4}\sum_{n=0}^{\infty}\frac{z^n}{2^n}\\
   &=-\frac{1}{2}z^{-1}-\frac{1}{4}-\frac{1}{8}z-\frac{1}{16}z^2-\cdots
   \end{aligned}
   \]

4. 适用域：\(0<|z|<2\)。

### 例 4：计算实积分 \(\int_{-\infty}^{+\infty}\frac{dx}{x^4+1}\)

**步骤**：
1. \(f(z)=\frac{1}{z^4+1}\)。分母零点即 \(z^4=-1=e^{i\pi}\)，解为 \(z_k=e^{i(\pi+2k\pi)/4},k=0,1,2,3\)。
   \[
   z_0=e^{i\pi/4}=\frac{1+i}{\sqrt2},\quad z_1=e^{i3\pi/4}=\frac{-1+i}{\sqrt2},\quad z_2=e^{i5\pi/4}=\frac{-1-i}{\sqrt2},\quad z_3=e^{i7\pi/4}=\frac{1-i}{\sqrt2}
   \]

2. 上半平面：\(z_0,z_1\)（虚部 > 0）。

3. 计算留数（一阶极点）：
   \[
   \operatorname{Res}(f,z_0)=\frac{1}{4z_0^3}=-\frac{z_0}{4},\quad
   \operatorname{Res}(f,z_1)=\frac{1}{4z_1^3}=-\frac{z_1}{4}
   \]
   （用到 \(z_k^4=-1\)，所以 \(1/(4z_k^3)=z_k/(4z_k^4)=-z_k/4\)）

4. 留数和：
   \[
   -\frac{1}{4}(z_0+z_1)=-\frac{1}{4}\left(\frac{1+i}{\sqrt2}+\frac{-1+i}{\sqrt2}\right)=-\frac{1}{4}\cdot\frac{2i}{\sqrt2}=-\frac{i}{2\sqrt2}
   \]

   更正计算：
   \[
   \operatorname{Res}(f,z_0)=\frac{1}{4z_0^3}=\frac{z_0}{4z_0^4}=-\frac{z_0}{4}=-\frac{1+i}{4\sqrt2}
   \]
   \[
   \operatorname{Res}(f,z_1)=-\frac{z_1}{4}=-\frac{-1+i}{4\sqrt2}
   \]
   留数和 = \(\frac{-1-i-(-1+i)}{4\sqrt2}=\frac{-1-i+1-i}{4\sqrt2}=\frac{-2i}{4\sqrt2}=-\frac{i}{2\sqrt2}\)

5. 积分 = \(2\pi i\cdot\left(-\frac{i}{2\sqrt2}\right)=\frac{\pi}{\sqrt2}\)。

**答案**：\(\frac{\pi}{\sqrt2}\)。

### 例 5：共形映射 — 将角形域映为上半平面

求将角形域 \(\{0<\arg z<\pi/3\}\) 映为上半平面的共形映射。

**步骤**：
1. 角形域张角 \(\pi/3\)。上半平面是张角为 \(\pi\) 的角形域。
2. 用幂函数放大角度：\(w=z^3\)。
   - 在角形域内，\(0<\arg z<\pi/3\)。
   - 映射后：\(0<\arg w<3\cdot\pi/3=\pi\)。
   - 恰好填满上半平面。
3. 验证：\(w=z^3\) 在区域内单叶解析且 \(w'(z)=3z^2\neq0\)（区域内 \(z\neq0\)）。

**答案**：\(w=z^3\)。

### 例 6：Rouché 定理 — 判断方程根的个数

证明方程 \(z^7-5z^3+12=0\) 在圆环 \(1<|z|<2\) 内根的个数。

**步骤**：

**第一步：在 \(|z|<2\) 内根的个数**

在 \(|z|=2\) 上，取 \(f(z)=z^7\)，\(g(z)=-5z^3+12\)。

\[
|f(z)|=|z|^7=2^7=128
\]
\[
|g(z)|=|-5z^3+12|\le 5|z|^3+12=5\cdot8+12=52
\]
\[
|f(z)|=128>52\ge|g(z)|
\]

Rouché 条件成立。\(f(z)=z^7\) 在 \(|z|<2\) 内有 7 个零点（\(z=0\)，7 重根）。

因此原方程在 \(|z|<2\) 内有 **7 个根**。

**第二步：在 \(|z|<1\) 内根的个数**

在 \(|z|=1\) 上，取 \(f(z)=12\)，\(g(z)=z^7-5z^3\)。

\[
|f(z)|=12
\]
\[
|g(z)|=|z^7-5z^3|\le|z|^7+5|z|^3=1+5=6
\]
\[
|f(z)|=12>6\ge|g(z)|
\]

Rouché 条件成立。\(f(z)=12\) 在 \(|z|<1\) 内无零点。

因此原方程在 \(|z|<1\) 内有 **0 个根**。

**第三步：结论**

圆环 \(1<|z|<2\) 内根的个数 = \(7-0=\boxed{7}\)。

**易错点**：
- 两次使用 Rouché 定理时，\(f\) 的选取可以不同。
- 验证不等式必须是严格的大于号。
- 注意 \(f\) 和 \(g\) 都在闭曲线上及其内部解析。

### 例 7：多步共形映射 — 带形域到上半平面

求将带形域 \(\{0<\Im z<\pi,\ \Re z>0\}\) 映为上半平面的共形映射。

**步骤**：

1. **第一步**：用 \(w_1=e^z\)。
   - \(z=x+iy\)，\(0<y<\pi\)，\(x>0\)。
   - \(w_1=e^x e^{iy}\)：模 \(e^x>1\)，辐角在 \((0,\pi)\)。
   - 区域变为：上半平面的单位圆外部 \(\{|w_1|>1,\ \Im w_1>0\}\)。

2. **第二步**：用 Möbius 变换将上半平面的单位圆外部映为上半平面。
   - 考虑 \(w_2=\frac{w_1-1}{w_1+1}\)。
   - 实轴上的区间 \((-1,1)\) 被映到负实轴，其余实轴映到正实轴。
   - 上半单位圆外被映到第一象限 \(\{ \Re w_2>0,\ \Im w_2>0 \}\)。

3. **第三步**：用 \(w=w_2^2\) 将第一象限映为上半平面。
   - 第一象限张角 \(\pi/2\)，平方后张角变为 \(\pi\)。
   - 因此 \(w=\left(\frac{e^z-1}{e^z+1}\right)^2\)。

**验证**：
- \(e^z\) 在带形域内单叶（因带形宽度 \(<\pi\)，\(e^z\) 是单叶的）。
- Möbius 变换保圆保角。
- \(w_2^2\) 在第一象限单叶（不含 0）。

**答案**：\(w=\left(\frac{e^z-1}{e^z+1}\right)^2\)。

**关键技巧**：多步映射的每一步都要把区域边界的变化写清楚。

### 例 8：Fourier 变换计算

求 \(f(t)=e^{-a|t|}\ (a>0)\) 的 Fourier 变换。

**步骤**：

\[
\begin{aligned}
F(\omega)&=\int_{-\infty}^{\infty}e^{-a|t|}e^{-i\omega t}\,dt\\
&=\int_{-\infty}^{0}e^{at}e^{-i\omega t}\,dt+\int_{0}^{\infty}e^{-at}e^{-i\omega t}\,dt\\
&=\int_{-\infty}^{0}e^{(a-i\omega)t}\,dt+\int_{0}^{\infty}e^{-(a+i\omega)t}\,dt\\
&=\left[\frac{e^{(a-i\omega)t}}{a-i\omega}\right]_{-\infty}^{0}+\left[\frac{-e^{-(a+i\omega)t}}{a+i\omega}\right]_{0}^{\infty}\\
&=\frac{1}{a-i\omega}+\frac{1}{a+i\omega}\\
&=\frac{2a}{a^2+\omega^2}
\end{aligned}
\]

**答案**：\(\mathcal{F}[e^{-a|t|}]=\frac{2a}{a^2+\omega^2}\)。

**验证**：当 \(a=1\) 时，变换为 \(\frac{2}{1+\omega^2}\)，这是常见的 Lorentz 型函数。

### 例 9：Laplace 变换解微分方程

用 Laplace 变换求解：\(y''+4y'+3y=e^{-t}\)，\(y(0)=1,\ y'(0)=0\)。

**步骤**：

1. 两边取 Laplace 变换：
   \[
   [s^2Y(s)-sy(0)-y'(0)]+4[sY(s)-y(0)]+3Y(s)=\frac{1}{s+1}
   \]

2. 代入初值 \(y(0)=1,y'(0)=0\)：
   \[
   [s^2Y(s)-s\cdot1-0]+4[sY(s)-1]+3Y(s)=\frac{1}{s+1}
   \]
   \[
   (s^2+4s+3)Y(s)-s-4=\frac{1}{s+1}
   \]

3. 解出 \(Y(s)\)：
   \[
   Y(s)=\frac{s+4}{s^2+4s+3}+\frac{1}{(s+1)(s^2+4s+3)}
   \]
   \[
   s^2+4s+3=(s+1)(s+3)
   \]
   \[
   Y(s)=\frac{s+4}{(s+1)(s+3)}+\frac{1}{(s+1)^2(s+3)}
   \]

4. 部分分式展开：
   \[
   \frac{s+4}{(s+1)(s+3)}=\frac{3/2}{s+1}-\frac{1/2}{s+3}
   \]
   \[
   \frac{1}{(s+1)^2(s+3)}=\frac{1/4}{s+1}+\frac{1/2}{(s+1)^2}-\frac{1/4}{s+3}
   \]

5. 合并：
   \[
   Y(s)=\frac{7/4}{s+1}+\frac{1/2}{(s+1)^2}-\frac{3/4}{s+3}
   \]

6. 取逆 Laplace 变换：
   \[
   y(t)=\frac{7}{4}e^{-t}+\frac{1}{2}te^{-t}-\frac{3}{4}e^{-3t}
   \]

**答案**：\(y(t)=\frac{7}{4}e^{-t}+\frac{1}{2}te^{-t}-\frac{3}{4}e^{-3t}\)。

**验证**：代入 \(t=0\)，\(y(0)=\frac{7}{4}+0-\frac{3}{4}=1\) ✓。

### 例 10：辐角原理应用

设 \(f(z)=z^3-2z+1\)。利用辐角原理判断 \(f(z)\) 在 \(|z|<2\) 内零点的个数。

**步骤**：

1. \(f(z)=z^3-2z+1\) 是多项式，在 \(|z|\le2\) 上解析，有 3 个零点（计重数）在全平面。

2. 在 \(|z|=2\) 上，
   \[
   f(2e^{i\theta})=8e^{i3\theta}-4e^{i\theta}+1=e^{i3\theta}(8-4e^{-i2\theta}+e^{-i3\theta})
   \]

3. 由于 \(| -4e^{-i2\theta}+e^{-i3\theta} |\le4+1=5\)，而 \(8>5\)，
   \[
   |f(z)-z^3|=|-2z+1|\le2|z|+1=5<8=|z|^3=|z^3|
   \]

4. 由 Rouché 定理，\(f(z)\) 与 \(z^3\) 在 \(|z|<2\) 内有相同个数的零点。

5. \(z^3\) 在 \(|z|<2\) 内有 3 个零点（\(z=0\)，三重）。因此原方程在 \(|z|<2\) 内也有 3 个零点。

**答案**：3 个零点。

## 公式卡片 — 复变函数必背

### 核心公式

**Cauchy-Riemann 方程**：
\[
u_x=v_y,\quad u_y=-v_x
\]

**Cauchy 积分公式（一阶）**：
\[
f(z_0)=\frac{1}{2\pi i}\oint_C\frac{f(z)}{z-z_0}\,dz
\]

**Cauchy 积分公式（高阶）**：
\[
f^{(n)}(z_0)=\frac{n!}{2\pi i}\oint_C\frac{f(z)}{(z-z_0)^{n+1}}\,dz
\]

**Taylor 级数**（在 \(z_0\) 展开，收敛半径 \(R\)）：
\[
f(z)=\sum_{n=0}^{\infty}\frac{f^{(n)}(z_0)}{n!}(z-z_0)^n,\quad|z-z_0|<R
\]

**Laurent 级数**（圆环域 \(r<|z-z_0|<R\)）：
\[
f(z)=\sum_{n=-\infty}^{\infty}c_n(z-z_0)^n,\quad c_n=\frac{1}{2\pi i}\oint_C\frac{f(z)}{(z-z_0)^{n+1}}\,dz
\]

**留数定理**：
\[
\oint_C f(z)\,dz=2\pi i\sum_{k=1}^{n}\operatorname{Res}(f,z_k)
\]

**一阶极点留数**：
\[
\operatorname{Res}(f,z_0)=\lim_{z\to z_0}(z-z_0)f(z)
\]

**m 阶极点留数**：
\[
\operatorname{Res}(f,z_0)=\frac{1}{(m-1)!}\lim_{z\to z_0}\frac{d^{m-1}}{dz^{m-1}}\Big[(z-z_0)^m f(z)\Big]
\]

**辐角原理**：
\[
\frac{1}{2\pi i}\oint_C\frac{f'(z)}{f(z)}\,dz=N-P
\]

**Möbius 变换（上半平面→单位圆盘）**：
\[
w=e^{i\theta}\frac{z-z_0}{z-\overline{z_0}},\quad\Im z_0>0
\]

### 常用展开

\[
e^z=1+z+\frac{z^2}{2!}+\frac{z^3}{3!}+\cdots=\sum_{n=0}^{\infty}\frac{z^n}{n!}
\]
\[
\sin z=z-\frac{z^3}{3!}+\frac{z^5}{5!}-\cdots=\sum_{n=0}^{\infty}(-1)^n\frac{z^{2n+1}}{(2n+1)!}
\]
\[
\cos z=1-\frac{z^2}{2!}+\frac{z^4}{4!}-\cdots=\sum_{n=0}^{\infty}(-1)^n\frac{z^{2n}}{(2n)!}
\]
\[
\frac{1}{1-z}=1+z+z^2+z^3+\cdots=\sum_{n=0}^{\infty}z^n,\quad|z|<1
\]
\[
\frac{1}{1+z}=1-z+z^2-z^3+\cdots=\sum_{n=0}^{\infty}(-1)^n z^n,\quad|z|<1
\]

### 实积分三类型速查

| 类型 | 方法 | 关键公式 |
|------|------|---------|
| \(\int_0^{2\pi}R(\cos\theta,\sin\theta)d\theta\) | \(z=e^{i\theta}\) 代换 | \(d\theta=\frac{dz}{iz},\ \cos\theta=\frac{z+z^{-1}}{2}\) |
| \(\int_{-\infty}^\infty\frac{P(x)}{Q(x)}dx\) | 上半平面留数 | \(\deg Q\ge\deg P+2\) |
| \(\int_{-\infty}^\infty\frac{P(x)}{Q(x)}e^{imx}dx\) | Jordan 引理 | 取实部/虚部对应原题 |

## 积分变换（Fourier & Laplace）

> 注：部分高校的"复变函数与积分变换"课程包含此内容

### Fourier 变换

**定义**：
\[
F(\omega)=\mathcal{F}[f(t)]=\int_{-\infty}^{+\infty}f(t)e^{-i\omega t}\,dt
\]
**逆变换**：
\[
f(t)=\mathcal{F}^{-1}[F(\omega)]=\frac{1}{2\pi}\int_{-\infty}^{+\infty}F(\omega)e^{i\omega t}\,d\omega
\]

**常用变换对**：
| \(f(t)\) | \(F(\omega)\) |
|----------|--------------|
| \(e^{-at}u(t)\ (a>0)\) | \(\frac{1}{a+i\omega}\) |
| \(\delta(t)\) | \(1\) |
| \(1\) | \(2\pi\delta(\omega)\) |
| 矩形脉冲 | \(\frac{2\sin\omega}{\omega}\) |

**性质**：
- 线性：\(\mathcal{F}[af+bg]=aF+bG\)
- 微分：\(\mathcal{F}[f'(t)]=i\omega F(\omega)\)
- 卷积：\(\mathcal{F}[f*g]=F(\omega)G(\omega)\)

### Laplace 变换

**定义**：
\[
F(s)=\mathcal{L}[f(t)]=\int_0^{\infty}f(t)e^{-st}\,dt
\]

**常用变换对**：
| \(f(t)\) | \(F(s)\) |
|----------|---------|
| \(1\) | \(\frac{1}{s}\) |
| \(t^n\) | \(\frac{n!}{s^{n+1}}\) |
| \(e^{at}\) | \(\frac{1}{s-a}\) |
| \(\sin at\) | \(\frac{a}{s^2+a^2}\) |
| \(\cos at\) | \(\frac{s}{s^2+a^2}\) |

**性质**：
- 微分：\(\mathcal{L}[f'(t)]=sF(s)-f(0)\)
- 积分：\(\mathcal{L}[\int_0^t f(\tau)d\tau]=\frac{F(s)}{s}\)
- 卷积：\(\mathcal{L}[f*g]=F(s)G(s)\)

### 用 Laplace 变换解 ODE

步骤：原微分方程 → Laplace 变换 → 解代数方程 → 逆变换 → 得解

易错：记得初值 \(f(0),f'(0)\) 要代进去。

## Poisson 积分公式

若 \(f\) 在 \(|z|\le R\) 解析，则对 \(|z|<R\)：
\[
f(z)=\frac{1}{2\pi}\int_0^{2\pi}f(Re^{i\varphi})\frac{R^2-|z|^2}{|Re^{i\varphi}-z|^2}\,d\varphi
\]

用于：由边界值求内部值。特别地取 \(z=0\) 得均值公式：
\[
f(0)=\frac{1}{2\pi}\int_0^{2\pi}f(Re^{i\varphi})\,d\varphi
\]

## 解析延拓

- 若 \(f\) 在区域 \(D_1\) 解析，\(g\) 在区域 \(D_2\) 解析，\(D_1\cap D_2\neq\varnothing\)，且在交集上 \(f=g\)，则 \(g\) 是 \(f\) 的解析延拓。
- Schwarz 对称原理：若 \(f\) 在实轴上一段为实数，则可对称延拓。

## 考前快速自查（复变函数）

- 我能不能手写 C-R 方程并判断一个函数的解析区域？
- 我能不能一眼看出 Cauchy 积分公式的入口（分母是 \((z-z_0)\) 还是 \((z-z_0)^{n+1}\)）？
- 我能不能做 Laurent 展开并分类奇点类型？
- 我能不能算一阶和 m 阶极点的留数？
- 我能不能选对三大实积分类型并正确使用？
- 我能不能用 Rouché 定理判断方程在某区域内的根的个数？
- 我能不能构造 Möbius 变换把上半平面映为单位圆盘？

