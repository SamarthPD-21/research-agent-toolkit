# 真实示例输出：中文文献周报邮件

> 这是用户提供的真实邮件 demo 示例，用于展示 Research Agent Toolkit 预期生成的中文周报结构、信息密度和核验标准。正式运行时，所有条目仍应来自可核验来源；不得编造论文、链接、权重、代码或许可证状态。

## 邮件标题

```text
[NeuroPET-MRI Weekly] MRI-to-PET / Tau PET / CLIP 文献更新 - 2026-04-29
```

---

## 一、本周期最重要结论

本次按既定流程先检索近 7 天（2026-04-22 至 2026-04-29），再在 MRI-to-PET / Tau PET / Alzheimer’s disease（AD）强相关结果不足时扩展到近 30 天（2026-03-30 至 2026-04-29）。

MRI-to-PET / Tau PET / AD 方向：本周期没有发现“近 30 天内新发布或有明确更新、且与 MRI-to-PET / Tau PET / AD 直接强相关、并能完成标题/作者/来源/链接一致性核验”的新增高价值论文达到默认汇报阈值（相关性评分 >= 70）。这一点需要如实说明，不建议为了凑数降低标准。

医学图像大模型 / 医学视觉语言模型方向：近 30 天有 4 个值得关注的更新，其中最值得优先下载代码或权重尝试的是 MedGemma 1.5 和 uAI-NEXUS-MedVLM；最值得优先阅读全文的是 MedP-CLIP 和 OpenMedQ。

对当前课题最有迁移价值的不是“泛医疗多模态”本身，而是三类方法学信号：

- 面向局部病灶/脑区的 region-aware 对齐（MedP-CLIP）；
- 用开放数据混合训练出可复用视觉编码器（OpenMedQ）；
- 能直接处理 3D CT/MRI 的开放多模态基座（MedGemma 1.5）。

热度高但对 MRI-to-PET / Tau PET / AD 迁移价值有限的工作：uAI-NEXUS-MedVLM。它的开放度很高，但核心场景是医疗视频/手术视频，不是神经影像；更适合作为“训练范式和奖励设计”参考，而不是当前课题的第一优先级下载对象。

---

## 二、MRI-to-PET / Tau PET / Alzheimer’s disease 强相关论文

本周期在近 30 天窗口（2026-03-30 至 2026-04-29）内，未发现同时满足以下条件的新增条目：

- 与 MRI-to-PET、Tau PET、Amyloid PET、AD/MCI 直接强相关；
- 来源与元信息可核验一致；
- 确属本周期新增或明确更新；
- 相关性评分 >= 70。

结论：本周期该方向“强相关新增论文不足”，建议不要降低收录标准。与当前课题真正直接相关、但不在本周期窗口内的工作，我放到第四部分作为间接启发保留。

---

## 三、医学图像大模型 / 医学视觉语言模型更新

### [1] MedGemma 1.5 Technical Report / google/medgemma-1.5-4b-it

- 类型：technical report + Hugging Face model
- 相关性评分：88/100
- 可复用性评分：95/100
- 论文标题：MedGemma 1.5 Technical Report
- 模型名称：MedGemma 1.5 4B IT
- 作者：Google Research 团队
- 机构：Google Research
- 发布时间 / 更新时间：技术报告发表于 2026-04-06；Hugging Face 模型卡显示 2026-01-13 发布 MedGemma 1.5，2026-01-23 更新 generation config
- 链接：
  - Paper：https://arxiv.org/abs/2604.05081
  - arXiv：https://arxiv.org/abs/2604.05081
  - GitHub：https://github.com/google-health/medgemma
  - Hugging Face：https://huggingface.co/google/medgemma-1.5-4b-it
  - Project page：https://research.google/blog/next-generation-medical-image-interpretation-with-medgemma-15-and-medical-speech-to-text-with-medasr/
