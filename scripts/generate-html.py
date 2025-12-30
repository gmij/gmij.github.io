#!/usr/bin/env python3
"""
Generate static HTML files with pre-rendered content for better SEO.
This script reads the JSON data files and generates complete HTML files
with all content already in place, so search engines can index the content
without needing to execute JavaScript.
"""

import json
import os
from pathlib import Path
from html import escape

def load_json(filepath):
    """Load JSON data from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def render_stats(stats):
    """Render stats section"""
    html = []
    for stat in stats:
        html.append(f'''
            <div class="stat-item">
                <span class="stat-number">{escape(stat["number"])}</span>
                <span class="stat-label">{escape(stat["label"])}</span>
            </div>''')
    return ''.join(html)

def render_about_items(items):
    """Render about section items"""
    html = []
    for item in items:
        html.append(f'''
            <div class="about-item">
                <h3><span class="about-icon">{item["icon"]}</span>{escape(item["title"])}</h3>
                <p>{item["description"]}</p>
            </div>''')
    return ''.join(html)

def render_project_card(project, github_label):
    """Render a single project card"""
    github_icon_svg = '''<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="vertical-align: middle; margin-right: 4px;">
        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
    </svg>'''
    
    links = []
    if project.get('github'):
        links.append(f'''
            <a href="{escape(project['github'])}" class="btn" target="_blank" rel="noopener noreferrer">
                {github_icon_svg}
                {escape(github_label)}
            </a>''')
    
    if project.get('website'):
        website_label = project.get('websiteLabel', 'Visit Site')
        links.append(f'''
            <a href="{escape(project['website'])}" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
                {escape(website_label)}
            </a>''')
    
    return f'''
        <div class="project-card">
            <h3>{escape(project["name"])}</h3>
            <span class="project-badge">{escape(project["badge"])}</span>
            <p>{project["description"]}</p>
            <div class="project-links">
                {''.join(links)}
            </div>
        </div>'''

def render_projects(projects, github_label):
    """Render projects grid"""
    return ''.join([render_project_card(p, github_label) for p in projects])

def render_skills(categories):
    """Render skills section"""
    html = []
    for category in categories:
        items_html = ''.join([f'<li>{escape(item)}</li>' for item in category['items']])
        html.append(f'''
            <div class="skill-category">
                <h3>{escape(category["name"])}</h3>
                <ul class="skill-list">
                    {items_html}
                </ul>
            </div>''')
    return ''.join(html)

def render_footer_links(links, github_label):
    """Render footer links"""
    github_icon_svg = '''<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="vertical-align: middle; margin-right: 4px;">
        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
    </svg>'''
    
    html = []
    for i, link in enumerate(links):
        prefix = ' · ' if i > 0 else ''
        if link['label'] == github_label:
            html.append(f'''{prefix}<a href="{escape(link['url'])}" target="_blank" rel="noopener noreferrer">
                {github_icon_svg}
                {escape(link['label'])}
            </a>''')
        else:
            html.append(f'''{prefix}<a href="{escape(link['url'])}" target="_blank" rel="noopener noreferrer">{escape(link['label'])}</a>''')
    
    return ''.join(html)

def get_html_template(lang_code):
    """Get the base HTML template with styles"""
    return '''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    <!-- Primary Meta Tags -->
    <title>{title}</title>
    <meta name="title" content="{title}">
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="GMIJ">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="GMIJ Personal Page">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{canonical_url}">
    
    <!-- Alternate language versions -->
    <link rel="alternate" hreflang="en" href="https://gmij.win/index-en.html">
    <link rel="alternate" hreflang="zh-CN" href="https://gmij.win/">
    <link rel="alternate" hreflang="x-default" href="https://gmij.win/">
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "GMIJ",
      "url": "https://gmij.win",
      "jobTitle": "Full Stack Engineer",
      "description": "15 years .NET full stack development experience, 5 years technical management experience",
      "knowsAbout": [".NET Development", "DevOps", "Continuous Integration", "Team Management", "Full Stack Development", "AI Programming", "AI Voice Interaction"],
      "sameAs": [
        "https://github.com/gmij",
        "https://github.com/dotnetcore/SmartSql",
        "https://github.com/ant-design-blazor/ant-design-blazor"
      ]
    }}
    </script>
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-primary: #0f1419;
            --bg-secondary: #1a1f29;
            --bg-tertiary: #242b38;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --accent: #3b9eff;
            --accent-hover: #58a6ff;
            --border: #30363d;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
        }}
        
        body {{
            font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.7;
            color: var(--text-primary);
            background-color: var(--bg-primary);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 24px;
        }}
        
        /* Language Switcher */
        .lang-switcher {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }}
        
        .lang-btn {{
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s ease;
            font-family: inherit;
            text-decoration: none;
            display: inline-block;
        }}
        
        .lang-btn:hover {{
            background: var(--bg-tertiary);
            border-color: var(--accent);
        }}
        
        /* Header */
        header {{
            padding: 120px 0 80px;
            text-align: center;
            border-bottom: 1px solid var(--border);
            background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        }}
        
        header h1 {{
            font-size: 64px;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: -1px;
            color: var(--text-primary);
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        @supports not (background-clip: text) {{
            header h1 {{
                color: var(--text-primary);
                background: none;
            }}
        }}
        
        header .tagline {{
            font-size: 24px;
            color: var(--text-primary);
            font-weight: 500;
            margin-bottom: 12px;
        }}
        
        header .subtitle {{
            font-size: 16px;
            color: var(--text-secondary);
            font-weight: 400;
            margin-bottom: 40px;
        }}
        
        /* Stats Bar */
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 40px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 36px;
            font-weight: 700;
            color: var(--accent);
            display: block;
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Section */
        section {{
            padding: 64px 0;
        }}
        
        section:not(:last-child) {{
            border-bottom: 1px solid var(--border);
        }}
        
        h2 {{
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 32px;
            color: var(--text-primary);
        }}
        
        /* About Section */
        .about-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
        }}
        
        .about-item {{
            padding: 32px 24px;
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .about-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--accent);
            transform: scaleY(0);
            transition: transform 0.3s ease;
        }}
        
        .about-item:hover {{
            border-color: var(--accent);
            box-shadow: var(--shadow-md);
            transform: translateY(-4px);
        }}
        
        .about-item:hover::before {{
            transform: scaleY(1);
        }}
        
        .about-item h3 {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .about-icon {{
            font-size: 28px;
            line-height: 1;
        }}
        
        .about-item p {{
            font-size: 15px;
            color: var(--text-secondary);
            line-height: 1.8;
        }}
        
        /* Projects Section */
        .section-subtitle {{
            font-size: 20px;
            font-weight: 600;
            margin: 40px 0 24px;
            color: var(--text-primary);
        }}
        
        .section-subtitle:first-of-type {{
            margin-top: 0;
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 24px;
        }}
        
        .project-card {{
            padding: 24px;
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 8px;
            transition: all 0.2s ease;
        }}
        
        .project-card:hover {{
            border-color: var(--accent);
            box-shadow: var(--shadow-md);
        }}
        
        .project-card h3 {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-primary);
        }}
        
        .project-badge {{
            display: inline-block;
            padding: 4px 10px;
            font-size: 12px;
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            border-radius: 4px;
            margin-bottom: 12px;
        }}
        
        .project-card p {{
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.7;
            margin-bottom: 16px;
        }}
        
        .project-links {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            display: inline-block;
            padding: 8px 16px;
            font-size: 14px;
            color: var(--accent);
            text-decoration: none;
            border: 1px solid var(--accent);
            border-radius: 6px;
            transition: all 0.2s ease;
            font-weight: 500;
        }}
        
        .btn:hover {{
            background: var(--accent);
            color: white;
        }}
        
        .btn-primary {{
            background: var(--accent);
            color: white;
        }}
        
        .btn-primary:hover {{
            background: var(--accent-hover);
            border-color: var(--accent-hover);
        }}
        
        /* Skills Section */
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 32px;
        }}
        
        .skill-category h3 {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-primary);
        }}
        
        .skill-list {{
            list-style: none;
        }}
        
        .skill-list li {{
            font-size: 15px;
            color: var(--text-secondary);
            padding: 6px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .skill-list li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: var(--accent);
            font-weight: bold;
        }}
        
        /* Footer */
        footer {{
            padding: 48px 0;
            text-align: center;
            border-top: 1px solid var(--border);
            background: var(--bg-secondary);
        }}
        
        footer p {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }}
        
        footer a {{
            color: var(--accent);
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        
        footer a:hover {{
            color: var(--accent-hover);
        }}
        
        /* Responsive */
        @media (max-width: 1024px) and (min-width: 769px) {{
            .about-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            header {{
                padding: 80px 0 60px;
            }}
            
            header h1 {{
                font-size: 42px;
            }}
            
            header .tagline {{
                font-size: 18px;
            }}
            
            header .subtitle {{
                font-size: 14px;
            }}
            
            .stats-bar {{
                gap: 40px;
            }}
            
            .stat-number {{
                font-size: 28px;
            }}
            
            .stat-label {{
                font-size: 12px;
            }}
            
            h2 {{
                font-size: 24px;
            }}
            
            .about-grid,
            .projects-grid,
            .skills-grid {{
                grid-template-columns: 1fr;
            }}
            
            section {{
                padding: 48px 0;
            }}
            
            .lang-switcher {{
                top: 15px;
                right: 15px;
            }}
        }}
        
        /* Accessibility - Reduced motion */
        @media (prefers-reduced-motion: reduce) {{
            *,
            *::before,
            *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
            
            .about-item::before {{
                transition: none;
            }}
            
            .about-item:hover {{
                transform: none;
            }}
        }}
    </style>
</head>
<body>
    <!-- Language Switcher -->
    <div class="lang-switcher">
        <a href="{lang_switch_url}" class="lang-btn">
            <span>{lang_button_text}</span>
        </a>
    </div>

    <header>
        <div class="container">
            <h1>{header_name}</h1>
            <p class="tagline">{header_tagline}</p>
            <p class="subtitle">{header_subtitle}</p>
            
            <div class="stats-bar">
                {stats_html}
            </div>
        </div>
    </header>

    <section>
        <div class="container">
            <h2>{about_title}</h2>
            <div class="about-grid">
                {about_html}
            </div>
        </div>
    </section>

    <section>
        <div class="container">
            <h2>{projects_title}</h2>
            
            <div class="section-subtitle">{projects_lead_title}</div>
            <div class="projects-grid">
                {lead_projects_html}
            </div>
            
            <div class="section-subtitle">{projects_contributor_title}</div>
            <div class="projects-grid">
                {contributor_projects_html}
            </div>
        </div>
    </section>

    <section>
        <div class="container">
            <h2>{skills_title}</h2>
            <div class="skills-grid">
                {skills_html}
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>{footer_copyright}</p>
            <p>
                {footer_links_html}
            </p>
        </div>
    </footer>
</body>
</html>'''

def generate_html_file(data, lang_code, output_path):
    """Generate a complete HTML file from JSON data"""
    
    # Determine URLs based on language
    if lang_code == 'en':
        canonical_url = 'https://gmij.win/index-en.html'
        lang_switch_url = '/'
        lang_button_text = data['ui']['langButton']  # Should be Chinese text
    else:  # zh
        canonical_url = 'https://gmij.win/'
        lang_switch_url = '/index-en.html'
        lang_button_text = data['ui']['langButton']  # Should be English text
    
    # Get the HTML template
    template = get_html_template(lang_code)
    
    # Render all sections
    stats_html = render_stats(data['header']['stats'])
    about_html = render_about_items(data['about']['items'])
    lead_projects_html = render_projects(data['projects']['leadProjects'], data['ui']['githubLabel'])
    contributor_projects_html = render_projects(data['projects']['contributorProjects'], data['ui']['githubLabel'])
    skills_html = render_skills(data['skills']['categories'])
    footer_links_html = render_footer_links(data['footer']['links'], data['ui']['githubLabel'])
    
    # Fill in the template
    html = template.format(
        lang='zh-CN' if lang_code == 'zh' else 'en',
        title=escape(data['meta']['title']),
        description=escape(data['meta']['description']),
        keywords=escape(data['meta']['keywords']),
        canonical_url=canonical_url,
        lang_switch_url=lang_switch_url,
        lang_button_text=escape(lang_button_text),
        header_name=escape(data['header']['name']),
        header_tagline=escape(data['header']['tagline']),
        header_subtitle=escape(data['header']['subtitle']),
        stats_html=stats_html,
        about_title=escape(data['about']['title']),
        about_html=about_html,
        projects_title=escape(data['projects']['title']),
        projects_lead_title=escape(data['projects']['leadTitle']),
        projects_contributor_title=escape(data['projects']['contributorTitle']),
        lead_projects_html=lead_projects_html,
        contributor_projects_html=contributor_projects_html,
        skills_title=escape(data['skills']['title']),
        skills_html=skills_html,
        footer_copyright=escape(data['footer']['copyright']),
        footer_links_html=footer_links_html
    )
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated {output_path}")

def main():
    """Main function to generate all HTML files"""
    
    # Load JSON data
    data_dir = Path('data')
    en_data = load_json(data_dir / 'en.json')
    zh_data = load_json(data_dir / 'zh.json')
    
    # Generate HTML files
    generate_html_file(zh_data, 'zh', Path('index.html'))
    generate_html_file(en_data, 'en', Path('index-en.html'))
    
    print("\n✓ All HTML files generated successfully!")
    print("  - index.html (Chinese)")
    print("  - index-en.html (English)")
    print("\nSEO improvements:")
    print("  ✓ Pre-rendered content in HTML (no JS required)")
    print("  ✓ Proper meta tags (title, description, keywords)")
    print("  ✓ Open Graph and Twitter Card meta tags")
    print("  ✓ Canonical URLs")
    print("  ✓ Alternate language links (hreflang)")
    print("  ✓ JSON-LD structured data")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
