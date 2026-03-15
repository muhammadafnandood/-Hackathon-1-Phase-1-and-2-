#!/usr/bin/env python3
"""
Learning Personalization Agent

Adapts textbook content to match individual learner's technical background.
Analyzes user profile and rewrites explanations, code comments, and examples
at the appropriate complexity level.
"""

import re
from typing import Dict, List, Optional, Literal, Any
from dataclasses import dataclass, field
from enum import Enum


class ExperienceLevel(Enum):
    """User experience level enumeration."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class UserProfile:
    """
    Represents a learner's technical background.
    
    Attributes:
        programming_experience: Coding proficiency level
        robotics_knowledge: Familiarity with robotics concepts
        ai_experience: Understanding of AI/ML concepts
        hardware_experience: Experience with embedded systems/hardware
        learning_style: Preferred learning approach (optional)
        goals: Specific learning objectives (optional)
    """
    programming_experience: ExperienceLevel
    robotics_knowledge: ExperienceLevel
    ai_experience: ExperienceLevel
    hardware_experience: ExperienceLevel
    learning_style: str = "balanced"  # "visual", "hands-on", "theoretical", "balanced"
    goals: Optional[str] = None
    
    def get_overall_level(self) -> ExperienceLevel:
        """Determine overall technical level from profile."""
        levels = [
            self.programming_experience,
            self.robotics_knowledge,
            self.ai_experience,
            self.hardware_experience,
        ]
        
        # Count levels
        counts = {level: 0 for level in ExperienceLevel}
        for level in levels:
            counts[level] += 1
        
        # Return most common level, preferring higher if tied
        if counts[ExperienceLevel.ADVANCED] >= 2:
            return ExperienceLevel.ADVANCED
        elif counts[ExperienceLevel.INTERMEDIATE] >= 2:
            return ExperienceLevel.INTERMEDIATE
        else:
            return ExperienceLevel.BEGINNER
    
    def get_domain_level(self, domain: str) -> ExperienceLevel:
        """Get experience level for a specific domain."""
        domain_map = {
            "programming": self.programming_experience,
            "robotics": self.robotics_knowledge,
            "ai": self.ai_experience,
            "hardware": self.hardware_experience,
        }
        return domain_map.get(domain.lower(), self.get_overall_level())
    
    def to_dict(self) -> Dict[str, str]:
        """Convert profile to dictionary."""
        return {
            "programming_experience": self.programming_experience.value,
            "robotics_knowledge": self.robotics_knowledge.value,
            "ai_experience": self.ai_experience.value,
            "hardware_experience": self.hardware_experience.value,
            "learning_style": self.learning_style,
            "goals": self.goals or "General learning",
        }


@dataclass
class PersonalizedChapter:
    """Result of content personalization."""
    original_text: str
    personalized_text: str
    user_profile: UserProfile
    adaptations_made: List[str] = field(default_factory=list)
    reading_level: str = ""
    word_count_original: int = 0
    word_count_personalized: int = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get personalization statistics."""
        return {
            "user_profile": self.user_profile.to_dict(),
            "reading_level": self.reading_level,
            "word_count_original": self.word_count_original,
            "word_count_personalized": self.word_count_personalized,
            "adaptations_count": len(self.adaptations_made),
            "adaptations": self.adaptations_made,
        }