- 模态：CT、MRI、胸片、病理全视野图像、皮肤、眼底、医学文档/EHR
- 数据集：模型卡可见 CT-RATE 及多类医学图像/医学文档来源；另含内部 CT/MRI 数据集说明
- 模型结构：基于 Gemma 3 的多模态生成模型
- 训练目标：医学图像理解、医学文档理解、多模态问答与生成
- 下游任务：3D CT/MRI 分类、胸片报告、定位、多时点胸片分析、医学问答
- 是否公开代码：是
- 是否公开权重：是
- License：Apache 2.0；Google 博客明确说明可用于 research and commercial use
- 中文总结：这是目前近 30 天里最值得实际下载尝试的开放医学多模态模型之一。关键价值不只是“医学版 Gemma”，而是它已经把 3D CT/MRI、WSI、医学文档放进同一开放体系，且权重、代码、模型卡都在。
- 与 BiomedCLIP 的关系：不是纯 BiomedCLIP 式对比学习编码器，而是更偏生成式多模态模型；但其视觉侧可视为比 BiomedCLIP 更接近“可直接干活”的医学多模态底座。
- 对 MRI-to-PET / Tau PET / AD 诊断预测的潜在价值：对 AD 神经影像最直接的价值在于它已经明确支持 MRI/CT 类 3D 体数据，适合尝试做 MRI + 文本/临床变量联合提示、MRI 表征抽取、弱监督图文对齐和后续 task adaptation。
- 它是不是一个类似 BiomedCLIP 的医学图像-文本预训练模型：不完全是；它是更通用的医学多模态生成模型，而非纯 CLIP 编码器。
- 它是否真的公开了模型权重：是，Hugging Face 可见。
- 它是否真的公开了代码：是，GitHub 可见。
- 它训练用的图像模态是什么：胸片、CT、MRI、病理等。
- 它能否迁移到 MRI-to-PET 或 AD 神经影像任务：能，尤其适合作为 3D 医学多模态底座或指令微调起点。
- 它对当前课题的最直接启发是什么：说明“开放 3D 医学多模态模型”已经开始覆盖 MRI 场景，后续可考虑把神经影像文本描述、脑区先验、临床变量接进统一指令框架。
- 是否值得下载代码或模型尝试：强烈建议
- 备注：已核到技术报告、官方博客、HF 模型卡；权重和许可状态清晰。

### [2] MedP-CLIP: Medical CLIP with Region-Aware Prompt Integration

- 类型：arXiv preprint
- 相关性评分：90/100
- 可复用性评分：62/100
- 论文标题：MedP-CLIP: Medical CLIP with Region-Aware Prompt Integration
- 模型名称：MedP-CLIP
- 作者：Jiahui Peng, He Yao, Jingwen Li, Yanzhou Su, Sibo Ju, Yujie Lu, Jin Ye, Hongchun Lu, Xue Li, Lincheng Jiang, Min Zhu, Junlong Cheng
- 机构：当前仅读取 arXiv 摘要页，机构未在摘要页完整展开
- 发布时间 / 更新时间：2026-04-13（arXiv v1）
- 链接：
  - Paper：https://arxiv.org/abs/2604.11197
  - arXiv：https://arxiv.org/abs/2604.11197
  - GitHub：未确认到官方公开代码
  - Hugging Face：未确认到官方公开权重
  - Project page：未确认到官方项目页
- 模态：多模态医学图像，强调 region-level annotation 与多种 prompt 形式（点、框、mask）
- 数据集：摘要页称预训练集含 640 万+ 医学图像、9730 万+ 区域级标注
- 模型结构：region-aware medical VLM / CLIP 类视觉骨干
- 训练目标：细粒度图像-文本对齐 + 区域提示融合
- 下游任务：zero-shot recognition、interactive segmentation、支持多模态大模型
- 是否公开代码：未确认
- 是否公开权重：未确认
- License：未确认
- 中文总结：这是近 30 天里和你课题“方法学迁移”最贴的一篇。它不是普通 medical CLIP，而是显式把区域提示融入视觉-语言对齐，特别适合迁移到脑区级 tau/amyloid burden、Braak staging、局部病灶引导提示等神经影像任务。
- 与 BiomedCLIP 的关系：是，属于更接近“BiomedCLIP 下一步”的工作，可看作在 medical CLIP 基础上把全局对齐推进到 region-aware 对齐。
- 对 MRI-to-PET / Tau PET / AD 诊断预测的潜在价值：非常高。你后续若做 MRI-to-TauPET、脑区级生成或脑区级图文对齐，MedP-CLIP 的 region prompt integration 思路比单纯 global CLIP 更贴近需求。
- 它是不是一个类似 BiomedCLIP 的医学图像-文本预训练模型：是，而且更强调区域级提示和局部语义。
- 它是否真的公开了模型权重：目前未核到。
- 它是否真的公开了代码：目前未核到。
- 它训练用的图像模态是什么：摘要页显示为跨疾病、跨模态医学图像，但未在摘要页细分到每个模态。
- 它能否迁移到 MRI-to-PET 或 AD 神经影像任务：能，尤其适合做脑区级 prompt、局部对齐、局部监督。
- 它对当前课题的最直接启发是什么：把“脑区/病灶/ROI”作为 prompt 条件，而不是只做整脑级别图文对齐。
- 是否值得我进一步阅读 / 尝试复现：强烈建议阅读全文；暂不建议立刻复现，因为代码与权重尚未核实。
- 备注：仅 arXiv，未同行评审；仅读取摘要页，代码/权重未确认。

