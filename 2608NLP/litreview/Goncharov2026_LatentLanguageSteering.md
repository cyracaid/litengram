# 📖 NLP 语言转向·CS 文献精读 — 2026-08-19

## 关键词: Language Steering, Latent Space, PCA, Unintended Code-Switching, PCA Language Direction

## Language Steering in Latent Space to Mitigate Unintended Code-Switching

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将（CS 缓解 + 语言转向——项目 CS 相关）
- **论文类型**: Methods + Empirical
- **domain**: nlp（多语言·语言转向）
- **阅读策略**: Standard
- **第一作者**: Andrey Goncharov | 俄/Steklov（Nikolai Kondusov, Alexey Zaytsev）
- **发表**: 2026 | Zapiski seminarov POMI | arXiv:2510.13849
- **venue**: arXiv:2510.13849
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2510.13849.pdf

### 📚 背景 / 核心

多语 LLM 常意外代码切换(非意图 CS)降可靠性；提出**潜在空间语言转向**——用 PCA 在平行翻译上找语言方向，沿轴 steer token 嵌入控语言身份；轻量推理期、极小平行数据；缓解 CS 并保语义。

### 🧠 关键概念

Latent-space language steering、PCA language direction、unintended code-switching mitigation。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | PCA 语言方向 steering 缓解非意图 CS | 【定义】轻量语言控制。【本文角色】方法。【论证关联】与 L7/LangFIR 同族；项目要控制"CS 输出语言"可用此 PCA 转向。 |
| 2 | 极小平行数据 | 【定义】低数据需求。呼应 LangFIR 单语 / L7 稀疏维度。 |

### 🔗 与你领域的关系

⚔️。项目要操纵/缓解 CS 输出语言时，PCA 潜在空间转向是轻量选项（与 L2 语言层、L6/L7 同族）。CS 主题域相关但非解离核心。

### 📄 摘要（一文）

用 PCA 在平行数据上找语言方向、steer token 嵌入控语言身份，缓解非意图代码切换、保语义、计算开销轻。
