# HKP4 编辑部 — 仓库工作规则

本文件每次会话自动加载，是硬约束，不是参考。

## 0. 第一条铁律（防止流程失忆）

凡涉及**撰写、改写、审阅、配图、发布**评论文章（新刊、下一篇、第二期皆算）：
**第一步必须调用 skill `hkp4-commentary-sop`**（位于 `~/.claude/skills/hkp4-commentary-sop/SKILL.md`），
按其行文 SOP（报章体裁、事实核查、配图流程、验收清单）执行。没有例外，不得凭记忆替代。

## 1. 发布授权

- 用户已点头内容（正文、配图、镜像稿）的**例行重新发布**：改完自检通过即直接 deploy，无须再次讨要点头；仅重大偏离（改立场表述、删已批 punchline、新文章首发）需当轮确认。改动先 `npm run build`，再 `npm run preview`（localhost:4321，日志 /tmp/hkp4-preview.log）给用户过目。
- 配图同权：图必须 `open <文件>` 打开给用户看，**用户点头才算定稿**；未点头的图不得入库。

## 2. GitHub 纪律：只示定稿

- `main` 永远只有一个提交。所有改动走：`git add -A && git commit --amend --no-edit && git push --force origin main`。
- 部署只用 `npm run deploy`（内部调 `scripts/deploy.sh`，gh-pages 强制单提交）。不得恢复 gh-pages 包的追加式推送。
- 任何改写历史的操作，先 `git bundle create` 全量备份。
- `node_modules/ dist/ .astro/` 不入库（.gitignore 已管，动 `git add -A` 前留意嵌套 git 仓库警告）。

## 3. 上线验证链（每次必跑）

1. s2t 繁体扫描无新增简体（可接受港用字：托/干/秘/克/咸/了/才/布）；「港製」出现次数 = 0。
2. `npm run build` 成功（2026-11-07 基线 21 页，新增文章页数会变）。
3. 上线后 curl 复验：中文文章 `/articles/<slug>/`（zh 无前缀），英文 `/en/articles/<slug>/`；GitHub Pages CDN 生效延迟 30–60 秒，先等再判。

## 4. 站定稿文案

- 站招（页脚 / OG / 关于页副题）：**以事實與邏輯深讀香港** / **reading Hong Kong in depth through facts and logic**。
- 门面不宣传「匿名」。关于页「我們為什麼匿名」答疑段保留（是答疑不是自夸）；donate 页「加密货币完全匿名」保留（功能描述）。
- 四透镜：繁榮 Prosperity · 推演 Projection · 前景 Prospect · 潛能 Potential。

## 5. 工具通道（2026-11-07 实测，坏通道勿再浪费轮次；2026-11-12 补 NovaMLX 条目）

- 云端图像生成只有 `google/gemini-3-pro-image` 可用；OpenRouter 图像（User not found，欠费）与 alibaba-cn（Invalid API-key）均不可用。
- websearch 工具欠费（402）；网络查询用 webfetch 或直接 curl。
- `*.gov.hk` 全站对本机反爬（统一 9018 字节拦截页）；大公文匯网可直接 curl。
- 本机 NovaMLX（`POST http://127.0.0.1:6590/v1/images/generations`，model `mzbac/Z-Image-Turbo-8bit`，key 见当轮会话）＝**头图固定生成通道**（2026-11-12 用户定），结果在 `data[0].b64_json`；单张 80–380 秒，免费。`google/gemini-3-pro-image` 降为备用（构图失控或 NovaMLX 不可用时）。OpenRouter 图像（User not found，欠费）与 alibaba-cn（Invalid API-key）仍不可用。
  - NovaMLX 尺寸坑：Z-Image 管线对每边 `max(size, 1024)` 抬升——16:9 唯一稳的档是 `2048x1152`（约 6.3 分/张）；`"16:9"` 字符串静默回落 1024²，`1344x768` 被抬成 1344×1024，`1920x1080` 报 PipelineError。16:9 图也可由方形图上下对称裁切得到。
