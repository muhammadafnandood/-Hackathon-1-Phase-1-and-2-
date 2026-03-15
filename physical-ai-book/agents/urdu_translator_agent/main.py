# Urdu Translator Agent
# Translates textbook content to Urdu while keeping technical terms in English

import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import re

load_dotenv()


class UrduTranslatorAgent:
    """AI agent for translating textbook content to Urdu."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "../../../docs"))
    
    def translate_to_urdu(
        self,
        content: str,
        preserve_technical_terms: bool = True
    ) -> str:
        """
        Translate content to Urdu.
        
        Args:
            content: English content to translate
            preserve_technical_terms: Keep technical terms in English
            
        Returns:
            Urdu translated content
        """
        system_prompt = """You are a professional translator translating technical educational content from English to Urdu.

Translation Rules:
1. Keep all technical terms in English (ROS 2, Python, Gazebo, LiDAR, IMU, etc.)
2. Translate explanations and descriptions to Urdu
3. Maintain readability for Pakistani students
4. Keep code blocks unchanged
5. Keep headings in English with Urdu translation in parentheses
6. Use clear, simple Urdu
7. Maintain the Markdown structure

Example:
English: "ROS 2 is a middleware for robotics communication"
Urdu: "ROS 2 روبوٹکس مواصلات کے لیے ایک middleware ہے"
"""
        
        user_prompt = f"""Translate the following textbook content to Urdu:

{content[:15000]}  # Limit to avoid token limits
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    
    def translate_chapter(self, chapter_path: str) -> str:
        """Translate a chapter file."""
        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        frontmatter_match = re.match(r'(---\n.*?\n---\n)', content, re.DOTALL)
        frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
        body = content[len(frontmatter):] if frontmatter else content
        
        # Translate body
        translated_body = self.translate_to_urdu(body)
        
        # Combine
        translated_content = frontmatter + translated_body
        
        return translated_content
    
    def save_translation(
        self,
        content: str,
        original_path: str,
        language: str = "ur"
    ):
        """Save translated content."""
        original = Path(original_path)
        translated_path = original.parent / f"{original.stem}.{language}{original.suffix}"
        
        with open(translated_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Saved translation to {translated_path}")
        return translated_path
    
    def translate_directory(self, module_dir: str, language: str = "ur"):
        """Translate all markdown files in a directory."""
        module_path = Path(module_dir)
        
        for md_file in module_path.rglob("*.md"):
            print(f"Translating: {md_file}")
            
            try:
                translated = self.translate_chapter(str(md_file))
                self.save_translation(translated, str(md_file), language)
            except Exception as e:
                print(f"❌ Error translating {md_file}: {e}")
    
    def translate_with_glossary(self, content: str, glossary: dict) -> str:
        """
        Translate using a custom glossary for consistent terminology.
        
        Args:
            content: Content to translate
            glossary: Dict of English -> Urdu translations for specific terms
        """
        # First, replace technical terms with placeholders
        placeholders = {}
        for i, (en, ur) in enumerate(glossary.items()):
            placeholder = f"__TERM_{i}__"
            placeholders[placeholder] = f"{en} ({ur})"
            content = content.replace(en, placeholder)
        
        # Translate
        translated = self.translate_to_urdu(content)
        
        # Restore terms with glossary
        for placeholder, replacement in placeholders.items():
            translated = translated.replace(placeholder, replacement)
        
        return translated


def main():
    """Example usage."""
    agent = UrduTranslatorAgent()
    
    # Example translation
    sample_text = """
# Introduction to ROS 2

ROS 2 is a middleware framework for robotics. It provides:

- Hardware abstraction
- Inter-process communication  
- Package management

## Installation

Install ROS 2 Humble on Ubuntu 22.04:

```bash
sudo apt install ros-humble-desktop
```
"""
    
    glossary = {
        "middleware": "درمیانی سافٹ ویئر",
        "robotics": "ربوٹکس",
        "communication": "مواصلات",
        "hardware": "ہارڈ ویئر",
        "package": "پیکج",
        "installation": "انسٹالیشن"
    }
    
    translated = agent.translate_with_glossary(sample_text, glossary)
    print(translated)


if __name__ == "__main__":
    main()
