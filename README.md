# HKP4 — 香港的四個面向 · Four Lenses on Hong Kong

匿名的繁中 + 英文双语香港观察刊物。Astro 静态站,部署在 GitHub Pages,零成本。

四个面向:**繁榮 Prosperity · 推演 Projection · 前景 Prospect · 潛能 Potential**

## 日常发布流程

1. 用中文写文章:新建 `src/content/articles/zh/<slug>.md`(参考范例 `one-country-two-systems.md`;文件名即网址 slug,用小写英文加连字符);
2. 把中文版翻译成英文,存为**同名文件**放在 `src/content/articles/en/`(同名 = 自动互相关联、自动出现语言切换链接);
3. `npm run dev` 本地预览 http://localhost:4321;
4. `git add . && git commit && git push`(存档源码);
5. `npm run deploy` → 构建并推送到 `gh-pages` 分支,约 1 分钟上线。

### 文章 frontmatter 格式

```yaml
---
title: 文章標題(繁體)
description: 一句話摘要,用於列表頁和 SEO
pubDate: 2026-11-05
p: [prosperity]   # 从 prosperity / projection / prospect / potential 中选,可多选
draft: false      # true = 不发布
---
```

## 上线架构(已完成,2026-11-06)

- GitHub 账号 `hkp4desk`(邮箱 `hkp4desk@proton.me`),仓库 `hkp4desk.github.io`;
- Pages 部署方式:**Deploy from a branch → `gh-pages` / root**。
  (不用 GitHub Actions:`actions/deploy-pages` 在本账号持续 10 分钟超时,branch 部署 <1 分钟,已于 2026-11-06 实测);
- 推送凭据:仓库专用 deploy key `~/.ssh/hkp4_deploy`(SSH 别名 `github-hkp4`,读写,仅限本仓库);
- 每次发布:`npm run deploy`。

```bash
# 首次搭好时的命令存档
git init -b main
git remote add origin git@github-hkp4:hkp4desk/hkp4desk.github.io.git
git push -u origin main
npm install -D gh-pages && npm run deploy
# GitHub → Settings → Pages → Source: Deploy from a branch → gh-pages / (root)
```

## 上线前必须替换的占位符

| 位置 | 占位符 | 换成 | 状态 |
|---|---|---|---|
| `src/lib/ui.ts` | `patreon` 链接 | `https://www.patreon.com/c/hkp4` | ✅ 已替换 |
| `src/lib/ui.ts` | `email` | `hkp4desk@proton.me`(公开联系专用号) | ✅ 已替换 |
| `src/pages/donate.astro` + `en/donate.astro` | 三个加密货币地址 | Trust 钱包地址(bech32/base58check/EIP-55 校验通过) | ✅ 已替换 |

## 匿名纪律(每次发布前过一遍)

- [ ] 文章、图片无真实姓名、地名、机构、时间线细节;
- [ ] 图片已去除 EXIF(`sips -s format jpeg in.jpg --out out.jpg` 可洗掉元数据);
- [ ] git 提交邮箱用 GitHub 的 `用户名@users.noreply.github.com`,且该 GitHub 账号未绑定个人邮箱;
- [ ] 不在任何实名平台提到本站,反之亦然。

## 目录结构

```
src/content/articles/zh/*.md   中文文章
src/content/articles/en/*.md   英文文章(与中文同文件名 = 自动配对)
src/pages/                     路由(繁中在根,/en/ 下是英文版)
src/views/ + src/components/   页面与组件
src/lib/ui.ts                  站点名、Patreon 链接、四个 P 的定义、双语字符串
```

## 常用命令

```bash
npm install    # 安装依赖
npm run dev    # 本地预览
npm run build  # 构建到 dist/
```
