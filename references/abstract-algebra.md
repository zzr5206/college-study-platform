# 抽象代数期末复习

## 复习核心

抽象代数考试通常考两类能力：
- 能准确写定义。
- 能从定义推出结论，完成证明。

做证明题时先问：
1. 要证明的对象是什么？
2. 该对象的定义包含哪些条件？
3. 哪些条件已经由题目给出，哪些需要验证？

## 群论基础

群：
- 非空集合 \(G\) 和二元运算 \(*\) 构成群，需要满足封闭性、结合律、单位元、逆元。

子群判别：
- 非空子集 \(H\subseteq G\)。
- 对任意 \(a,b\in H\)，若 \(ab^{-1}\in H\)，则 \(H\) 是子群。
- 有限子集常用：非空且对运算封闭即可。

循环群：
- 若存在 \(a\in G\)，使 \(G=\langle a\rangle\)，则 \(G\) 为循环群。
- 元 \(a\) 的阶是使 \(a^n=e\) 的最小正整数 \(n\)。

Lagrange 定理：
- 若 \(G\) 是有限群，\(H\le G\)，则 \(|H|\mid |G|\)。
- 推论：元素阶整除群阶。

陪集：
- 左陪集：\(aH=\{ah:h\in H\}\)。
- 右陪集：\(Ha=\{ha:h\in H\}\)。
- 陪集要么相等，要么不交。

正规子群：
- \(N\trianglelefteq G\) 当且仅当对任意 \(g\in G\)，有 \(gNg^{-1}=N\)。
- 等价地，左陪集等于右陪集：\(gN=Ng\)。

商群：
- 若 \(N\trianglelefteq G\)，则 \(G/N=\{gN:g\in G\}\) 构成群。
- 运算为 \((aN)(bN)=abN\)。