class ContentPersonalizer:
    """
    Personalizes technical content based on user profiles.
    
    Adapts explanations, code examples, and technical depth to match
    the learner's background in programming, robotics, AI, and hardware.
    """
    
    def __init__(self, user_profile: UserProfile):
        """
        Initialize the personalizer with a user profile.
        
        Args:
            user_profile: The learner's technical background
        """
        self.profile = user_profile
        self.overall_level = user_profile.get_overall_level()
        
        # Define adaptation templates for each level
        self.explanation_templates = self._load_explanation_templates()
        self.analogy_library = self._load_analogy_library()
        self.code_comment_styles = self._load_comment_styles()
    
    def _load_explanation_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load explanation templates for different levels and domains."""
        return {
            "beginner": {
                "programming": [
                    "Think of this like a recipe - you follow steps in order to get a result.",
                    "Just like you'd organize files into folders, this organizes code into modules.",
                    "Imagine giving instructions to a very literal friend who does exactly what you say.",
                ],
                "robotics": [
                    "A robot is like a person with senses (sensors), a brain (processor), and hands/legs (actuators).",
                    "Think of ROS 2 as a universal language that lets different robot parts talk to each other.",
                    "Just as your nervous system sends signals from brain to muscles, this sends commands to motors.",
                ],
                "ai": [
                    "AI is like teaching a computer to recognize patterns, similar to how you learn from experience.",
                    "Think of machine learning like training a pet - you show examples and reward correct behavior.",
                    "An AI model is like a recipe that takes ingredients (data) and produces a dish (predictions).",
                ],
                "hardware": [
                    "Hardware is the physical parts you can touch, like the screen you're reading this on.",
                    "Think of embedded systems as tiny computers built into everyday devices.",
                    "Sensors are like the robot's eyes, ears, and skin - they help it perceive the world.",
                ],
            },
            "intermediate": {
                "programming": [
                    "This follows the single responsibility principle - each function does one thing well.",
                    "Similar to design patterns in software, this provides a reusable solution.",
                    "The API abstracts away implementation details, exposing only what's needed.",
                ],
                "robotics": [
                    "The middleware handles message serialization, discovery, and QoS management.",
                    "This architecture separates perception, planning, and control layers.",
                    "Sensor fusion combines multiple data sources for more robust state estimation.",
                ],
                "ai": [
                    "The model architecture uses attention mechanisms for contextual understanding.",
                    "Training involves gradient descent optimization with backpropagation.",
                    "Feature extraction transforms raw input into a representation suitable for learning.",
                ],
                "hardware": [
                    "The microcontroller interfaces with sensors via I2C, SPI, or UART protocols.",
                    "Real-time constraints require careful interrupt handling and priority management.",
                    "Power management balances performance with thermal and battery constraints.",
                ],
            },
            "advanced": {
                "programming": [
                    "This implementation achieves O(1) amortized complexity through careful memory management.",
                    "The lock-free data structure uses atomic operations for thread safety.",
                    "Metaprogramming techniques enable compile-time optimization and type safety.",
                ],
                "robotics": [
                    "The SLAM algorithm employs factor graph optimization with loop closure detection.",
                    "Model predictive control solves the constrained optimization problem in real-time.",
                    "The manipulation pipeline integrates perception, grasp planning, and trajectory optimization.",
                ],
                "ai": [
                    "The transformer architecture employs multi-head self-attention with positional encodings.",
                    "Contrastive learning maximizes mutual information between representations.",
                    "The policy gradient method optimizes expected return with variance reduction techniques.",
                ],
                "hardware": [
                    "The FPGA implementation achieves deterministic latency through pipelined architecture.",
                    "Heterogeneous computing leverages CPU-GPU-NPU coordination for optimal throughput.",
                    "The sensor interface uses time-triggered Ethernet for synchronized data acquisition.",
                ],
            },
        }
    
    def _load_analogy_library(self) -> Dict[str, List[Dict[str, str]]]:
        """Load analogies for explaining complex concepts."""
        return {
            "publisher_subscriber": [
                {
                    "level": "beginner",
                    "analogy": "Like a YouTube channel - creators post videos (publish), viewers subscribe to channels they like. They don't need to know each other."
                },
                {
                    "level": "intermediate", 
                    "analogy": "Like an event-driven architecture - components emit events and others listen for events they care about, enabling loose coupling."
                },
                {
                    "level": "advanced",
                    "analogy": "Implements the observer pattern with data-centric communication - publishers own the data, subscribers express interest, DDS handles routing."
                },
            ],
            "vector_embedding": [
                {
                    "level": "beginner",
                    "analogy": "Like converting a song into coordinates on a map - similar songs end up close together, different songs far apart."
                },
                {
                    "level": "intermediate",
                    "analogy": "Projects high-dimensional data into a continuous vector space where semantic similarity corresponds to geometric proximity."
                },
                {
                    "level": "advanced",
                    "analogy": "Learns a manifold embedding that preserves semantic relationships through contrastive loss or language modeling objectives."
                },
            ],
            "neural_network": [
                {
                    "level": "beginner",
                    "analogy": "Like a team of workers passing notes - each worker does a simple calculation and passes the result to the next person."
                },
                {
                    "level": "intermediate",
                    "analogy": "Composes multiple layers of linear transformations with non-linear activations to learn hierarchical representations."
                },
                {
                    "level": "advanced",
                    "analogy": "Implements universal function approximation through composition of differentiable operators optimized via gradient-based methods."
                },
            ],
        }
    
    def _load_comment_styles(self) -> Dict[str, Dict[str, str]]:
        """Load code commenting styles for different levels."""
        return {
            "beginner": {
                "style": "verbose",
                "prefix": "# ",
                "explain_what": True,
                "explain_why": True,
                "explain_how": True,
                "example": "# Create a variable to store the temperature\n# We need this to check if the motor is too hot\ntemperature = 25.0  # Starting temperature in Celsius",
            },
            "intermediate": {
                "style": "balanced",
                "prefix": "# ",
                "explain_what": True,
                "explain_why": True,
                "explain_how": False,
                "example": "# Initialize temperature sensor\n# Used for thermal monitoring\ntemperature = 25.0",
            },
            "advanced": {
                "style": "minimal",
                "prefix": "# ",
                "explain_what": False,
                "explain_why": False,
                "explain_how": False,
                "example": "# Configuration\ntemperature = 25.0",
            },
        }
    
    def _detect_domain(self, text: str) -> List[str]:
        """Detect which technical domains are present in the text."""
        domains = []
        text_lower = text.lower()
        
        # Programming indicators
        prog_keywords = ["function", "variable", "code", "algorithm", "api", "class", "method", "loop"]
        if any(kw in text_lower for kw in prog_keywords):
            domains.append("programming")
        
        # Robotics indicators
        robot_keywords = ["robot", "ros", "sensor", "actuator", "motor", "joint", "trajectory", "kinematics"]
        if any(kw in text_lower for kw in robot_keywords):
            domains.append("robotics")
        
        # AI indicators
        ai_keywords = ["model", "training", "neural", "machine learning", "ai", "inference", "embedding", "vector"]
        if any(kw in text_lower for kw in ai_keywords):
            domains.append("ai")
        
        # Hardware indicators
        hw_keywords = ["hardware", "embedded", "microcontroller", "fpga", "circuit", "gpio", "i2c", "spi"]
        if any(kw in text_lower for kw in hw_keywords):
            domains.append("hardware")
        
        return domains if domains else ["general"]
    
    def _simplify_explanation(self, text: str, domain: str) -> str:
        """Simplify an explanation for beginners."""
        # Replace jargon with simpler terms
        replacements = {
            "middleware": "software that connects different programs",
            "abstraction": "simplified view that hides complexity",
            "implementation": "the actual code that makes it work",
            "architecture": "the overall design and structure",
            "paradigm": "a pattern or model",
            "encapsulation": "bundling data and functions together",
            "polymorphism": "ability to take multiple forms",
            "instantiate": "create",
            "invoke": "call",
            "utilize": "use",
            "facilitate": "help",
            "mechanism": "method",
            "protocol": "set of rules",
            "interface": "connection point",
            "payload": "data being sent",
            "latency": "delay",
            "throughput": "amount processed per second",
            "robust": "strong and reliable",
            "scalable": "can grow to handle more",
            "deterministic": "always produces the same result",
            "stochastic": "involves randomness",
            "concurrent": "happening at the same time",
            "asynchronous": "not requiring simultaneous presence",
            "synchronous": "happening at the same time",
        }
        
        result = text
        for complex_term, simple_explanation in replacements.items():
            # Only replace if the term appears and isn't already explained
            pattern = rf'\b{complex_term}\b'
            if re.search(pattern, result, re.IGNORECASE):
                # Add explanation in parentheses
                replacement = f"{complex_term} ({simple_explanation})"
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def _add_context(self, text: str, domain: str, level: ExperienceLevel) -> str:
        """Add contextual information based on domain and level."""
        if level == ExperienceLevel.BEGINNER:
            context_additions = {
                "programming": "\n\n💡 **Why this matters:** Good code organization makes programs easier to understand and fix.",
                "robotics": "\n\n💡 **Why this matters:** Robots need to sense, think, and act - all in the right order and timing.",
                "ai": "\n\n💡 **Why this matters:** AI helps robots understand complex patterns that are hard to program by hand.",
                "hardware": "\n\n💡 **Why this matters:** Hardware choices affect speed, power use, and what the robot can do.",
            }
            return text + context_additions.get(domain, "")
        
        elif level == ExperienceLevel.INTERMEDIATE:
            context_additions = {
                "programming": "\n\n📊 **Best Practice:** Consider trade-offs between readability, performance, and maintainability.",
                "robotics": "\n\n📊 **Industry Standard:** This pattern is widely used in production robotics systems.",
                "ai": "\n\n📊 **Key Insight:** The choice of model architecture depends on your data and constraints.",
                "hardware": "\n\n📊 **Design Consideration:** Balance real-time requirements with power and cost constraints.",
            }
            return text + context_additions.get(domain, "")
        
        else:  # Advanced
            context_additions = {
                "programming": "\n\n🔬 **Advanced Topic:** For performance-critical applications, consider lock-free alternatives or custom memory allocators.",
                "robotics": "\n\n🔬 **Research Direction:** Recent work explores learning-based approaches that combine perception and control end-to-end.",
                "ai": "\n\n🔬 **State of the Art:** See 'Attention Is All You Need' (Vaswani et al., 2017) for the foundational transformer architecture.",
                "hardware": "\n\n🔬 **Cutting Edge:** Heterogeneous architectures with specialized accelerators are becoming standard for edge AI.",
            }
            return text + context_additions.get(domain, "")
    
    def _adapt_code_comments(self, code: str, level: ExperienceLevel) -> str:
        """Adapt code comments based on user's level."""
        style = self.code_comment_styles[level.value]
        
        if level == ExperienceLevel.BEGINNER:
            # Add more explanatory comments
            lines = code.split('\n')
            adapted_lines = []
            
            for line in lines:
                adapted_lines.append(line)
                # Add explanation after key statements
                if '=' in line and not line.strip().startswith('#'):
                    # This is an assignment - explain what it does
                    if 'import' not in line:
                        adapted_lines.append('    # ^ This stores the value for later use')
            
            return '\n'.join(adapted_lines)
        
        elif level == ExperienceLevel.INTERMEDIATE:
            # Keep standard comments
            return code
        
        else:  # Advanced
            # Remove verbose comments, keep only essential ones
            lines = code.split('\n')
            adapted_lines = []
            
            for line in lines:
                if line.strip().startswith('#'):
                    # Keep only section headers and important notes
                    if any(marker in line for marker in ['===', 'IMPORTANT', 'NOTE', 'WARNING']):
                        adapted_lines.append(line)
                else:
                    adapted_lines.append(line)
            
            return '\n'.join(adapted_lines)
    
    def _insert_analogy(self, concept: str, text: str) -> str:
        """Insert an appropriate analogy for a concept."""
        concept_key = concept.lower().replace(' ', '_')
        
        if concept_key in self.analogy_library:
            analogies = self.analogy_library[concept_key]
            level = self.overall_level.value
            
            # Find analogy for user's level
            for analogy_data in analogies:
                if analogy_data['level'] == level:
                    analogy_text = analogy_data['analogy']
                    insertion_point = text.find('\n\n')  # Insert after first paragraph
                    if insertion_point == -1:
                        insertion_point = len(text)
                    
                    adapted = f"\n\n💭 **Analogy:** {analogy_text}\n"
                    return text[:insertion_point] + adapted + text[insertion_point:]
        
        return text
    
    def personalize(self, chapter_text: str, target_section: Optional[str] = None) -> PersonalizedChapter:
        """
        Rewrite chapter content based on user's technical background.
        
        Args:
            chapter_text: Original markdown content
            target_section: Optional specific section to personalize
        
        Returns:
            PersonalizedChapter with adapted content
        """
        # Detect domains in the text
        domains = self._detect_domain(chapter_text)
        
        # Start with original text
        personalized = chapter_text
        
        # Track adaptations
        adaptations = []
        
        # Apply adaptations based on level
        if self.overall_level == ExperienceLevel.BEGINNER:
            # Simplify jargon
            for domain in domains:
                original_len = len(personalized)
                personalized = self._simplify_explanation(personalized, domain)
                if len(personalized) < original_len:
                    adaptations.append(f"Simplified {domain} terminology")
            
            # Add analogies for key concepts
            for concept in ["publisher_subscriber", "vector_embedding", "neural_network"]:
                if concept.replace('_', ' ') in personalized.lower():
                    personalized = self._insert_analogy(concept, personalized)
                    adaptations.append(f"Added analogy for {concept.replace('_', ' ')}")
            
            # Add motivational context
            for domain in domains:
                personalized = self._add_context(personalized, domain, self.overall_level)
                adaptations.append(f"Added context for {domain}")
        
        elif self.overall_level == ExperienceLevel.INTERMEDIATE:
            # Add best practices and deeper explanations
            for domain in domains:
                personalized = self._add_context(personalized, domain, self.overall_level)
                adaptations.append(f"Added intermediate {domain} context")
        
        else:  # Advanced
            # Add research insights and advanced topics
            for domain in domains:
                personalized = self._add_context(personalized, domain, self.overall_level)
                adaptations.append(f"Added advanced {domain} insights")
        
        # Adapt any code blocks
        code_pattern = r'```(\w+)?\n(.*?)```'
        
        def adapt_code_block(match):
            lang = match.group(1) or ''
            code = match.group(2)
            adapted_code = self._adapt_code_comments(code, self.overall_level)
            return f'```{lang}\n{adapted_code}\n```'
        
        personalized = re.sub(code_pattern, adapt_code_block, personalized, flags=re.DOTALL)
        if code_pattern in personalized:
            adaptations.append("Adapted code comments for level")
        
        # Create result
        result = PersonalizedChapter(
            original_text=chapter_text,
            personalized_text=personalized,
            user_profile=self.profile,
            adaptations_made=adaptations,
            reading_level=self.overall_level.value,
            word_count_original=len(chapter_text.split()),
            word_count_personalized=len(personalized.split()),
        )
        
        return result
    
    def personalize_section(
        self,
        chapter_text: str,
        section_title: str
    ) -> PersonalizedChapter:
        """
        Personalize a specific section of a chapter.
        
        Args:
            chapter_text: Full chapter content
            section_title: Title of section to personalize
        
        Returns:
            PersonalizedChapter with only that section adapted
        """
        # Find the section
        section_pattern = rf'(## {re.escape(section_title)}\n.*?) (?=## |\Z)'
        match = re.search(section_pattern, chapter_text, re.DOTALL)
        
        if not match:
            raise ValueError(f"Section '{section_title}' not found")
        
        section_text = match.group(1)
        personalized_section = self.personalize(section_text)
        
        # Replace section in original
        personalized_chapter = chapter_text.replace(section_text, personalized_section.personalized_text)
        
        return PersonalizedChapter(
            original_text=chapter_text,
            personalized_text=personalized_chapter,
            user_profile=self.profile,
            adaptations_made=[f"Personalized section: {section_title}"] + personalized_section.adaptations_made,
            reading_level=self.overall_level.value,
            word_count_original=len(chapter_text.split()),
            word_count_personalized=len(personalized_chapter.split()),
        )