### [3] OpenMedQ: Broad Open Pretraining for Medical Vision-Language Models

- 类型：conference submission（MIDL 2026 Short Paper, OpenReview）
- 相关性评分：84/100
- 可复用性评分：58/100
- 论文标题：OpenMedQ: Broad Open Pretraining for Medical Vision-Language Models
- 模型名称：OpenMedQ
- 作者：Halil Ibrahim Gulluk, Max Van Puyvelde, Olivier Gevaert
- 机构：Stanford University；Stanford University School of Medicine；Ghent University
- 发布时间 / 更新时间：2026-04-16（OpenReview）
- 链接：
  - Paper：https://openreview.net/forum?id=xD07n1BUnV
  - arXiv：未见
  - GitHub：未确认到官方代码仓库
  - Hugging Face：未确认到官方权重
  - Project page / Demo：https://openmedq.streamlit.app/
- 模态：pathology、radiology、microscopy，以及 text-only clinical QA
- 数据集：14 个 fully-open 数据集，总计约 335 万预训练样本
- 模型结构：LLaVA-style VLM；ViT-base（从 BiomedCLIP 初始化）+ LLaMA-7B + LoRA
- 训练目标：next-token prediction；构建 broad open medical VLM
- 下游任务：PathVQA、VQA-MED、分类迁移
- 是否公开代码：未确认
- 是否公开权重：否，文中明确写的是“upon acceptance”
- License：OpenReview 页面 CC BY 4.0；模型权重许可证未见
- 中文总结：这篇的核心价值不是单点指标，而是“用全开放数据混合训练出一个比 BiomedCLIP / PMC-CLIP / PubMedCLIP 更强的可迁移视觉编码器”。如果你后面想做神经影像 CLIP 或医学图文对齐，这是非常值得细读的训练配方型工作。
- 与 BiomedCLIP 的关系：非常直接。它的 vision encoder 以 BiomedCLIP 为初始化，并在更广的开放医学数据混合上继续训练。
- 对 MRI-to-PET / Tau PET / AD 诊断预测的潜在价值：适合借鉴“开放数据配方 + 统一下游评测”的路线，尤其可用于后续构建 neuroimaging-specific open CLIP/VLM。
- 它是不是一个类似 BiomedCLIP 的医学图像-文本预训练模型：部分是，但它更偏生成式 VLM；同时它的 encoder 比较适合当 BiomedCLIP 的开放扩展版思路参考。
- 它是否真的公开了模型权重：否，尚未真正公开，只是承诺 acceptance 后发布。
- 它是否真的公开了代码：当前未核到。
- 它训练用的图像模态是什么：病理、放射、显微图像。
- 它能否迁移到 MRI-to-PET 或 AD 神经影像任务：中等偏高，主要迁移的是训练范式和 encoder 预训练思路，而不是现成神经影像模型。
- 它对当前课题的最直接启发是什么：如果后续你想做“开放可复现的 neuro-CLIP / neuro-VLM”，OpenMedQ 的数据混合与评测组织方式很值得学。
- 是否值得我进一步阅读 / 尝试复现：建议阅读全文；暂不建议立刻下载复现，因为权重尚未正式开放。
- 备注：OpenReview 可读；PDF 中给出了公开 demo；权重尚未真正发布。

