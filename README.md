# HKP4 — 香港的四個面向 · Four Lenses on Hong Kong

匿名的繁中 + 英文双语香港观察刊物。Astro 静态站,部署在 GitHub Pages,零成本。

四个面向:**繁榮 Prosperity · 推演 Projection · 前景 Prospect · 潛能 Potential**

## 日常发布流程

1. 用中文写文章:复制 `src/content/articles/zh/why-hkp4.md` 为新的 `.md` 文件(文件名即网址 slug,用小写英文加连字符);
2. 把中文版翻译成英文,存为**同名文件**放在 `src/content/articles/en/`(同名 = 自动互相关联、自动出现语言切换链接);
3. `npm run dev` 本地预览 http://localhost:4321;
4. `git add . && git commit && git push` → GitHub Actions 自动构建上线(约 1 分钟)。

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

## 上线步骤(一次性)

1. 用专用 ProtonMail 注册 GitHub 账号,用户名 **hkp4**(若被占用,换 `hkp4-journal` 之类,并改 `astro.config.mjs` 里的 `site`);
2. 新建仓库,**仓库名必须等于 `用户名.github.io`**(如 `hkp4.github.io`),这样 Pages 根路径部署,无需改 base;
3. 把本目录推上去(见下),GitHub → Settings → Pages → Build and deployment → **Source: GitHub Actions**(工作流文件已备好 `.github/workflows/deploy.yml`);
4. 打开 `https://hkp4.github.io` 验收。

```bash
git init -b main   # 本目录已初始化过则跳过
git remote add origin git@github.com:hkp4/hkp4.github.io.git
git push -u origin main
```

## 上线前必须替换的占位符

| 位置 | 占位符 | 换成 |
|---|---|---|
| `src/lib/ui.ts` | `patreon` 链接 | 你的 Patreon 页面地址 |
| `src/lib/ui.ts` | `email` | 你的 ProtonMail 地址 |
| `src/pages/donate.astro` + `en/donate.astro` | 三个加密货币地址 | 你的钱包地址(先小额自测) |

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
