# 自我介绍
15年研发经验：2002年-2017年，专注.NET开发，全栈工程师，对代码有着一定的精神洁癖，不定期的进行重构。

熟练掌握DevOps相关知识，擅长使用Teamcity进行持续构建。

5年管理经理：2017-2023年，曾任岗位：研发总监（研发团队20人+），运维总监（驻场运维团队70人+）

擅长领域：研发和运维团队从0到1组建，擅长研发效能改进以及运维管理改进（把年运维合同额从100w提升到近2000w）

管理思路: 带领团队不断取得胜利

目前参与贡献的开源项目（github）:
[dotnetcore/smartsql](https://github.com/dotnetcore/SmartSql)、[ant-design-blazor](https://github.com/ant-design-blazor/ant-design-blazor)

目前自己在主导的开源项目（github）：
[DynamicWallpaper](https://github.com/gmij/DynamicWallpaper)  =====>>  [壁纸墙](https://dw.gmij.win)

[Audio3A_CSharp](https://github.com/gmij/Audio3A_CSharp) =====>> 一个完全由AI编写的.NET原生音频3A处理SDK

[绿色软件下载站](https://github.com/gmij/soft)  =====>> [绿色软件下载站](https://gmij.win/soft)一个完全由AI编写的资源下载站

[children_image](https://github.com/gmij/children_image) =====>> [Ai幼画](https://img.gmij.win) 一个完全由AI编写的儿童手抄报生成器

[ZerotierFix](https://github.com/gmij/ZerotierFix) =====>> 一个完全由AI完善的ZeroTier安卓客户端，用于个人VPN

---

## 构建说明 / Build Instructions

本网站使用自动化构建流程来优化SEO（搜索引擎优化）。

### 工作流程

1. **README.md → JSON**: 当 README.md 更新时，GitHub Actions 自动使用 AI 生成 `data/en.json` 和 `data/zh.json`
2. **JSON → HTML**: 生成的 JSON 文件会被转换为带有完整内容的静态 HTML 文件（`index.html` 和 `index-en.html`）

### SEO 优化

- ✅ **预渲染内容**: 所有内容直接包含在 HTML 中，无需 JavaScript 加载
- ✅ **完整的元标签**: 标题、描述、关键词都从 JSON 数据填充
- ✅ **Open Graph 标签**: 优化社交媒体分享
- ✅ **Twitter Card 标签**: 优化 Twitter 分享
- ✅ **规范化 URL**: 正确的 URL 规范化
- ✅ **Hreflang 标签**: 多语言 SEO 支持
- ✅ **JSON-LD 结构化数据**: 搜索引擎富文本摘要

### 手动构建

如果需要手动重新生成 HTML 文件：

```bash
# 生成 HTML 文件
python scripts/generate-html.py
```

---

## Build Instructions

This website uses an automated build process to optimize for SEO (Search Engine Optimization).

### Workflow

1. **README.md → JSON**: When README.md is updated, GitHub Actions automatically uses AI to generate `data/en.json` and `data/zh.json`
2. **JSON → HTML**: The generated JSON files are converted to static HTML files with full content (`index.html` and `index-en.html`)

### SEO Optimizations

- ✅ **Pre-rendered content**: All content is included directly in HTML, no JavaScript loading required
- ✅ **Complete meta tags**: Title, description, keywords populated from JSON data
- ✅ **Open Graph tags**: Optimized for social media sharing
- ✅ **Twitter Card tags**: Optimized for Twitter sharing
- ✅ **Canonical URLs**: Proper URL canonicalization
- ✅ **Hreflang tags**: Multi-language SEO support
- ✅ **JSON-LD structured data**: Rich snippets for search engines

### Manual Build

To manually regenerate the HTML files:

```bash
# Generate HTML files
python scripts/generate-html.py
```
