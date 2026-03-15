# Book Writer Agent
# Generates textbook content using AI

import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from datetime import datetime

load_dotenv()


class BookWriterAgent:
    """AI agent for generating textbook content."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "../../../docs"))
    
    def generate_chapter(
        self,
        module_name: str,
        chapter_title: str,
        topics: list,
        learning_objectives: list
    ) -> str:
        """
        Generate a complete chapter.
        
        Args:
            module_name: Name of the module
            chapter_title: Title of the chapter
            topics: List of topics to cover
            learning_objectives: List of learning objectives
            
        Returns:
            Generated chapter content in Markdown
        """
        system_prompt = """You are an expert technical author writing a textbook on Physical AI & Humanoid Robotics.

Write educational content that is:
- Clear and structured
- Beginner to advanced friendly
- Includes code examples
- Includes diagrams (ASCII art)
- Includes hands-on labs
- Optimized for RAG (short sections, descriptive headings)

Follow this structure:
1. Learning Objectives
2. Concept Explanation
3. Architecture Overview (with diagram)
4. Code Examples
5. Hands-on Lab
6. Summary
7. Exercises
"""
        
        user_prompt = f"""Write a complete chapter for the Physical AI & Humanoid Robotics textbook.

Module: {module_name}
Chapter Title: {chapter_title}

Topics to cover:
{chr(10).join(f'- {topic}' for topic in topics)}

Learning Objectives:
{chr(10).join(f'- {obj}' for obj in learning_objectives)}

Requirements:
- Use Markdown format
- Include Python code examples where relevant
- Include ASCII architecture diagrams
- Include a hands-on lab with step-by-step instructions
- Keep sections short (for RAG optimization)
- Use descriptive headings
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    
    def generate_module_overview(self, module_name: str, chapters: list) -> str:
        """Generate a module overview page."""
        system_prompt = """You are creating a module overview page for a textbook.
        
The overview should include:
- Module description
- What students will learn
- Chapter list with descriptions
- Prerequisites
- Time commitment
- Resources
"""
        
        user_prompt = f"""Create a module overview for: {module_name}

Chapters:
{chr(10).join(f'- {chapter}' for chapter in chapters)}
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def save_chapter(self, content: str, module: str, chapter: str):
        """Save chapter to file."""
        output_path = self.output_dir / module / f"{chapter}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Saved chapter to {output_path}")
    
    def generate_from_outline(self, outline: dict):
        """Generate content from a complete outline."""
        module_name = outline.get("module", "module1")
        
        # Generate module overview
        chapters = outline.get("chapters", [])
        overview = self.generate_module_overview(
            module_name,
            [c.get("title", "") for c in chapters]
        )
        self.save_chapter(overview, module_name, "index")
        
        # Generate each chapter
        for chapter in chapters:
            print(f"Generating chapter: {chapter.get('title')}")
            
            content = self.generate_chapter(
                module_name=module_name,
                chapter_title=chapter.get("title"),
                topics=chapter.get("topics", []),
                learning_objectives=chapter.get("objectives", [])
            )
            
            slug = chapter.get("slug", chapter.get("title", "").lower().replace(" ", "-"))
            self.save_chapter(content, module_name, slug)


def main():
    """Example usage."""
    agent = BookWriterAgent()
    
    # Example outline for Module 2
    outline = {
        "module": "module2",
        "chapters": [
            {
                "title": "Introduction to Gazebo Simulation",
                "slug": "chapter1-gazebo-introduction",
                "topics": [
                    "What is Gazebo",
                    "Gazebo vs Isaac Sim",
                    "Installing Gazebo",
                    "Your first simulation"
                ],
                "objectives": [
                    "Understand Gazebo architecture",
                    "Install and configure Gazebo",
                    "Create a basic simulation world"
                ]
            }
        ]
    }
    
    agent.generate_from_outline(outline)


if __name__ == "__main__":
    main()
