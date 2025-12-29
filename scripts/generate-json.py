#!/usr/bin/env python3
"""
Generate language-specific JSON files from README.md using AI
This script uses GitHub Models API to understand README.md and generate structured JSON files
"""

import json
import os
import sys
from pathlib import Path

def generate_json_with_ai():
    """Use GitHub Models API to generate JSON files from README.md"""
    
    # GitHub token is automatically available in Actions
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return 1
    
    # Read README.md
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("Error: README.md not found")
        return 1
    
    readme_content = readme_path.read_text(encoding='utf-8')
    
    # Read schema
    schema_path = Path("data/schema.json")
    if not schema_path.exists():
        print("Error: data/schema.json not found")
        return 1
    
    schema = schema_path.read_text(encoding='utf-8')
    
    # Prepare the prompt for AI
    prompt = f"""You are a helpful assistant that converts personal introduction content into structured JSON format.

I have a README.md file with personal information in Chinese, and I need you to generate two JSON files following a specific schema:
1. en.json - English version
2. zh.json - Chinese version (based on the README content)

README.md content:
```
{readme_content}
```

JSON Schema to follow:
```json
{schema}
```

Based on the README content, please generate BOTH en.json and zh.json files. 

For the Chinese version (zh.json), extract and structure the information from README.md.
For the English version (en.json), translate the content appropriately.

Additional context:
- Name: GMIJ
- The person has 15 years of .NET development experience (2002-2017)
- 5 years of management experience (2017-2023)
- Expertise in DevOps, TeamCity, team building (0-to-1)
- Managed R&D team (20+) and Operations team (70+)
- Increased annual operations contract from 1M to nearly 20M CNY
- Active in open source projects: SmartSql, Ant Design Blazor
- Lead projects: DynamicWallpaper, Audio3A_CSharp, Green Software Download Site, Children Image, ZerotierFix
- All recent projects are AI-powered/AI-written

Please provide the output as two separate JSON objects labeled clearly as "EN_JSON:" and "ZH_JSON:".
Ensure all required fields from the schema are included.
Use proper English translations for the English version.
"""

    try:
        import requests
        
        # Use GitHub Models API
        api_url = "https://models.inference.ai.azure.com/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {github_token}"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that converts personal information into structured JSON format. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "gpt-4o",
            "temperature": 0.3,
            "max_tokens": 4000
        }
        
        print("Calling GitHub Models API to generate JSON files...")
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Extract the response
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Parse the response to extract JSON objects
        en_json_str = None
        zh_json_str = None
        
        # Try to find EN_JSON and ZH_JSON markers
        if "EN_JSON:" in content:
            en_start = content.find("EN_JSON:") + len("EN_JSON:")
            en_end = content.find("ZH_JSON:") if "ZH_JSON:" in content else len(content)
            en_json_str = content[en_start:en_end].strip()
            
            # Remove markdown code blocks if present
            if en_json_str.startswith("```json"):
                en_json_str = en_json_str[7:]
            if en_json_str.startswith("```"):
                en_json_str = en_json_str[3:]
            if en_json_str.endswith("```"):
                en_json_str = en_json_str[:-3]
            en_json_str = en_json_str.strip()
        
        if "ZH_JSON:" in content:
            zh_start = content.find("ZH_JSON:") + len("ZH_JSON:")
            zh_json_str = content[zh_start:].strip()
            
            # Remove markdown code blocks if present
            if zh_json_str.startswith("```json"):
                zh_json_str = zh_json_str[7:]
            if zh_json_str.startswith("```"):
                zh_json_str = zh_json_str[3:]
            if zh_json_str.endswith("```"):
                zh_json_str = zh_json_str[:-3]
            zh_json_str = zh_json_str.strip()
        
        # If markers not found, try to parse the entire response as JSON array
        if not en_json_str or not zh_json_str:
            # Try to find JSON objects in the content
            import re
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, content, re.DOTALL)
            if len(matches) >= 2:
                en_json_str = matches[0]
                zh_json_str = matches[1]
        
        if not en_json_str or not zh_json_str:
            print("Error: Could not parse AI response")
            print("Response:", content[:500])
            return 1
        
        # Parse JSON
        try:
            en_data = json.loads(en_json_str)
            zh_data = json.loads(zh_json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print("EN JSON:", en_json_str[:200])
            print("ZH JSON:", zh_json_str[:200])
            return 1
        
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
        
    except ImportError as e:
        print(f"Error: Missing required package: {e}")
        print("Installing requests...")
        os.system("pip install requests")
        print("Please run the script again.")
        return 1
    except requests.exceptions.RequestException as e:
        print(f"Error calling GitHub Models API: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

def main():
    """Main function"""
    return generate_json_with_ai()

if __name__ == "__main__":
    sys.exit(main())
