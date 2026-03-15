#!/usr/bin/env python3
"""
Urdu Translator Agent

Translates technical textbook chapters into Urdu while preserving:
- Technical terminology (ROS 2, AI, ML, etc.)
- Markdown formatting
- Code blocks
- Structure and layout
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TranslationResult:
    """Result of Urdu translation."""
    original_text: str
    translated_text: str
    source_file: str
    output_file: str
    word_count_original: int
    word_count_translated: int
    sections_translated: int


class UrduTechnicalTranslator:
    """
    Translates technical content to Urdu while preserving technical terms.
    """
    
    # Technical terms to keep in English
    TECHNICAL_TERMS = {
        # ROS 2 / Robotics
        'ROS 2', 'ROS', 'node', 'topic', 'publisher', 'subscriber', 'middleware',
        'service', 'action', 'message', 'parameter', 'launch', 'gazebo', 'rviz',
        'tf2', 'urdf', 'sdf', 'robot', 'sensor', 'actuator', 'motor', 'joint',
        'link', 'end effector', 'manipulator', 'mobile robot', 'humanoid',
        
        # AI / ML
        'AI', 'ML', 'DL', 'neural network', 'deep learning', 'machine learning',
        'embedding', 'vector', 'tensor', 'model', 'training', 'inference',
        'dataset', 'epoch', 'batch', 'gradient', 'loss', 'optimizer',
        'transformer', 'attention', 'CNN', 'RNN', 'LSTM', 'GAN', 'VAE',
        'reinforcement learning', 'imitation learning', 'policy', 'reward',
        
        # RAG / Vector DB
        'RAG', 'retrieval', 'generation', 'Qdrant', 'vector database',
        'embedding', 'similarity', 'cosine', 'dot product', 'index',
        'chunk', 'payload', 'collection', 'point', 'filter',
        
        # Programming
        'Python', 'C++', 'JavaScript', 'code', 'function', 'class', 'method',
        'variable', 'import', 'return', 'if', 'else', 'for', 'while',
        'list', 'dict', 'array', 'string', 'integer', 'float', 'boolean',
        'API', 'REST', 'HTTP', 'JSON', 'YAML', 'XML',
        
        # Hardware / Embedded
        'CPU', 'GPU', 'NPU', 'FPGA', 'microcontroller', 'Arduino', 'Raspberry Pi',
        'GPIO', 'I2C', 'SPI', 'UART', 'PWM', 'ADC', 'DAC',
        'camera', 'LiDAR', 'radar', 'IMU', 'accelerometer', 'gyroscope',
        
        # NVIDIA / Simulation
        'NVIDIA', 'Isaac', 'Omniverse', 'Unity', 'Unreal Engine',
        'simulation', 'digital twin', 'synthetic data',
        
        # OpenAI / LLM
        'OpenAI', 'GPT', 'LLM', 'language model', 'chatbot', 'prompt',
        'token', 'completion', 'fine-tuning', 'zero-shot', 'few-shot',
    }
    
    # Common English to Urdu translations
    TRANSLATION_DICT = {
        # General
        'introduction': 'تعارف',
        'chapter': 'باب',
        'section': 'شق',
        'example': 'مثال',
        'exercise': 'مشق',
        'question': 'سوال',
        'answer': 'جواب',
        'summary': 'خلاصہ',
        'conclusion': 'نتیجہ',
        
        # Learning
        'learning objectives': 'سیکھنے کے مقاصد',
        'what you will learn': 'آپ کیا سیکھیں گے',
        'prerequisites': 'پہلے سے ضروری معلومات',
        'key takeaways': 'اہم نکات',
        'what we covered': 'ہم نے کیا احاطہ کیا',
        'what next': 'آگے کیا ہے',
        
        # Technical explanations
        'is a': 'ایک ہے',
        'are': 'ہیں',
        'the': 'وہ',
        'and': 'اور',
        'or': 'یا',
        'but': 'لیکن',
        'with': 'کے ساتھ',
        'for': 'کے لیے',
        'from': 'سے',
        'to': 'کو',
        'in': 'میں',
        'on': 'پر',
        'at': 'پر',
        'by': 'کی طرف سے',
        'this': 'یہ',
        'that': 'وہ',
        'these': 'یہ',
        'those': 'وہ',
        
        # Code related
        'code': 'کوڈ',
        'output': 'آؤٹ پٹ',
        'input': 'ان پٹ',
        'data': 'ڈیٹا',
        'file': 'فائل',
        'directory': 'ڈائریکٹری',
        'folder': 'فولڈر',
        
        # Instructions
        'create': 'بنائیں',
        'run': 'چلائیں',
        'execute': 'چلائیں',
        'install': 'انسٹال کریں',
        'configure': 'کنفیگر کریں',
        'start': 'شروع کریں',
        'stop': 'روکیں',
        'open': 'کھولیں',
        'close': 'بند کریں',
        'save': 'محفوظ کریں',
        'load': 'لوڈ کریں',
        'read': 'پڑھیں',
        'write': 'لکھیں',
        
        # Descriptive
        'helps': 'مدد کرتا ہے',
        'enables': 'قابل بناتا ہے',
        'allows': 'اجازت دیتا ہے',
        'provides': 'فراہم کرتا ہے',
        'uses': 'استعمال کرتا ہے',
        'creates': 'بناتا ہے',
        'sends': 'بھیجتا ہے',
        'receives': 'وصول کرتا ہے',
        'processes': 'پروسیس کرتا ہے',
        'stores': 'ذخیرہ کرتا ہے',
        'returns': 'واپس کرتا ہے',
        'contains': 'شامل ہے',
        'includes': 'شامل ہے',
        'represents': 'نمائندگی کرتا ہے',
        'defines': 'تعریف کرتا ہے',
        'implements': 'لاگو کرتا ہے',
        'configures': 'کنفیگر کرتا ہے',
        'initializes': 'شروع کرتا ہے',
        'calculates': 'حساب کرتا ہے',
        'computes': 'کمپیوٹ کرتا ہے',
        'generates': 'تیار کرتا ہے',
        'produces': 'پیدا کرتا ہے',
        'displays': 'دکھاتا ہے',
        'shows': 'دکھاتا ہے',
        'prints': 'پرنٹ کرتا ہے',
        'logs': 'لاگ کرتا ہے',
        'errors': 'غلطیاں',
        'warnings': 'انتباہات',
        'messages': 'پیغامات',
        'commands': 'کمانڈز',
        'instructions': 'ہدایات',
        'steps': 'مراحل',
        'process': 'عمل',
        'system': 'سسٹم',
        'component': 'جزو',
        'module': 'ماڈیول',
        'part': 'حصہ',
        'parts': 'حصے',
        'different': 'مختلف',
        'various': 'مختلف',
        'multiple': 'متعدد',
        'single': 'واحد',
        'first': 'پہلا',
        'second': 'دوسرا',
        'third': 'تیسرا',
        'next': 'اگلا',
        'previous': 'پچھلا',
        'current': 'موجودہ',
        'new': 'نیا',
        'old': 'پرانا',
        'same': 'ایک ہی',
        'other': 'دوسرا',
        'another': 'ایک اور',
        'each': 'ہر ایک',
        'all': 'سب',
        'some': 'کچھ',
        'many': 'کئی',
        'few': 'چند',
        'more': 'مزید',
        'most': 'سب سے زیادہ',
        'less': 'کم',
        'least': 'سب سے کم',
        'high': 'زیادہ',
        'low': 'کم',
        'large': 'بڑا',
        'small': 'چھوٹا',
        'big': 'بڑا',
        'good': 'اچھا',
        'better': 'بہتر',
        'best': 'بہترین',
        'bad': 'برا',
        'worse': 'بدتر',
        'worst': 'سب سے برا',
        'easy': 'آسان',
        'hard': 'مشکل',
        'simple': 'سادہ',
        'complex': 'پیچیدہ',
        'fast': 'تیز',
        'slow': 'سست',
        'quick': 'تیز',
        'efficient': 'کارکرد',
        'effective': 'موثر',
        'correct': 'درست',
        'incorrect': 'غلط',
        'true': 'سچ',
        'false': 'جھوٹ',
        'yes': 'ہاں',
        'no': 'نہیں',
        'not': 'نہیں',
        'never': 'کبھی نہیں',
        'always': 'ہمیشہ',
        'often': 'اکثر',
        'sometimes': 'کبھی کبھی',
        'usually': 'عام طور پر',
        'now': 'اب',
        'then': 'پھر',
        'when': 'جب',
        'where': 'کہاں',
        'why': 'کیوں',
        'how': 'کیسے',
        'what': 'کیا',
        'which': 'کون سا',
        'who': 'کون',
        'whose': 'کس کا',
        'whom': 'کس کو',
    }
    
    def __init__(self):
        """Initialize the translator."""
        self.preserved_terms_pattern = self._build_preserved_terms_pattern()
    
    def _build_preserved_terms_pattern(self) -> re.Pattern:
        """Build regex pattern for technical terms to preserve."""
        # Sort by length (longest first) to match multi-word terms first
        sorted_terms = sorted(self.TECHNICAL_TERMS, key=len, reverse=True)
        # Escape special regex characters and join with |
        escaped_terms = [re.escape(term) for term in sorted_terms]
        pattern = r'\b(' + '|'.join(escaped_terms) + r')\b'
        return re.compile(pattern, re.IGNORECASE)
    
    def _protect_technical_terms(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Replace technical terms with placeholders to protect them during translation.
        
        Returns:
            Tuple of (protected_text, mapping_dict)
        """
        protected = text
        mapping = {}
        
        # Find all technical terms
        matches = list(self.preserved_terms_pattern.finditer(text))
        
        # Replace from end to start to preserve positions
        for i, match in enumerate(reversed(matches)):
            term = match.group(0)
            placeholder = f"__TECH_TERM_{len(matches) - i - 1}__"
            mapping[placeholder] = term
            protected = protected[:match.start()] + placeholder + protected[match.end():]
        
        return protected, mapping
    
    def _restore_technical_terms(self, text: str, mapping: Dict[str, str]) -> str:
        """Restore technical terms from placeholders."""
        result = text
        for placeholder, original_term in mapping.items():
            result = result.replace(placeholder, original_term)
        return result
    
    def _translate_text(self, text: str) -> str:
        """
        Translate English text to Urdu.
        
        Note: This is a simplified translation. For production, use a proper
        translation API or service.
        """
        # Protect technical terms
        protected, mapping = self._protect_technical_terms(text)
        
        # Simple word-by-word translation (placeholder for real translation)
        # In production, this would call a translation API
        translated = protected
        
        # Apply dictionary translations (case-insensitive)
        for english, urdu in self.TRANSLATION_DICT.items():
            pattern = re.compile(r'\b' + re.escape(english) + r'\b', re.IGNORECASE)
            translated = pattern.sub(urdu, translated)
        
        # Restore technical terms
        translated = self._restore_technical_terms(translated, mapping)
        
        return translated
    
    def _translate_heading(self, line: str, level: int) -> str:
        """Translate a markdown heading."""
        # Remove heading markers
        text = line.lstrip('#').strip()
        # Translate
        translated = self._translate_text(text)
        # Re-add heading markers
        return '#' * level + ' ' + translated
    
    def _translate_list_item(self, line: str) -> str:
        """Translate a markdown list item."""
        # Detect list type
        if line.strip().startswith('-'):
            prefix = '- '
            text = line.strip()[2:]
        elif re.match(r'^\d+\.', line.strip()):
            match = re.match(r'^(\d+\.\s*)', line.strip())
            prefix = match.group(1)
            text = line.strip()[len(prefix):]
        else:
            return line
        
        translated = self._translate_text(text)
        return prefix + translated
    
    def translate_markdown(self, content: str, source_file: str = "") -> str:
        """
        Translate markdown content to Urdu.
        
        Args:
            content: Original markdown content
            source_file: Source file path for reference
        
        Returns:
            Translated markdown content
        """
        lines = content.split('\n')
        translated_lines = []
        in_code_block = False
        in_callout = False
        
        for line in lines:
            # Check for code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                translated_lines.append(line)  # Keep code block markers as-is
                continue
            
            # Skip code blocks
            if in_code_block:
                translated_lines.append(line)
                continue
            
            # Check for callouts
            if line.strip().startswith(':::'):
                in_callout = not in_callout
                # Translate callout type if it's the opening
                if ':::tip' in line:
                    translated_lines.append(line.replace(':::tip', ':::tip'))
                elif ':::note' in line:
                    translated_lines.append(line.replace(':::note', ':::note'))
                elif ':::info' in line:
                    translated_lines.append(line.replace(':::info', ':::info'))
                elif ':::warning' in line:
                    translated_lines.append(line.replace(':::warning', ':::warning'))
                else:
                    translated_lines.append(line)
                continue
            
            # Skip empty lines
            if not line.strip():
                translated_lines.append(line)
                continue
            
            # Translate based on line type
            if line.startswith('######'):
                translated_lines.append(self._translate_heading(line, 6))
            elif line.startswith('#####'):
                translated_lines.append(self._translate_heading(line, 5))
            elif line.startswith('####'):
                translated_lines.append(self._translate_heading(line, 4))
            elif line.startswith('###'):
                translated_lines.append(self._translate_heading(line, 3))
            elif line.startswith('##'):
                translated_lines.append(self._translate_heading(line, 2))
            elif line.startswith('#'):
                translated_lines.append(self._translate_heading(line, 1))
            elif line.strip().startswith('-') or re.match(r'^\s*\d+\.', line):
                translated_lines.append(self._translate_list_item(line))
            elif line.startswith('|'):
                # Table row - translate cell contents
                translated_lines.append(self._translate_table_row(line))
            else:
                # Regular paragraph
                translated_lines.append(self._translate_text(line))
        
        return '\n'.join(translated_lines)
    
    def _translate_table_row(self, line: str) -> str:
        """Translate a markdown table row."""
        cells = line.split('|')
        translated_cells = []
        
        for i, cell in enumerate(cells):
            if i == 0 or i == len(cells) - 1:
                # Empty cells at start/end
                translated_cells.append(cell)
            elif cell.strip() == '---':
                # Separator row
                translated_cells.append(cell)
            else:
                # Content cell
                translated_cells.append(self._translate_text(cell))
        
        return '|'.join(translated_cells)
    
    def translate_file(self, input_path: str, output_path: Optional[str] = None) -> TranslationResult:
        """
        Translate a markdown file to Urdu.
        
        Args:
            input_path: Path to input markdown file
            output_path: Path for output file (optional)
        
        Returns:
            TranslationResult with translation details
        """
        input_file = Path(input_path)
        
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Read input
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Translate
        translated = self.translate_markdown(content, str(input_file))
        
        # Add translation metadata to frontmatter
        translated = self._add_translation_frontmatter(translated, str(input_file))
        
        # Determine output path
        if output_path:
            output_file = Path(output_path)
        else:
            # Create Urdu version in same directory
            output_file = input_file.parent / f"{input_file.stem}-urdu{input_file.suffix}"
        
        # Write output
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        # Calculate stats
        original_words = len(content.split())
        translated_words = len(translated.split())
        sections = len(re.findall(r'^#{1,6}\s', translated, re.MULTILINE))
        
        return TranslationResult(
            original_text=content,
            translated_text=translated,
            source_file=str(input_file),
            output_file=str(output_file),
            word_count_original=original_words,
            word_count_translated=translated_words,
            sections_translated=sections,
        )
    
    def _add_translation_frontmatter(self, content: str, source_file: str) -> str:
        """Add translation metadata frontmatter."""
        from datetime import datetime
        
        frontmatter = f"""---
translated: true
original_language: English
translated_language: Urdu
source_file: {source_file}
translation_date: {datetime.now().strftime('%Y-%m-%d')}
translator: Urdu-Translator-Agent
---

> **نوٹ:** یہ مواد انگریزی سے اردو میں ترجمہ کیا گیا ہے۔ تکنیکی اصطلاحات انگریزی میں رکھی گئی ہیں۔

"""
        
        # Check if content already has frontmatter
        if content.strip().startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # Insert after existing frontmatter
                return parts[0] + parts[1] + '---\n' + frontmatter + parts[2]
        
        return frontmatter + content
    
    def translate_directory(self, input_dir: str, output_dir: Optional[str] = None) -> List[TranslationResult]:
        """
        Translate all markdown files in a directory.
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path (optional)
        
        Returns:
            List of TranslationResult objects
        """
        input_path = Path(input_dir)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        markdown_files = list(input_path.rglob('*.md'))
        results = []
        
        for md_file in markdown_files:
            if output_dir:
                # Preserve directory structure
                rel_path = md_file.relative_to(input_path)
                out_file = Path(output_dir) / rel_path
            else:
                out_file = None
            
            try:
                result = self.translate_file(str(md_file), str(out_file) if out_file else None)
                results.append(result)
                print(f"✓ Translated: {md_file.name} -> {result.output_file}")
            except Exception as e:
                print(f"✗ Error translating {md_file.name}: {e}")
        
        return results