群同态：
- 映射 \(\varphi:G\to G'\) 满足 \(\varphi(ab)=\varphi(a)\varphi(b)\)。
- 核：\(\ker\varphi=\{g\in G:\varphi(g)=e'\}\)。
- 像：\(\operatorname{Im}\varphi=\{\varphi(g):g\in G\}\)。
- \(\ker\varphi\trianglelefteq G\)。

第一同构定理：
\[
G/\ker\varphi \cong \operatorname{Im}\varphi.
\]

## 群论典型证明套路

### 证明子群

模板：
1. 说明 \(H\) 非空，通常证明 \(e\in H\)。
2. 任取 \(a,b\in H\)。
3. 证明 \(ab^{-1}\in H\)。
4. 得出 \(H\le G\)。

**例**：设 \(G\) 为群，证明 \(Z(G)=\{g\in G:gx=xg,\forall x\in G\}\) 是 \(G\) 的子群。

1. **非空**：\(e\in Z(G)\)（单位元与所有元素交换）。

2. **封闭**：任取 \(a,b\in Z(G)\)。对任意 \(x\in G\)：
   \[
   (ab^{-1})x=a(b^{-1}x)=a(b^{-1}x(b b^{-1}))=a(b^{-1}(xb)b^{-1})
   \]
   利用 \(b\in Z(G)\)，\(xb=bx\)，即 \(b^{-1}x=xb^{-1}\)：
   \[
   =a(xb^{-1})= (ax)b^{-1}= (xa)b^{-1}=x(ab^{-1})
   \]
   因此 \(ab^{-1}\in Z(G)\)。

3. 由子群判别法，\(Z(G)\le G\)。

### 证明正规

常见入口：
- 任取 \(g\in G,n\in N\)，证明 \(gng^{-1}\in N\)。
- 若 \(N=\ker\varphi\)，直接说明核一定正规。
- 若 \(G\) 是阿贝尔群，则任意子群正规。

**例**：证明 \(Z(G)\trianglelefteq G\)。

任取 \(g\in G,a\in Z(G)\)。由 \(Z(G)\) 定义：
\[
gag^{-1}=a(gg^{-1})=a\in Z(G).
\]
因此 \(Z(G)\) 对共轭封闭，\(Z(G)\trianglelefteq G\)。

**例**：若群 \(G\) 满足 \(G/Z(G)\) 是循环群，证明 \(G\) 是阿贝尔群。

设 \(G/Z(G)=\langle xZ(G)\rangle\)。任取 \(a,b\in G\)：
- \(aZ(G)=(xZ(G))^i=x^iZ(G)\)，即 \(a=x^iz_1\)
- \(bZ(G)=(xZ(G))^j=x^jZ(G)\)，即 \(b=x^jz_2\)
- 则 \(ab=x^iz_1x^jz_2=x^ix^jz_1z_2=x^{i+j}z_1z_2\)
- \(ba=x^jz_2x^iz_1=x^jx^iz_2z_1=x^{i+j}z_1z_2=ab\)
因此 \(G\) 为阿贝尔群。

### 求商群

步骤：
1. 先验证正规性。
2. 写出所有陪集。
3. 用代表元计算运算。
4. 判断商群结构。

**例**：\(G=\mathbb Z_6\)（加法），\(H=\langle[2]\rangle=\{[0],[2],[4]\}\)（正规，因 G 阿贝尔）。

陪集：
\[
0+H=\{[0],[2],[4]\},\quad 1+H=\{[1],[3],[5]\}
\]
\(G/H=\{H,1+H\}\)，\(|G/H|=6/3=2\)。

运算：\((1+H)+(1+H)=2+H=H\)（2阶元）。

\(G/H\cong\mathbb Z_2\)。

## 环与域

环：
- 集合 \(R\) 对加法构成阿贝尔群。
- 乘法满足结合律。
- 乘法对加法满足左右分配律。

交换环：
- 乘法交换。

含幺环：
- 存在乘法单位元 \(1\)。

整环：
- 含幺交换环，且无零因子。

域：
- 至少两个元素的含幺交换环。
- 每个非零元素都有乘法逆元。
- 域一定是整环，反过来不一定成立。

理想：
- \(I\subseteq R\) 是加法子群。
- 对任意 \(r\in R,a\in I\)，有 \(ra,ar\in I\)。
- 交换环中只需写 \(ra\in I\)。

商环：
- 若 \(I\) 是环 \(R\) 的理想，则 \(R/I\) 构成环。

环同态：
- 保持加法和乘法，通常还要求保持单位元，视教材定义而定。
- 核是理想。

最大理想与域：
- 交换含幺环中，\(I\) 为最大理想当且仅当 \(R/I\) 是域。

素理想与整环：
- 交换含幺环中，\(I\) 为素理想当且仅当 \(R/I\) 是整环。

## 环论典型证明套路

### 证明理想

模板：
1. 证明 \(I\) 对加法为子群。
2. 任取 \(r\in R,a\in I\)。
3. 证明 \(ra\in I\) 和必要时 \(ar\in I\)。

**例**：在 \(\mathbb Z\) 中，证明 \(n\mathbb Z=\{nk:k\in\mathbb Z\}\) 是理想。

1. **加法子群**：\(nk_1-nk_2=n(k_1-k_2)\in n\mathbb Z\)。0 = n·0 ∈ nZ。✓

2. **吸收性**：任取 \(r\in\mathbb Z\)，\(nk\in n\mathbb Z\)，
   \(r\cdot nk=n(rk)\in n\mathbb Z\)。✓（\(\mathbb Z\) 交换，单侧 = 双侧）

3. 因此 \(n\mathbb Z\) 是 \(\mathbb Z\) 的理想。实际上，\(\mathbb Z\) 的所有理想都是 \(n\mathbb Z\) 的形式（\(\mathbb Z\) 是 PID）。

### 证明商环是域

常见方法：
- 证明对应理想是最大理想。
- 或者直接证明每个非零陪集都有逆元。

**例**：证明 \(\mathbb Z_3[i]=\mathbb Z[i]/(3)\) 是域。

1. \(\mathbb Z[i]\) 是 Euclidean 环（范数 \(N(a+bi)=a^2+b^2\)）。

2. 检查 (3) 是否为极大理想：假设 (3) ⊆ I ⊆ Z[i] 且 I 为理想。

3. 因 Z[i] 是 PID，I = (α)。则 α | 3。

4. 在 Z[i] 中，3 = (1+2i)(1-2i) + ... 实际 3 在 Z[i] 中是否可约？
   - \(N(3)=9\)。若 3 = αβ，则 N(α)N(β)=9。
   - 检查 N(α)=3 是否有解：\(a^2+b^2=3\) 无整数解。
   - 因此 3 在 Z[i] 中不可约，(3) 是极大理想。

5. 由极大理想对应域：\(\mathbb Z[i]/(3)\) 是域（9 个元素的有限域）。

## 高频计算

整数模 \(n\)：
- \(\mathbb Z_n\) 是域当且仅当 \(n\) 是素数。
- \(\mathbb Z_n\) 中元素 \([a]\) 可逆当且仅当 \(\gcd(a,n)=1\)。

**例**：在 \(\mathbb Z_{26}\) 中，哪些元素可逆？求 \([7]^{-1}\)。

可逆元素：1,3,5,7,9,11,15,17,19,21,23,25（与 26 互素的数，共 \(\varphi(26)=12\) 个）。

求 \([7]^{-1}\)：用扩展欧几里得。26 = 7·3+5, 7 = 5·1+2, 5 = 2·2+1。回代：
1 = 5-2·2 = 5-2·(7-5·1) = 3·5-2·7 = 3·(26-7·3)-2·7 = 3·26-11·7。
因此 -11·7 ≡ 1 (mod 26)，15·7 ≡ 1 (mod 26)，\([7]^{-1}=[15]\)。

验证：7·15=105=26·4+1≡1 (mod 26) ✓。

循环群：
- \(\mathbb Z_n\) 的生成元是与 \(n\) 互素的元素。
- 生成元个数为 \(\varphi(n)\)。

**例**：求 \(\mathbb Z_{20}\) 的所有生成元。

\(\varphi(20)=20(1-1/2)(1-1/5)=8\)。与 20 互素的数：1,3,7,9,11,13,17,19。
生成元：[1],[3],[7],[9],[11],[13],[17],[19]。

置换群：
- 置换阶等于循环分解中各循环长度的最小公倍数。
- 奇偶性看换位分解个数奇偶。

**例**：求置换 \(\sigma=(1\;2\;3)(4\;5)(6\;7\;8\;9)\)（S₉）的阶和奇偶性。

循环分解：1 个 3-轮换 + 1 个 2-轮换 + 1 个 4-轮换。
阶 = lcm(3,2,4) = **12**。

奇偶性：3-轮换 = 2 个换位（奇）→但分开判定更简单：
- 一个 k-轮换 = k-1 个换位
- (1 2 3) = 2 个换位，(4 5) = 1 个换位，(6 7 8 9) = 3 个换位
- 总换位数 = 2+1+3 = 6（偶）→ σ 是**偶置换** ∈ A₉。

## 易错点

- 子群和正规子群不是一回事。
- 商群要求正规子群，商环要求理想。
- 同态的核不是普通子群，而是正规子群或理想。
- 阿贝尔群中所有子群正规，非阿贝尔群中不一定。
- 域中只有两个平凡理想：\(\{0\}\) 和自身。
- \(\mathbb Z_n\) 是域必须 \(n\) 为素数。

## 考前背诵清单

- 群、子群、正规子群、商群、同态、核。
- Lagrange 定理和元素阶整除群阶。
- 第一同构定理。
- 环、理想、商环、整环、域。
- 最大理想对应域，素理想对应整环。

## Sylow 定理

Sylow 定理是有限群理论的核心，用于分析群的子群结构和判断群的单纯性。

### 三个 Sylow 定理

设 \(G\) 为有限群，\(|G|=p^a\cdot m\)，其中 \(p\) 为素数，\(\gcd(p,m)=1\)。

**第一 Sylow 定理（存在性）**：
对每个 \(1\le k\le a\)，\(G\) 存在 \(p^k\) 阶子群。特别地，存在 \(p^a\) 阶子群，称为 Sylow \(p\)-子群。

**第二 Sylow 定理（共轭性）**：
\(G\) 的所有 Sylow \(p\)-子群两两共轭。即若 \(P,Q\) 为 Sylow \(p\)-子群，则存在 \(g\in G\) 使 \(Q=gPg^{-1}\)。

**第三 Sylow 定理（计数定理）**：
设 \(n_p\) 为 \(G\) 中 Sylow \(p\)-子群的个数，则：
\[
n_p\equiv1\pmod{p},\qquad n_p\mid m.
\]
且 \(n_p=[G:N_G(P)]\)，其中 \(N_G(P)\) 是 \(P\) 的正规化子。

### 典型应用：证明群不是单群

思路模板：
1. 取 \(|G|\) 的一个素因子 \(p\)。
2. 计算可能满足 \(n_p\equiv1\pmod{p}\) 且 \(n_p\mid m\) 的 \(n_p\)。
3. 若 \(n_p=1\) 是唯一可能，则 Sylow \(p\)-子群正规，\(G\) 不是单群。
4. 若 \(n_p>1\)，尝试用群作用推出矛盾。

例：证明阶为 \(pq\) 的群不是单群（\(p,q\) 为素数，\(p>q\)）。
- \(|G|=pq=p\cdot q\)，\(n_p\mid q\) 且 \(n_p\equiv1\pmod{p}\)。
- \(n_p\) 只能为 1（因为 \(q<p\)，无法满足 \(q\equiv1\pmod{p}\)）。
- 因此 Sylow \(p\)-子群正规，\(G\) 不是单群。

例：证明阶为 72 的群不是单群。
- \(72=2^3\cdot3^2\)。
- \(n_3\equiv1\pmod{3}\) 且 \(n_3\mid8\)，可能值：1,4。
- 若 \(n_3=1\)，则 Sylow 3-子群正规，非单群。
- 若 \(n_3=4\)，考虑 \(G\) 在 Sylow 3-子群集合上的共轭作用，得同态 \(G\to S_4\)。由 \(72\nmid24\) 知核非平凡，非单群。

### p-群的性质

- 非平凡 \(p\)-群有非平凡中心（类方程推导）。
- \(p^2\) 阶群必为阿贝尔群。
- \(p\)-群的任意子群链可在顶部和底部正规化子递增。

## 群作用

### 基本概念

群 \(G\) 在集合 \(X\) 上的作用是指同态 \(\varphi:G\to S_X\)（\(S_X\) 为 \(X\) 的对称群）。等价定义：
- 映射 \(G\times X\to X\)，\((g,x)\mapsto g\cdot x\)。
- 满足 \((gh)\cdot x=g\cdot(h\cdot x)\) 且 \(e\cdot x=x\)。

### 轨道与稳定子

轨道：
\[
G\cdot x=\{g\cdot x:g\in G\}\subseteq X.
\]

稳定子：
\[
G_x=\{g\in G:g\cdot x=x\}\le G.
\]

**轨道-稳定子定理**：
\[
|G\cdot x|=[G:G_x]=\frac{|G|}{|G_x|}.
\]

### 类方程

取 \(X=G\)，作用为共轭 \(g\cdot x=gxg^{-1}\)，得：
\[
|G|=|Z(G)|+\sum_{i=1}^{r}[G:C_G(g_i)]
\]
其中 \(\{g_i\}\) 为非中心元素的共轭类代表元，\(C_G(g_i)\) 为中心化子。

类方程是证明 \(p\)-群有非平凡中心的标准工具。

## 对称群与交代群

### \(S_n\) 的结构

- 任意置换可唯一分解为不相交的轮换的乘积。
- **共轭类**：\(S_n\) 中两元素共轭当且仅当它们的轮换型相同。
- 置换的阶等于轮换分解中各轮换长度的最小公倍数。
- 奇偶性：偶置换构成交代群 \(A_n\)，\([S_n:A_n]=2\)，故 \(A_n\trianglelefteq S_n\)。

### \(A_n\) 的单纯性

- \(A_n\) 对 \(n\ge5\) 是单群。
- 这是证明五次以上一般方程无根式解（Galois 理论）的关键。

## 多项式环与不可约性

### 基本概念

设 \(F\) 为域，\(F[x]\) 为多项式环：
- \(F[x]\) 是 Euclidean 环（有带余除法），因此是 PID，因此是 UFD。
- \(F[x]\) 中不可约多项式对应极大理想（在 PID 中）。

### 不可约性判别法

**Eisenstein 判别法**：
设 \(f(x)=a_nx^n+\cdots+a_0\in\mathbb Z[x]\)。若存在素数 \(p\) 满足：
- \(p\mid a_i\ (i=0,\ldots,n-1)\)。
- \(p\nmid a_n\)。
- \(p^2\nmid a_0\)。

则 \(f(x)\) 在 \(\mathbb Q[x]\) 中不可约。

例：\(x^4+2x^3+2x+2\)，取 \(p=2\)，满足条件，在 \(\mathbb Q\) 上不可约。

**模 \(p\) 约化法**：
将系数模素数 \(p\)，若模 \(p\) 后不可约，则原多项式不可约。

**有理根检验**：
若 \(f(x)=a_nx^n+\cdots+a_0\in\mathbb Z[x]\) 有有理根 \(\frac{r}{s}\)（既约），则 \(r\mid a_0\)，\(s\mid a_n\)。

## 域扩张入门

### 扩张的基本概念

- 若 \(F\subseteq K\) 且均为域，则称 \(K/F\) 为域扩张。
- **扩张次数**：\([K:F]=\dim_F K\)（作为 \(F\)-向量空间）。
- **次数公式**：若 \(F\subseteq L\subseteq K\)，则 \([K:F]=[K:L][L:F]\)。

### 代数元与超越元

- \(\alpha\) 在 \(F\) 上**代数**：存在非零多项式 \(f\in F[x]\) 使 \(f(\alpha)=0\)。
- 否则称 \(\alpha\) 在 \(F\) 上**超越**。

### 极小多项式

若 \(\alpha\) 在 \(F\) 上代数：
- 极小多项式是次数最低的首一多项式 \(m_\alpha(x)\in F[x]\) 满足 \(m_\alpha(\alpha)=0\)。
- \(m_\alpha(x)\) 在 \(F[x]\) 中不可约。
- \([F(\alpha):F]=\deg m_\alpha\)。

### 单扩张结构

\[
F(\alpha)\cong F[x]/(m_\alpha(x)).
\]

### 有限域基本结论

- 有限域的阶必为素数幂：\(|\mathbb F|=p^n\)。
- 对每个素数幂 \(p^n\)，存在唯一的 \(p^n\) 阶域（同构意义下），记为 \(\mathbb F_{p^n}\)。
- \(\mathbb F_{p^n}^\times\) 是循环群（乘法群）。
- \(\mathbb F_{p^n}\) 是 \(x^{p^n}-x\) 在 \(\mathbb F_p\) 上的分裂域。

## 经典例题精讲

### 例 1：证明子群

设 \(G\) 为群，\(H,K\le G\)。证明 \(H\cap K\le G\)。

**证明**：
1. **非空**：\(e\in H\) 且 \(e\in K\)（子群含单位元），故 \(e\in H\cap K\)，非空。
2. **封闭性**：任取 \(a,b\in H\cap K\)。
   - \(a,b\in H\) 且 \(H\le G\)，故 \(ab^{-1}\in H\)。
   - \(a,b\in K\) 且 \(K\le G\)，故 \(ab^{-1}\in K\)。
   - 因此 \(ab^{-1}\in H\cap K\)。
3. 由于集非空且对 \(ab^{-1}\) 封闭，\(H\cap K\le G\)。

**注**：并集 \(H\cup K\) 一般不是子群，反例：\(G=\mathbb Z_6\)，\(H=\{[0],[3]\}\)，\(K=\{[0],[2],[4]\}\)，则 \(H\cup K\) 对加法不封闭（\(3+2=5\notin H\cup K\)）。

### 例 2：Sylow 定理 — 判断群非单

证明阶为 56 的群不是单群。

**证明**：
- \(56=2^3\cdot7=8\cdot7\)。
- **n₇**：\(n_7\equiv1\pmod7\)，\(n_7\mid8\)。可能值：\(1,8\)。
- 若 \(n_7=1\)，Sylow 7-子群正规，非单群。✓
- 若 \(n_7=8\)：8 个 Sylow 7-子群，每群有 6 个 7 阶元。共 \(8\times6=48\) 个 7 阶元。
- 剩余 \(56-48=8\) 个元素构成唯一的 Sylow 2-子群（阶 8）。
- 因唯一，该 Sylow 2-子群正规，非单群。✓
- 两种情况下 \(G\) 均非单。

### 例 3：证明商环是域

证明在 \(\mathbb Z[x]\) 中，理想 \(I=(x,2)\) 是极大理想，从而 \(\mathbb Z[x]/(x,2)\) 是域。

**证明**：
1. 考虑同态 \(\varphi:\mathbb Z[x]\to\mathbb Z_2\)，\(\varphi(f(x))=f(0)\bmod2\)。
   - \(\varphi\) 是满射（常数多项式 \(0,1\) 映到 \(\mathbb Z_2\) 的两个元素）。
2. 核：\(\ker\varphi=\{f\in\mathbb Z[x]:f(0)\equiv0\pmod2\}=\{f:f(0)\text{ 为偶数}\}\)。
   - 这等于是所有常数项为偶数的多项式。
   - 即 \(\ker\varphi=(x,2)\)（由 \(x\) 和 \(2\) 生成的理想）。
3. 由第一同构定理：\(\mathbb Z[x]/(x,2)\cong\mathbb Z_2\)，而 \(\mathbb Z_2\) 是域。
4. 因此 \((x,2)\) 是极大理想。

### 例 4：Eisenstein 判别法

证明 \(f(x)=x^4+4x^3+6x^2+4x+2\) 在 \(\mathbb Q\) 上不可约。

**证明**：
1. \(f(x)=(x+1)^4+1\)（注意到系数是二项式系数）。检查 Eisenstein：
   - 取 \(p=2\)。
   - \(a_4=1\)（不被 2 整除 ✓）
   - \(a_3=4,\ a_2=6,\ a_1=4,\ a_0=2\)（均被 2 整除 ✓）
   - \(a_0=2\)（不被 \(4\) 整除 ✓）
2. 三个条件满足，由 Eisenstein 判别法，\(f(x)\) 在 \(\mathbb Q\) 上不可约。

### 例 5：求极小多项式和扩张次数

求 \(\alpha=\sqrt{2}+\sqrt{3}\) 在 \(\mathbb Q\) 上的极小多项式，并求 \([\mathbb Q(\alpha):\mathbb Q]\)。

**解**：
1. 设 \(\alpha=\sqrt2+\sqrt3\)。
2. \(\alpha^2=2+3+2\sqrt6=5+2\sqrt6\)。
3. \((\alpha^2-5)^2=(2\sqrt6)^2=24\)。
4. \(\alpha^4-10\alpha^2+25=24\)，得 \(\alpha^4-10\alpha^2+1=0\)。
5. \(m_\alpha(x)=x^4-10x^2+1\)（可通过 Eisenstein 或其他方法验证不可约）。
6. 因此 \([\mathbb Q(\alpha):\mathbb Q]=\deg m_\alpha=4\)。

### 例 6：循环群生成元

求 \(\mathbb Z_{18}\) 的所有生成元。

**解**：
1. \(\mathbb Z_{18}\) 中 \([a]\) 是生成元当且仅当 \(\gcd(a,18)=1\)。
2. 1 到 18 中与 18 互素的数：\(1,5,7,11,13,17\)。
3. 共 \(\varphi(18)=18(1-1/2)(1-1/3)=6\) 个。
4. 生成元：\([1],[5],[7],[11],[13],[17]\)。

### 例 7：证明正规子群

设 \(G\) 为群，\(H\le G\) 且 \([G:H]=2\)。证明 \(H\trianglelefteq G\)。

**证明**：

1. 因 \([G:H]=2\)，存在两个左陪集：\(H\) 和 \(aH\)（\(a\notin H\)），且 \(G=H\cup aH\)。

2. 同理，存在两个右陪集：\(H\) 和 \(Ha\)，\(G=H\cup Ha\)。

3. 对任意 \(g\in G\)：
   - 若 \(g\in H\)，则 \(gH=H=Hg\)（因为 \(H\) 是子群）。
   - 若 \(g\notin H\)，则 \(g\in aH\)，即 \(g=ah\)。同时 \(g\) 也不能在 \(H\) 中，故 \(g\in Ha\)（因为只有两个右陪集，\(g\notin H\Rightarrow g\in Ha\)）。
   - 因此 \(gH=aH=Ha=Hg\)（两个陪集的情况一致）。

4. 对任意 \(g\in G\) 均有 \(gH=Hg\)，故 \(H\trianglelefteq G\)。

**推论**：指数为 2 的子群必为正规子群。这个结论在 Sylow 定理和群作用分析中经常用到。

**注意**：这个结论在考试中可以直接引用，但要理解证明。

### 例 8：商群的构造

设 \(G=\mathbb Z_{12}\)（加法群），\(H=\langle[4]\rangle=\{[0],[4],[8]\}\)。求商群 \(G/H\) 的元素和运算表。

**解**：

1. **验证正规性**：\(\mathbb Z_{12}\) 是阿贝尔群，所有子群都正规。✓

2. **写出所有陪集**：
   \[
   \begin{aligned}
   0+H&=\{[0],[4],[8]\}=H\\
   1+H&=\{[1],[5],[9]\}\\
   2+H&=\{[2],[6],[10]\}\\
   3+H&=\{[3],[7],[11]\}
   \end{aligned}
   \]

3. **商群结构**：\(G/H=\{H,1+H,2+H,3+H\}\)，共有 \(|G|/|H|=12/3=4\) 个元素。

4. **运算**（以陪集加法为例）：
   \[
   (1+H)+(2+H)=3+H,\quad (2+H)+(2+H)=4+H=H
   \]

5. **判断同构类型**：4 阶群只有 \(\mathbb Z_4\) 或 Klein 四元群。
   - \((1+H)+(1+H)=2+H\neq H\)（不是 2 阶元）
   - \((1+H)+(1+H)+(1+H)+(1+H)=4+H=H\)（是 4 阶元）
   - 因此 \(G/H\cong\mathbb Z_4\)。

**答案**：\(G/H\cong\mathbb Z_4\)，生成元为 \(1+H\)。

### 例 9：第一同构定理的应用

定义 \(\varphi:\mathbb Z\to\mathbb Z_n\) 为 \(\varphi(k)=[k]_n\)（取模 \(n\) 的余数类）。利用第一同构定理证明 \(\mathbb Z/n\mathbb Z\cong\mathbb Z_n\)。

**证明**：

1. \(\varphi\) 是群同态（加法保运算）：
   \[
   \varphi(a+b)=[a+b]_n=[a]_n+[b]_n=\varphi(a)+\varphi(b)
   \]

2. \(\varphi\) 是满射：对任意 \([k]_n\in\mathbb Z_n\)，取 \(k\in\mathbb Z\)，\(\varphi(k)=[k]_n\)。

3. 求核：
   \[
   \ker\varphi=\{k\in\mathbb Z:\varphi(k)=[0]_n\}=\{k\in\mathbb Z:n\mid k\}=n\mathbb Z
   \]

4. 第一同构定理：
   \[
   \mathbb Z/\ker\varphi\cong\operatorname{Im}\varphi
   \]
   即 \(\mathbb Z/n\mathbb Z\cong\mathbb Z_n\)。

**注**：这就是为什么 \(\mathbb Z_n\) 和 \(\mathbb Z/n\mathbb Z\) 在教材中经常混用——它们是同构的。

### 例 10：证明理想

在环 \(\mathbb Z[x]\) 中，令 \(I=\{f(x)\in\mathbb Z[x]:f(0)\text{ 是偶数}\}\)。证明 \(I\) 是理想，并求生成元。

**证明**：

1. **加法子群**：若 \(f(0),g(0)\) 均为偶数，则 \(f(0)-g(0)\) 也是偶数，所以 \(I\) 对减法封闭。零多项式 \(0\in I\)（\(0\) 是偶数）。

2. **吸收性**：任取 \(f\in I\)（\(f(0)\) 偶），\(r\in\mathbb Z[x]\)。
   - \((rf)(0)=r(0)f(0)\)。由于 \(f(0)\) 是偶数，\(r(0)f(0)\) 也是偶数。
   - 因此 \(rf\in I\)。
   - \(\mathbb Z[x]\) 是交换环，左吸收 = 右吸收。✓

3. **生成元**：
   - \(x\in I\)（因为 \(x\) 在 \(x=0\) 处取值为 0，是偶数）
   - \(2\in I\)（常数多项式 2 在 0 处取值为 2，是偶数）
   - 任何 \(f(x)\in I\) 可写成 \(f(x)=a_0+x\cdot g(x)\)，其中 \(a_0\) 为偶数。
   - 令 \(a_0=2k\)，则 \(f(x)=x\cdot g(x)+2k\)。
   - 因此 \(I=(x,2)\)，由 \(x\) 和 \(2\) 生成。

**答案**：\(I=(x,2)\)，这是 \(\mathbb Z[x]\) 中不是主理想的典型例子。

### 例 11：Sylow 定理 — 72 阶群非单

证明阶为 72 的群不是单群。

**证明**：

- \(72=2^3\cdot3^2=8\cdot9\)。

**分析 n₃**：\(n_3\equiv1\pmod{3}\)，\(n_3\mid8\)。可能值：\(1,4\)。
- 若 \(n_3=1\)，Sylow 3-子群唯一，正规，非单群。✓

**分析 n₂**：\(n_2\equiv1\pmod{2}\)，\(n_2\mid9\)。可能值：\(1,3,9\)。
- 若 \(n_2=1\)，Sylow 2-子群唯一，正规，非单群。✓

**剩余情况**：\(n_3=4\) 且 \(n_2=3\) 或 \(n_2=9\)。

若 \(n_3=4\)，考虑 \(G\) 在 4 个 Sylow 3-子群集合上的共轭作用：
- 存在同态 \(\varphi:G\to S_4\)。
- \(|G|=72\)，\(|S_4|=24\)。
- \(\ker\varphi\neq\{e\}\)（因为 \(72\nmid24\)，\(G/\ker\varphi\cong\operatorname{Im}\varphi\le S_4\)，所以 \(|G/\ker\varphi|\le24\)）。
- 若 \(\ker\varphi=G\)，则每个 Sylow 3-子群都正规，矛盾。
- 因此 \(\{e\}\subsetneq\ker\varphi\subsetneq G\)，\(\ker\varphi\) 是非平凡正规子群。非单群。✓

**所有情况均非单群**，得证。

### 例 12：轨道-稳定子定理应用

设 \(G\) 为有限群，\(H\le G\)。考虑 \(G\) 在左陪集集合 \(G/H\) 上的左乘作用：
\[
g\cdot (xH)=(gx)H.
\]
求稳定子和轨道，并利用轨道-稳定子定理推出 Lagrange 定理。

**解**：

1. **轨道**：对陪集 \(xH\)，
   \[
   G\cdot(xH)=\{gxH:g\in G\}=G/H\quad\text{（全体陪集）}
   \]
   作用是可迁的（只有一个轨道），轨道大小 = \([G:H]\)。

2. **稳定子**：
   \[
   G_{xH}=\{g\in G:gxH=xH\}=\{g\in G:x^{-1}gx\in H\}=xHx^{-1}
   \]
   即 \(xH\) 的稳定子是 \(H\) 的共轭子群 \(xHx^{-1}\)。

3. **轨道-稳定子定理**：
   \[
   |G\cdot(xH)|=[G:G_{xH}]\quad\Rightarrow\quad [G:H]=[G:xHx^{-1}]
   \]

4. 取 \(x=e\)，\(|G\cdot H|=[G:H]\)，\(G_H=H\)。由轨道-稳定子定理：
   \[
   |G|/|H|=[G:H]\quad\Rightarrow\quad |G|=|H|\cdot[G:H]
   \]
   这正是 **Lagrange 定理**。

**启示**：轨道-稳定子定理是 Lagrange 定理的推广，适用于所有群作用。

### 例 13：Galois 群计算

求 \(\mathbb Q(\sqrt{2},\sqrt{3})/\mathbb Q\) 的 Galois 群并列出所有中间域。

**解**：

1. **扩张次数**：
   - \([\mathbb Q(\sqrt{2}):\mathbb Q]=2\)（极小多项式 \(x^2-2\)）
   - \([\mathbb Q(\sqrt{2},\sqrt{3}):\mathbb Q(\sqrt{2})]\le2\)（极小多项式 \(x^2-3\) 在 \(\mathbb Q(\sqrt{2})\) 上是否可约？）
   - 若 \(\sqrt{3}\in\mathbb Q(\sqrt{2})\)，则 \(\sqrt{3}=a+b\sqrt{2}\)，平方得 \(3=a^2+2b^2+2ab\sqrt{2}\)。
   - 因 \(\sqrt{2}\notin\mathbb Q\)，须 \(2ab=0\)。若 \(b=0\)，\(3=a^2\) 无理解。若 \(a=0\)，\(3=2b^2\) 无理解。故 \(\sqrt{3}\notin\mathbb Q(\sqrt{2})\)。
   - 因此 \([\mathbb Q(\sqrt{2},\sqrt{3}):\mathbb Q]=4\)。

2. **Galois 群**：扩张是正规+可分（特征 0），故为 Galois 扩张。自同构由 \(\sqrt{2}\mapsto\pm\sqrt{2}\)，\(\sqrt{3}\mapsto\pm\sqrt{3}\) 决定。
   \[
   \operatorname{Gal}(\mathbb Q(\sqrt{2},\sqrt{3})/\mathbb Q)=\{1,\sigma,\tau,\sigma\tau\}\cong\mathbb Z_2\times\mathbb Z_2
   \]
   其中：
   - \(\sigma:\sqrt{2}\mapsto-\sqrt{2},\ \sqrt{3}\mapsto\sqrt{3}\)
   - \(\tau:\sqrt{2}\mapsto\sqrt{2},\ \sqrt{3}\mapsto-\sqrt{3}\)
   - \(\sigma\tau:\sqrt{2}\mapsto-\sqrt{2},\ \sqrt{3}\mapsto-\sqrt{3}\)

3. **子群 ↔ 中间域对应**（Galois 基本定理）：

   | 子群 | 不动域 |
   |------|--------|
   | \(\{1\}\) | \(\mathbb Q(\sqrt{2},\sqrt{3})\) |
   | \(\{1,\sigma\}\) | \(\mathbb Q(\sqrt{3})\) |
   | \(\{1,\tau\}\) | \(\mathbb Q(\sqrt{2})\) |
   | \(\{1,\sigma\tau\}\) | \(\mathbb Q(\sqrt{6})\) |
   | \(\{1,\sigma,\tau,\sigma\tau\}\) | \(\mathbb Q\) |

4. 三个真中间域：\(\mathbb Q(\sqrt{2})\)、\(\mathbb Q(\sqrt{3})\)、\(\mathbb Q(\sqrt{6})\)。

**答案**：Galois 群 \(\cong\mathbb Z_2\times\mathbb Z_2\)（Klein 四元群），3 个真中间域。

## 公式卡片 — 抽象代数必背

### 群论核心公式

**群公理**（非空 \(G\)，二元运算 \(*\)）：
\[
\forall a,b\in G:ab\in G;\quad\forall a,b,c\in G:(ab)c=a(bc);\quad\exists e\in G:ae=ea=a;\quad\forall a\in G,\exists a^{-1}:aa^{-1}=a^{-1}a=e
\]

**子群判别法**：
\[
H\le G\iff H\neq\varnothing\text{ 且 }\forall a,b\in H,\ ab^{-1}\in H
\]

**Lagrange 定理**：
\[
|G|=|H|\cdot[G:H]
\]

**元素阶整除群阶**：
\[
|a|\ \big|\ |G|
\]

**陪集划分**：
\[
G=\bigcup_{i=1}^{k}a_iH,\quad a_iH\cap a_jH=\varnothing\ (i\neq j)
\]

**正规子群判定**：
\[
N\trianglelefteq G\iff\forall g\in G,\ gNg^{-1}=N\iff gN=Ng\ (\forall g\in G)
\]

**第一同构定理**：
\[
G/\ker\varphi\cong\operatorname{Im}\varphi
\]

**类方程**：
\[
|G|=|Z(G)|+\sum_{i=1}^{r}[G:C_G(g_i)]
\]

**轨道-稳定子定理**：
\[
|G\cdot x|=[G:G_x]=\frac{|G|}{|G_x|}
\]

### Sylow 定理（记牢三个）

\[
\begin{aligned}
\text{第一：}&\ |G|=p^a\cdot m,\ p\nmid m,\ \exists P\le G,\ |P|=p^a\\
\text{第二：}&\ \text{所有 Sylow }p\text{-子群两两共轭}\\
\text{第三：}&\ n_p\equiv1\pmod{p},\quad n_p\mid m,\quad n_p=[G:N_G(P)]
\end{aligned}
\]

### 环论核心对应

\[
R/P\text{ 是整环}\iff P\text{ 是素理想}
\]
\[
R/M\text{ 是域}\iff M\text{ 是最大理想}
\]
\[
\text{Euclidean 环}\implies\text{PID}\implies\text{UFD}
\]

### 域扩张公式

**次数公式**：
\[
[K:F]=[K:L][L:F]
\]

**单扩张结构**：
\[
F(\alpha)\cong F[x]/(m_\alpha(x)),\quad [F(\alpha):F]=\deg m_\alpha
\]

**有限域阶**：
\[
|\mathbb{F}_{p^n}|=p^n,\quad \mathbb{F}_{p^n}^\times\text{ 是循环群},\quad \mathbb{F}_{p^n}\text{ 是 }x^{p^n}-x\text{ 在 }\mathbb{F}_p\text{ 上的分裂域}
\]

### 不可约性判别

**Eisenstein 判别法**：\(\exists\) 素数 \(p\) 使 \(p\mid a_i\ (i<n),\ p\nmid a_n,\ p^2\nmid a_0\implies f(x)\) 在 \(\mathbb{Q}\) 上不可约。

**有理根检验**：\(f(x)=\sum a_i x^i\in\mathbb{Z}[x]\) 有有理根 \(\frac{r}{s}\implies r\mid a_0,\ s\mid a_n\)。

**模 \(p\) 约化法**：\(f(x)\bmod p\) 不可约 \(\implies f(x)\) 在 \(\mathbb{Z}[x]\) 不可约。

## UFD、PID、Euclidean 环的链

### 逐层关系

\[
\text{Euclidean 环}\implies\text{PID}\implies\text{UFD}
\]

**Euclidean 环**：存在赋值函数 \(\delta:R\setminus\{0\}\to\mathbb N\)，使 \(\forall a,b\neq0,\exists q,r\) 满足 \(a=bq+r\) 且 \(r=0\) 或 \(\delta(r)<\delta(b)\)。

例子：\(\mathbb Z\)（\(\delta(n)=|n|\)）、域上的多项式环 \(F[x]\)（\(\delta(f)=\deg f\)）、Gauss 整数环 \(\mathbb Z[i]\)（\(\delta(a+bi)=a^2+b^2\)）。

**PID（主理想整环）**：每个理想都是主理想（由一个元素生成）。

**UFD（唯一分解整环）**：每个非零非单位元素可唯一分解为不可约元乘积。

### 关键反例
- \(\mathbb Z[x]\) 是 UFD 但不是 PID（理想 \((2,x)\) 不是主理想）
- \(F[x,y]\) 是 UFD 但不是 PID
- \(\mathbb Z[\sqrt{-5}]\) 不是 UFD：\(6=2\cdot3=(1+\sqrt{-5})(1-\sqrt{-5})\)

## 模论入门

### 基本概念

左 \(R\)-模：类比向量空间，标量来自环 \(R\) 而非域。

**子模、商模、模同态**与群/环理论平行。

**自由模**：有基的模。有限生成自由 \(R\)-模 \(\cong R^n\)。

### 模与 Abel 群

\(\mathbb Z\)-模 = Abel 群（\(n\cdot x=x+\cdots+x\ (n\text{ 次})\)）

### 模的张量积（略）

## 更多 Galois 理论

### Galois 基本定理

若 \(E/F\) 是有限 Galois 扩张，则存在一一对应：
\[
\{\text{中间域 }K\mid F\subseteq K\subseteq E\}\longleftrightarrow\{\text{子群 }H\mid H\le\operatorname{Gal}(E/F)\}
\]
\[
K\mapsto\operatorname{Gal}(E/K),\quad H\mapsto E^H(\text{不动域})
\]

### 经典例子

**\(\mathbb Q(\sqrt{2},\sqrt{3})/\mathbb Q\)**：
- Galois 群 \(\cong\mathbb Z_2\times\mathbb Z_2\)（Klein 四元群）
- 3 个真中间域：\(\mathbb Q(\sqrt{2}),\mathbb Q(\sqrt{3}),\mathbb Q(\sqrt{6})\)

**有限域的 Galois 群**：
- \(\operatorname{Gal}(\mathbb F_{p^n}/\mathbb F_p)\cong\mathbb Z_n\)，由 Frobenius 自同构 \(x\mapsto x^p\) 生成

### 正规闭包与可分扩张

- **可分扩张**：极小多项式无重根
- **正规扩张**：不可约多项式若有根在扩域中，则所有根都在
- **Galois 扩张** = 正规 + 可分 + 有限

## 考前背诵清单（完整版）

- 群、子群、正规子群、商群、同态、核。
- Lagrange 定理和元素阶整除群阶。
- 第一同构定理。
- 环、理想、商环、整环、域。
- 最大理想对应域，素理想对应整环。
- **Sylow 三定理**：存在、共轭、\(n_p\equiv1\pmod{p}\) 且 \(n_p\mid m\)。
- **类方程**：\(|G|=|Z(G)|+\sum[G:C_G(g_i)]\)。
- **轨道-稳定子定理**。
- **Eisenstein 判别法**条件和用法。
- **有限域阶必为 \(p^n\)**，乘法群循环。