def personalize_content(
    chapter_text: str,
    user_profile: UserProfile,
    target_section: Optional[str] = None
) -> PersonalizedChapter:
    """
    Convenience function to personalize content.
    
    Args:
        chapter_text: Original markdown content
        user_profile: User's experience levels
        target_section: Optional specific section to personalize
    
    Returns:
        PersonalizedChapter with adapted content
    """
    personalizer = ContentPersonalizer(user_profile)
    
    if target_section:
        return personalizer.personalize_section(chapter_text, target_section)
    else:
        return personalizer.personalize(chapter_text)


# Example usage
if __name__ == "__main__":
    # Example user profile
    beginner_profile = UserProfile(
        programming_experience=ExperienceLevel.BEGINNER,
        robotics_knowledge=ExperienceLevel.BEGINNER,
        ai_experience=ExperienceLevel.BEGINNER,
        hardware_experience=ExperienceLevel.BEGINNER,
    )
    
    intermediate_profile = UserProfile(
        programming_experience=ExperienceLevel.INTERMEDIATE,
        robotics_knowledge=ExperienceLevel.BEGINNER,
        ai_experience=ExperienceLevel.INTERMEDIATE,
        hardware_experience=ExperienceLevel.BEGINNER,
    )
    
    advanced_profile = UserProfile(
        programming_experience=ExperienceLevel.ADVANCED,
        robotics_knowledge=ExperienceLevel.INTERMEDIATE,
        ai_experience=ExperienceLevel.ADVANCED,
        hardware_experience=ExperienceLevel.INTERMEDIATE,
    )
    
    # Sample chapter text
    sample_text = """
## Introduction to Publisher-Subscriber Pattern

The publisher-subscriber pattern enables decoupled communication between nodes.
Publishers send messages to topics without knowing who will receive them.
Subscribers express interest in topics and receive relevant messages.

```python
class Publisher:
    def __init__(self, topic):
        self.topic = topic
        self.subscribers = []
    
    def publish(self, message):
        for sub in self.subscribers:
            sub.receive(message)
```

This architecture is widely used in robotics middleware like ROS 2.
"""
    
    # Personalize for different users
    print("=" * 60)
    print("BEGINNER VERSION")
    print("=" * 60)
    
    beginner_result = personalize_content(sample_text, beginner_profile)
    print(beginner_result.personalized_text)
    print("\n📊 Adaptations made:")
    for adaptation in beginner_result.adaptations_made:
        print(f"  - {adaptation}")
    
    print("\n" + "=" * 60)
    print("ADVANCED VERSION")
    print("=" * 60)
    
    advanced_result = personalize_content(sample_text, advanced_profile)
    print(advanced_result.personalized_text)
    print("\n📊 Adaptations made:")
    for adaptation in advanced_result.adaptations_made:
        print(f"  - {adaptation}")
