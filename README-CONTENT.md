# Personal Website Content Management

This repository uses an automated workflow to manage website content. You only need to edit `CONTENT.md`, and the rest is handled automatically!

## 📝 How It Works

```
CONTENT.md (edit this) 
    ↓
GitHub Action (automatic)
    ↓
data/en.json + data/zh.json (auto-generated)
    ↓
index.html (displays content)
```

## ✏️ Updating Content

**You only need to edit `CONTENT.md`!**

1. Edit `CONTENT.md` with your changes
2. Commit and push to the `main` branch
3. GitHub Actions automatically generates `data/en.json` and `data/zh.json`
4. Your website is updated automatically!

### Example: Adding a New Project

Open `CONTENT.md` and add a new project section:

```markdown
#### 6. My New Project
- **Badge EN**: New
- **Badge ZH**: 新项目
- **Description EN**: This is my awesome new project.
- **描述 ZH**: 这是我很棒的新项目。
- **GitHub**: https://github.com/username/project
- **Website**: https://example.com
- **Website Label EN**: Visit Site
- **网站标签 ZH**: 访问站点
```

That's it! Commit and push, and the action will update the JSON files.

## 🏗️ Architecture

### Files

- **`CONTENT.md`** - The single source of truth for all website content (edit this!)
- **`data/schema.json`** - JSON schema defining the structure
- **`data/en.json`** - Auto-generated English content
- **`data/zh.json`** - Auto-generated Chinese content
- **`scripts/generate-json.py`** - Python script that converts CONTENT.md to JSON
- **`.github/workflows/generate-json.yml`** - GitHub Action that runs the script
- **`index.html`** - Website template that loads and displays JSON content

### Workflow

1. **Content Source**: All content is maintained in `CONTENT.md` using a structured markdown format
2. **Automation**: GitHub Action triggers on every push to `main` when `CONTENT.md` changes
3. **Generation**: Python script parses `CONTENT.md` and generates JSON files
4. **Validation**: JSON files are validated against the schema
5. **Deployment**: Generated JSON files are committed and pushed automatically
6. **Display**: Website loads JSON based on user's language preference

## 🛠️ Local Development

### Generate JSON Locally

```bash
python3 scripts/generate-json.py
```

### Validate JSON

```bash
python3 -m json.tool data/en.json > /dev/null && echo "✓ en.json is valid"
python3 -m json.tool data/zh.json > /dev/null && echo "✓ zh.json is valid"
```

### Preview Website

```bash
python3 -m http.server 8000
# Open http://localhost:8000/index.html
```

## 📋 Content Structure

The `CONTENT.md` file is organized into clear sections:

- **Meta Information** - SEO metadata (title, description, keywords)
- **Header** - Page header with tagline and stats
- **About Me** - Four highlight cards about experience
- **Projects** - Lead projects and contributor projects
- **Skills** - Skill categories and items
- **Footer** - Copyright and links
- **UI Text** - Interface labels and messages

Each section has both English and Chinese versions clearly marked.

## 🔄 Migration from Old System

The old system required editing HTML files with embedded content:

```html
<!-- Old way - editing HTML -->
<h3 lang="zh">AI编程专家</h3>
<h3 lang="en">AI Programming Expert</h3>
```

The new system uses a single markdown file:

```markdown
<!-- New way - editing CONTENT.md -->
### Item 1: AI Programming Expert / AI编程专家
- **English Title**: AI Programming Expert
- **中文标题**: AI编程专家
```

## 🎯 Benefits

1. **Simple to Edit** - Markdown is easy to read and write
2. **Single Source** - One file contains all content
3. **Automated** - No manual JSON generation needed
4. **Validated** - JSON schema ensures correctness
5. **Version Controlled** - Clear git diffs for content changes
6. **Scalable** - Easy to add more languages

## 📚 Schema

The JSON structure is defined in `data/schema.json` using JSON Schema draft-07. This ensures:

- Consistent structure across languages
- Validation of generated JSON
- Clear documentation of data format
- Easy integration with tools and editors

## 🚀 CI/CD

The GitHub Action runs automatically:

- **Trigger**: Push to `main` with changes to `CONTENT.md`
- **Manual**: Can also be triggered manually via workflow_dispatch
- **Output**: Commits updated JSON files if changes detected
- **Validation**: Ensures JSON files are valid before committing

## 💡 Tips

- Use `[skip ci]` in commit message to skip the action
- The action only runs when `CONTENT.md` changes
- JSON files are auto-generated - don't edit them directly!
- Keep CONTENT.md formatting consistent for reliable parsing
- Test locally with `python3 scripts/generate-json.py` before pushing

## 🤝 Contributing

When adding new content:

1. Edit `CONTENT.md` following the existing format
2. Test locally with the generation script
3. Commit and push to see it live!

---

**Note**: This setup was created to make content management easier. Now you can focus on writing content in a simple markdown file, and automation handles the rest! ✨