### [4] uAI-NEXUS-MedVLM-1.0a-7B-RL / MedGRPO

- 类型：Hugging Face model + dataset release + project/code release + CVPR 2026 paper
- 相关性评分：72/100
- 可复用性评分：92/100
- 论文标题：MedGRPO: Multi-Task Reinforcement Learning for Heterogeneous Medical Video Understanding
- 模型名称：uAI-NEXUS-MedVLM-1.0a-7B-RL
- 作者：模型卡列出论文作者为 Yuhao Su 等
- 机构：United Imaging Intelligence
- 发布时间 / 更新时间：2026-04-24 官方宣布开源；模型卡显示已接受 CVPR 2026
- 链接：
  - Paper：https://arxiv.org/abs/2512.06581
  - arXiv：https://arxiv.org/abs/2512.06581
  - GitHub：https://github.com/UII-AI/MedGRPO-Code
  - Hugging Face（model）：https://huggingface.co/UII-AI/uAI-NEXUS-MedVLM-1.0a-7B-RL
  - Hugging Face（dataset）：https://huggingface.co/datasets/UII-AI/MedVidBench
  - Project page：https://uii-ai.github.io/MedGRPO/
- 模态：医疗/手术视频
- 数据集：MedVidBench；模型卡显示训练用 51,505 balanced video-instruction pairs，测试集 6,245 samples
- 模型结构：Qwen2.5-VL-7B-Instruct 微调；SFT + GRPO
- 训练目标：医疗视频理解、多任务强化学习
- 下游任务：时序动作定位、时空定位、视频摘要、区域描述、手术技能评估等
- 是否公开代码：是
- 是否公开权重：是
- License：Apache 2.0
- 中文总结：这不是神经影像模型，但它是本周期开放度最高的医学多模态更新之一：权重、代码、基准、项目页都齐。真正值得看的不是视频本身，而是它把 RL 奖励设计、任务统一评测、HF 发布链路做得很完整。
- 与 BiomedCLIP 的关系：不是 BiomedCLIP 类图像-文本预训练模型，而是视频 VLM + RL。
- 对 MRI-to-PET / Tau PET / AD 诊断预测的潜在价值：直接价值有限；更像方法论参考，特别是 reward shaping、多任务统一 benchmark、从 SFT 到 RL 的两阶段训练。
- 它是不是一个类似 BiomedCLIP 的医学图像-文本预训练模型：不是。
- 它是否真的公开了模型权重：是。
- 它是否真的公开了代码：是。
- 它训练用的图像模态是什么：医疗视频/手术视频。
- 它能否迁移到 MRI-to-PET 或 AD 神经影像任务：直接迁移价值有限。
- 它对当前课题的最直接启发是什么：如果你后面考虑用 RL 或偏好优化来提升医学多模态模型的“临床有用性”，这个项目的训练与发布范式值得借鉴。
- 是否值得我进一步阅读 / 尝试复现：建议阅读；若只为当前 MRI-to-PET / AD 课题，暂不作为第一优先级复现对象。
- 备注：公开度高，但场景偏医疗视频，不是神经影像。

---

## 四、间接相关但可能有启发的论文或模型

### [1] RelA-Diffusion: Relativistic Adversarial Diffusion for Multi-Tracer PET Synthesis from Multi-Sequence MRI

- 相关性判断：非常高，但不在本周期窗口内；OpenReview 页面显示 2026-02-11 修改
- 为什么有启发：多序列 MRI（T1w + T2-FLAIR）到多 tracer PET 的扩散生成，非常贴近你关心的 MRI-to-PET 路线，而且明确提到 tau / amyloid / neuroinflammation 多 tracer 场景。
- 链接：https://openreview.net/forum?id=TXdKKABtWB

### [2] Machine learning prediction of tau-PET in Alzheimer’s disease using plasma, MRI, and clinical data

- 相关性判断：高，但发表于 2025-02，不在本周期窗口内
- 为什么有启发：如果你后面做 MRI-to-TauPET，不一定非要走纯生成；这篇更像“低成本变量预测 tau burden”的强基线，适合作为任务定义与评价参照。
- 链接：https://pubmed.ncbi.nlm.nih.gov/39985487/