def translate_to_urdu(
    content: str,
    preserve_technical_terms: bool = True
) -> str:
    """
    Convenience function to translate content to Urdu.
    
    Args:
        content: Markdown content to translate
        preserve_technical_terms: Whether to keep technical terms in English
    
    Returns:
        Translated Urdu markdown content
    """
    translator = UrduTechnicalTranslator()
    
    if not preserve_technical_terms:
        # Allow translation of technical terms too
        translator.TECHNICAL_TERMS = set()
    
    return translator.translate_markdown(content)


# Example usage
if __name__ == "__main__":
    # Example content
    sample_content = """
# Introduction to ROS 2

ROS 2 is a middleware for robotics. It helps different parts of a robot communicate with each other.

## What You'll Learn

- Understand what ROS 2 is
- Create your first node
- Publish and subscribe to topics

## Code Example

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.publisher = self.create_publisher(String, 'topic', 10)
```

This code creates a ROS 2 node with a publisher.
"""
    
    translator = UrduTechnicalTranslator()
    translated = translator.translate_markdown(sample_content)
    
    print("=" * 60)
    print("ORIGINAL")
    print("=" * 60)
    print(sample_content)
    
    print("\n" + "=" * 60)
    print("URDU TRANSLATION")
    print("=" * 60)
    print(translated)
