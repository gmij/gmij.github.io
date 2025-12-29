#!/usr/bin/env python3
"""
Generate language-specific JSON files from CONTENT.md
This script parses the structured markdown file and creates en.json and zh.json
"""

import re
import json
from pathlib import Path

def parse_content_md(content: str) -> tuple:
    """Parse CONTENT.md and extract English and Chinese content"""
    
    en_data = {
        "meta": {},
        "header": {"stats": []},
        "about": {"items": []},
        "projects": {"leadProjects": [], "contributorProjects": []},
        "skills": {"categories": []},
        "footer": {"links": []},
        "ui": {}
    }
    
    zh_data = {
        "meta": {},
        "header": {"stats": []},
        "about": {"items": []},
        "projects": {"leadProjects": [], "contributorProjects": []},
        "skills": {"categories": []},
        "footer": {"links": []},
        "ui": {}
    }
    
    # Parse Meta Information
    meta_match = re.search(r'## 🌐 Meta Information.*?### English\n(.*?)### 中文\n(.*?)---', content, re.DOTALL)
    if meta_match:
        en_meta = meta_match.group(1)
        zh_meta = meta_match.group(2)
        
        en_data["meta"]["title"] = re.search(r'\*\*Title\*\*: (.+)', en_meta).group(1)
        en_data["meta"]["description"] = re.search(r'\*\*Description\*\*: (.+)', en_meta).group(1)
        en_data["meta"]["keywords"] = re.search(r'\*\*Keywords\*\*: (.+)', en_meta).group(1)
        
        zh_data["meta"]["title"] = re.search(r'\*\*标题\*\*: (.+)', zh_meta).group(1)
        zh_data["meta"]["description"] = re.search(r'\*\*描述\*\*: (.+)', zh_meta).group(1)
        zh_data["meta"]["keywords"] = re.search(r'\*\*关键词\*\*: (.+)', zh_meta).group(1)
    
    # Parse Header
    header_match = re.search(r'## 👤 Header.*?### English\n(.*?)### 中文\n(.*?)### Stats', content, re.DOTALL)
    if header_match:
        en_header = header_match.group(1)
        zh_header = header_match.group(2)
        
        en_data["header"]["name"] = re.search(r'\*\*Name\*\*: (.+)', en_header).group(1)
        en_data["header"]["tagline"] = re.search(r'\*\*Tagline\*\*: (.+)', en_header).group(1)
        en_data["header"]["subtitle"] = re.search(r'\*\*Subtitle\*\*: (.+)', en_header).group(1)
        
        zh_data["header"]["name"] = re.search(r'\*\*姓名\*\*: (.+)', zh_header).group(1)
        zh_data["header"]["tagline"] = re.search(r'\*\*标语\*\*: (.+)', zh_header).group(1)
        zh_data["header"]["subtitle"] = re.search(r'\*\*副标题\*\*: (.+)', zh_header).group(1)
    
    # Parse Stats
    stats_match = re.search(r'### Stats.*?\n(.*?)---', content, re.DOTALL)
    if stats_match:
        stats = stats_match.group(1).strip().split('\n')
        for stat in stats:
            if '|' in stat:
                parts = stat.split('|')
                number = re.search(r'\*\*(.+?)\*\*', parts[0]).group(1)
                en_label = parts[1].split('/')[0].strip()
                zh_label = parts[1].split('/')[1].strip()
                
                en_data["header"]["stats"].append({"number": number, "label": en_label})
                zh_data["header"]["stats"].append({"number": number, "label": zh_label})
    
    # Parse About section
    about_match = re.search(r'## 💡 About Me.*?---', content, re.DOTALL)
    if about_match:
        about_section = about_match.group(0)
        items = re.findall(r'### Item \d+:.*?\n- \*\*Icon\*\*: (.+?)\n.*?\*\*English Title\*\*: (.+?)\n.*?\*\*English Description\*\*: (.+?)\n.*?\*\*中文标题\*\*: (.+?)\n.*?\*\*中文描述\*\*: (.+?)(?=\n###|\n---)', about_section, re.DOTALL)
        
        en_data["about"]["title"] = "About Me"
        zh_data["about"]["title"] = "关于我"
        
        for icon, en_title, en_desc, zh_title, zh_desc in items:
            en_data["about"]["items"].append({
                "icon": icon.strip(),
                "title": en_title.strip(),
                "description": en_desc.strip()
            })
            zh_data["about"]["items"].append({
                "icon": icon.strip(),
                "title": zh_title.strip(),
                "description": zh_desc.strip()
            })
    
    # Parse Projects
    projects_match = re.search(r'## 🚀 Projects.*?## 🛠️ Skills', content, re.DOTALL)
    if projects_match:
        projects_section = projects_match.group(0)
        
        en_data["projects"]["title"] = "Open Source Projects"
        en_data["projects"]["leadTitle"] = "Lead Projects"
        en_data["projects"]["contributorTitle"] = "Contributor Projects"
        zh_data["projects"]["title"] = "开源项目"
        zh_data["projects"]["leadTitle"] = "主导项目"
        zh_data["projects"]["contributorTitle"] = "贡献项目"
        
        # Parse lead projects
        lead_section = re.search(r'### Lead Projects.*?### Contributor Projects', projects_section, re.DOTALL)
        if lead_section:
            lead_items = re.findall(r'#### \d+\. (.+?)\n(.*?)(?=\n####|\n###)', lead_section.group(0), re.DOTALL)
            for name, details in lead_items:
                en_name = name.strip()
                zh_name = name.strip()
                
                # Check if there's a Chinese name
                name_match = re.search(r'\*\*Name EN\*\*: (.+?)\n.*?\*\*名称 ZH\*\*: (.+?)[\n]', details)
                if name_match:
                    en_name = name_match.group(1).strip()
                    zh_name = name_match.group(2).strip()
                
                en_badge = re.search(r'\*\*Badge EN\*\*: (.+)', details).group(1).strip()
                zh_badge = re.search(r'\*\*Badge ZH\*\*: (.+)', details).group(1).strip()
                en_desc = re.search(r'\*\*Description EN\*\*: (.+)', details).group(1).strip()
                zh_desc = re.search(r'\*\*描述 ZH\*\*: (.+)', details).group(1).strip()
                
                github_match = re.search(r'\*\*GitHub\*\*: (.+)', details)
                website_match = re.search(r'\*\*Website\*\*: (.+)', details)
                website_label_en = re.search(r'\*\*Website Label EN\*\*: (.+)', details)
                website_label_zh = re.search(r'\*\*网站标签 ZH\*\*: (.+)', details)
                
                en_project = {
                    "name": en_name,
                    "badge": en_badge,
                    "description": en_desc
                }
                zh_project = {
                    "name": zh_name,
                    "badge": zh_badge,
                    "description": zh_desc
                }
                
                if github_match:
                    en_project["github"] = github_match.group(1).strip()
                    zh_project["github"] = github_match.group(1).strip()
                
                if website_match:
                    en_project["website"] = website_match.group(1).strip()
                    zh_project["website"] = website_match.group(1).strip()
                
                if website_label_en:
                    en_project["websiteLabel"] = website_label_en.group(1).strip()
                if website_label_zh:
                    zh_project["websiteLabel"] = website_label_zh.group(1).strip()
                
                en_data["projects"]["leadProjects"].append(en_project)
                zh_data["projects"]["leadProjects"].append(zh_project)
        
        # Parse contributor projects
        contrib_section = re.search(r'### Contributor Projects.*?(?=---|\n##)', projects_section, re.DOTALL)
        if contrib_section:
            contrib_items = re.findall(r'#### \d+\. (.+?)\n(.*?)(?=\n####|\n---|\n##)', contrib_section.group(0), re.DOTALL)
            for name, details in contrib_items:
                en_badge = re.search(r'\*\*Badge EN\*\*: (.+)', details).group(1).strip()
                zh_badge = re.search(r'\*\*Badge ZH\*\*: (.+)', details).group(1).strip()
                en_desc = re.search(r'\*\*Description EN\*\*: (.+)', details).group(1).strip()
                zh_desc = re.search(r'\*\*描述 ZH\*\*: (.+)', details).group(1).strip()
                github = re.search(r'\*\*GitHub\*\*: (.+)', details).group(1).strip()
                
                en_data["projects"]["contributorProjects"].append({
                    "name": name.strip(),
                    "badge": en_badge,
                    "description": en_desc,
                    "github": github
                })
                zh_data["projects"]["contributorProjects"].append({
                    "name": name.strip(),
                    "badge": zh_badge,
                    "description": zh_desc,
                    "github": github
                })
    
    # Parse Skills
    skills_match = re.search(r'## 🛠️ Skills.*?## 📝 Footer', content, re.DOTALL)
    if skills_match:
        skills_section = skills_match.group(0)
        
        en_data["skills"]["title"] = "Skills & Expertise"
        zh_data["skills"]["title"] = "技能专长"
        
        categories = re.findall(r'### Category \d+:.*?\n- \*\*EN\*\*: (.+?) \| \*\*ZH\*\*: (.+?)\n- \*\*Items EN\*\*:\n(.*?)- \*\*项目 ZH\*\*:\n(.*?)(?=\n###|\n---|\n##)', skills_section, re.DOTALL)
        
        for en_name, zh_name, en_items, zh_items in categories:
            en_items_list = [item.strip().lstrip('- ').strip() for item in en_items.strip().split('\n') if item.strip()]
            zh_items_list = [item.strip().lstrip('- ').strip() for item in zh_items.strip().split('\n') if item.strip()]
            
            en_data["skills"]["categories"].append({
                "name": en_name.strip(),
                "items": en_items_list
            })
            zh_data["skills"]["categories"].append({
                "name": zh_name.strip(),
                "items": zh_items_list
            })
    
    # Parse Footer
    footer_match = re.search(r'## 📝 Footer.*?## 🎨 UI Text', content, re.DOTALL)
    if footer_match:
        footer_section = footer_match.group(0)
        
        en_data["footer"]["copyright"] = "© 2024 GMIJ. All rights reserved."
        zh_data["footer"]["copyright"] = "© 2024 GMIJ. All rights reserved."
        
        links = re.findall(r'\d+\. \*\*(.+?)\*\* - (.+)', footer_section)
        for label, url in links:
            if '/' in label:
                en_label = label.split('/')[0].strip()
                zh_label = label.split('/')[1].strip()
                en_data["footer"]["links"].append({"label": en_label, "url": url.strip()})
                zh_data["footer"]["links"].append({"label": zh_label, "url": url.strip()})
            else:
                en_data["footer"]["links"].append({"label": label.strip(), "url": url.strip()})
                zh_data["footer"]["links"].append({"label": label.strip(), "url": url.strip()})
    
    # Parse UI Text
    ui_match = re.search(r'## 🎨 UI Text.*', content, re.DOTALL)
    if ui_match:
        ui_section = ui_match.group(0)
        
        en_data["ui"]["langButton"] = "中文"
        zh_data["ui"]["langButton"] = "EN"
        en_data["ui"]["githubLabel"] = "GitHub"
        zh_data["ui"]["githubLabel"] = "GitHub"
        
        loading_en = re.search(r'\*\*Loading EN\*\*: (.+)', ui_section)
        loading_zh = re.search(r'\*\*加载 ZH\*\*: (.+)', ui_section)
        if loading_en:
            en_data["ui"]["loading"] = loading_en.group(1).strip()
        if loading_zh:
            zh_data["ui"]["loading"] = loading_zh.group(1).strip()
    
    return en_data, zh_data

def main():
    """Main function to generate JSON files"""
    
    # Read CONTENT.md
    content_path = Path("CONTENT.md")
    if not content_path.exists():
        print("Error: CONTENT.md not found")
        return 1
    
    content = content_path.read_text(encoding='utf-8')
    
    # Parse content
    en_data, zh_data = parse_content_md(content)
    
    # Write JSON files
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    en_path = data_dir / "en.json"
    zh_path = data_dir / "zh.json"
    
    with open(en_path, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, indent=2, ensure_ascii=False)
    
    with open(zh_path, 'w', encoding='utf-8') as f:
        json.dump(zh_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {en_path}")
    print(f"✓ Generated {zh_path}")
    
    return 0

if __name__ == "__main__":
    exit(main())