### [3] MedCLIPSeg: Probabilistic Vision-Language Adaptation for Data-Efficient and Generalizable Medical Image Segmentation

- 相关性判断：方法上有启发，但最新 GitHub 提交为 2026-03-24，略早于本周期 30 天窗口
- 为什么有启发：它把 CLIP 用到医学图像分割，并显式做 uncertainty-aware 的跨模态适配。对脑区级引导、局部监督和 prompt 设计有借鉴价值。
- 链接：
  - Paper：https://arxiv.org/abs/2602.20423
  - GitHub：https://github.com/HealthX-Lab/MedCLIPSeg

---

## 五、未纳入内容与原因

### 1. MRI2PET: Realistic PET Image Generation from MRI for Automated Inference of Brain Atrophy and Alzheimer’s

- 原因：与课题高度相关，但 OpenReview 页面时间为 2025-09-19 / 2025-12-05，明显不在本周期 7 天或 30 天窗口内。
- 链接：https://openreview.net/forum?id=PMCD5pKglt

### 2. MedGPT-oss: Training a General-Purpose Vision-Language Model for Biomedicine

- 原因：工作本身值得关注，但 arXiv 时间为 2026-03-01，超出 30 天窗口；且本次检索中未核到官方权重/代码入口的稳定主链接，因此不放入本周期主列表。
- 链接：https://arxiv.org/abs/2603.00842

### 3. HiPro-CT: A Hierarchical Probabilistic Framework for 3D Medical Vision-Language Alignment

- 原因：2026-04-16 有更新，方法也不错，但核心场景是 chest CT；当前未核到代码/权重公开，且对 MRI-to-PET / AD 的直接迁移价值弱于 MedP-CLIP 与 MedGemma 1.5。
- 链接：https://openreview.net/forum?id=FrnSJeYO6v

### 4. MedVR: Annotation-Free Medical Visual Reasoning via Agentic Reinforcement Learning

- 原因：2026-04-11 有更新，但更偏 medical VQA / visual reasoning；对当前 MRI-to-PET / Tau PET / AD 课题的直接方法迁移价值不如 region-aware CLIP 与 3D 医学底座模型。
- 链接：https://openreview.net/forum?id=cK35kNVm5r

---

## 六、下周建议关注关键词

1. MRI-to-TauPET, tau PET synthesis, synthetic tau PET, tau burden estimation, Braak staging, ADNI tau PET MRI
2. MRI-to-PET, multi-tracer PET synthesis, amyloid PET synthesis, FDG-PET prediction, PET imputation, multimodal generation
3. Alzheimer’s disease, MCI conversion, cognitive decline prediction, plasma + MRI + tau PET, biomarker prediction
4. neuroimaging CLIP, brain MRI vision-language model, neuroimaging foundation model, report-supervised neuroimaging
5. region-aware medical CLIP, organ-aware / lesion-aware alignment, fine-grained medical image-text alignment
6. 3D medical VLM, CT/MRI volume language model, 3D radiology foundation model, MRI report grounding
7. medical open-weight multimodal model, Hugging Face model card, GitHub release, demo, benchmark, leaderboard

---

## 本周期优先级建议

### 最值得优先阅读全文

1. MedP-CLIP
2. OpenMedQ
3. MedGemma 1.5 Technical Report

### 最值得优先下载代码或权重尝试

1. MedGemma 1.5
2. uAI-NEXUS-MedVLM（仅建议借鉴开放发布链路与 RL 训练范式，不建议作为当前课题主线模型）

### 虽然热度高但对 MRI-to-PET / Tau PET / AD 迁移价值有限

1. uAI-NEXUS-MedVLM（视频方向）
2. MedVR（更偏医学视觉推理/VQA）

---

## 备注

- 本周 MRI-to-PET / Tau PET / AD 强相关新增确实偏少，以上结论是按高标准核验后得出。
- 如果下周仍然稀疏，建议增加“会议论文主页 / OpenReview rebuttal 后版本 / GitHub 新开源实现”的监控权重，以便更早捕捉真正可复现的更新。
