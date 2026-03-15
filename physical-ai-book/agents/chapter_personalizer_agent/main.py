# Chapter Personalizer Agent
# Adapts chapter content to user's skill level and hardware availability

import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from typing import Dict, Any

load_dotenv()


class ChapterPersonalizerAgent:
    """AI agent for personalizing chapter content based on user profile."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "../../../docs"))
    
    def personalize_chapter(
        self,
        content: str,
        user_profile: Dict[str, Any]
    ) -> str:
        """
        Adapt chapter content to user's profile.
        
        Args:
            content: Original chapter content
            user_profile: User's profile with experience levels, hardware, etc.
            
        Returns:
            Personalized content
        """
        system_prompt = """You are an AI teaching assistant personalizing educational content.

Adapt the content based on the user's profile:

1. **Experience Level Adjustments:**
   - Beginner: Add more explanations, examples, and analogies. Simplify language.
   - Intermediate: Standard technical depth with practical examples.
   - Advanced: Focus on advanced concepts, optimizations, and edge cases.

2. **Hardware Adaptations:**
   - No hardware: Emphasize simulation alternatives
   - Simulation only: Focus on Gazebo/Isaac Sim workflows
   - Jetson: Include edge deployment considerations
   - Workstation: Include full-scale training examples
   - Physical robot: Include hardware-specific tips

3. **Learning Path:**
   - Highlight relevant sections
   - Add prerequisites if needed
   - Suggest additional resources

Keep the original structure but adapt explanations and examples.
"""
        
        user_prompt = f"""Personalize this chapter for the following user profile:

User Profile:
- Programming Experience: {user_profile.get('programming_experience', 'beginner')}
- AI/ML Experience: {user_profile.get('ai_experience', 'beginner')}
- Robotics Experience: {user_profile.get('robotics_experience', 'beginner')}
- Hardware Availability: {user_profile.get('hardware_availability', 'none')}
- GPU Capability: {user_profile.get('gpu_capability', 'integrated')}
- Preferred Language: {user_profile.get('preferred_language', 'en')}

Original Chapter Content:
{content[:15000]}  # Limit to avoid token limits
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    
    def add_personalization_notes(
        self,
        content: str,
        user_profile: Dict[str, Any]
    ) -> str:
        """
        Add personalization notes/annotations to content without modifying it.
        
        This is useful for overlaying personalized hints on standard content.
        """
        notes = []
        
        # Generate notes based on profile
        if user_profile.get('programming_experience') == 'beginner':
            notes.append(
                "> 💡 **Beginner Tip**: Take your time with the code examples. "
                "Type them out manually instead of copying to build muscle memory."
            )
        
        if user_profile.get('robotics_experience') == 'beginner':
            notes.append(
                "> 📚 **Background**: If you're new to robotics, review Module 1 first "
                "to understand ROS 2 basics before proceeding."
            )
        
        if user_profile.get('hardware_availability') == 'simulation':
            notes.append(
                "> 🖥️ **Simulation Focus**: All labs in this chapter include "
                "simulation alternatives. You can complete everything in Gazebo."
            )
        
        if user_profile.get('gpu_capability') == 'integrated':
            notes.append(
                "> ⚠️ **GPU Note**: Some examples may run slowly on integrated graphics. "
                "Consider using cloud GPUs (Colab, Kaggle) for training tasks."
            )
        
        if not notes:
            notes.append(
                "> ✅ **Ready to Go**: Based on your profile, you're well-prepared "
                "for this chapter. Jump right in!"
            )
        
        notes_section = "\n\n".join(notes)
        
        # Insert notes after frontmatter
        import re
        frontmatter_match = re.match(r'(---\n.*?\n---\n)', content, re.DOTALL)
        
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            body = content[len(frontmatter):]
            personalized_content = frontmatter + "\n" + notes_section + "\n\n" + body
        else:
            personalized_content = notes_section + "\n\n" + content
        
        return personalized_content
    
    def get_recommended_path(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get recommended learning path based on user profile.
        
        Returns:
            Dict with recommended chapters, estimated time, and prerequisites
        """
        experience_level = max(
            user_profile.get('programming_experience', 'beginner'),
            user_profile.get('ai_experience', 'beginner'),
            user_profile.get('robotics_experience', 'beginner'),
            key=lambda x: {'beginner': 0, 'intermediate': 1, 'advanced': 2}.get(x, 0)
        )
        
        paths = {
            'beginner': {
                'estimated_weeks': 12,
                'hours_per_week': 8,
                'focus_areas': ['ROS 2 Basics', 'Python Programming', 'Simulation First'],
                'skip_chapters': [],
                'additional_resources': [
                    'Python for Beginners',
                    'Linux Command Line Basics',
                    'Robotics Mathematics Primer'
                ]
            },
            'intermediate': {
                'estimated_weeks': 8,
                'hours_per_week': 6,
                'focus_areas': ['AI Integration', 'Advanced Control', 'Real Projects'],
                'skip_chapters': ['Basic Python Review'],
                'additional_resources': [
                    'Deep Learning for Robotics',
                    'ROS 2 Best Practices'
                ]
            },
            'advanced': {
                'estimated_weeks': 4,
                'hours_per_week': 5,
                'focus_areas': ['Production Deployment', 'Optimization', 'Research Topics'],
                'skip_chapters': ['Introduction to ROS 2', 'Python Basics'],
                'additional_resources': [
                    'ROS 2 Source Code',
                    'Research Papers on Physical AI'
                ]
            }
        }
        
        return paths.get(experience_level, paths['beginner'])
    
    def personalize_for_chapter(
        self,
        chapter_path: str,
        user_profile: Dict[str, Any],
        add_notes_only: bool = True
    ) -> str:
        """Personalize a chapter file."""
        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if add_notes_only:
            personalized = self.add_personalization_notes(content, user_profile)
        else:
            personalized = self.personalize_chapter(content, user_profile)
        
        return personalized


def main():
    """Example usage."""
    agent = ChapterPersonalizerAgent()
    
    # Example user profile
    user_profile = {
        'programming_experience': 'beginner',
        'ai_experience': 'beginner',
        'robotics_experience': 'beginner',
        'hardware_availability': 'simulation',
        'gpu_capability': 'integrated',
        'preferred_language': 'en'
    }
    
    # Get recommended path
    path = agent.get_recommended_path(user_profile)
    print("Recommended Learning Path:")
    print(f"  Duration: {path['estimated_weeks']} weeks")
    print(f"  Focus: {', '.join(path['focus_areas'])}")
    print(f"  Additional Resources: {', '.join(path['additional_resources'])}")
    
    # Example personalization
    sample_content = """---
title: Introduction to ROS 2
---

# Chapter 1: Introduction to ROS 2

ROS 2 is a middleware framework for robotics...
"""
    
    personalized = agent.add_personalization_notes(sample_content, user_profile)
    print("\n\nPersonalized Content:")
    print(personalized)


if __name__ == "__main__":
    main()
