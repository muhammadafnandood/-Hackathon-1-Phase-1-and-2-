---
sidebar_label: '2. Voice-to-Action'
---

# Chapter 2: Voice-to-Action Commands

## Learning Objectives

By the end of this chapter, you will be able to:

- Implement speech-to-text using OpenAI Whisper
- Convert voice commands to robot actions in real-time
- Build a voice-controlled robot system
- Handle noisy audio and speech recognition errors
- Integrate Whisper with ROS2 for hands-free robot control

## Concept Explanation

### OpenAI Whisper for Robotics

**Whisper** is a state-of-the-art speech recognition model that transcribes voice to text:

```
┌─────────────────────────────────────────────────────────────┐
│                  WHISPER FOR ROBOTICS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Audio Input    →    Whisper Model    →    Text Output      │
│  ───────────         ──────────────         ───────────      │
│                                                              │
│  • USB Microphone    • Transformer-based   • Transcription  │
│  • 16kHz audio       • Multilingual        • Timestamps     │
│  • Real-time         • Noise-robust        • Confidence     │
│                                                              │
│  Whisper Variants:                                           │
│  ───────────────────                                         │
│  • whisper.tiny     (39M params)  - Fastest, less accurate  │
│  • whisper.base     (74M params)  - Fast, good accuracy     │
│  • whisper.small    (244M params) - Balanced                │
│  • whisper.medium   (769M params) - High accuracy           │
│  • whisper.large    (1.5B params) - Best accuracy           │
│                                                              │
│  Recommendation for Robotics: whisper.small or whisper.base │
│  (balance between speed and accuracy)                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Benefits for Robotics:**

- **Real-time**: Low latency for responsive control
- **Robust**: Works in noisy environments
- **Multilingual**: Supports 99+ languages
- **Offline**: No internet required after download

### Voice-to-Action Pipeline

**Complete voice control system:**

```
┌─────────────────────────────────────────────────────────────┐
│              VOICE-TO-ACTION PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Audio Capture                                            │
│     ────────────────                                         │
│     • USB microphone (16kHz, 16-bit)                        │
│     • Audio buffer (VAD for silence detection)              │
│                                                              │
│  2. Speech Recognition                                       │
│     ───────────────────                                      │
│     • Whisper model                                         │
│     • Real-time transcription                               │
│     • Language detection                                    │
│                                                              │
│  3. Command Parsing                                          │
│     ────────────────                                         │
│     • Extract intent                                        │
│     • Identify parameters                                   │
│     • Validate command                                      │
│                                                              │
│  4. Action Execution                                         │
│     ─────────────────                                        │
│     • Convert to ROS2 commands                              │
│     • Execute on robot                                      │
│     • Provide feedback                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Real-time Audio Processing

**Audio pipeline** for continuous voice control:

```
┌─────────────────────────────────────────────────────────────┐
│              REAL-TIME AUDIO PROCESSING                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Microphone  │───►│    VAD       │───►│   Whisper    │  │
│  │  (Audio In)  │    │  (Voice      │    │  (STT)       │  │
│  │              │    │   Activity   │    │              │  │
│  │              │    │   Detection) │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│         │                   │                   │           │
│    Continuous            Detects             Transcribes    │
│    audio stream          speech              to text        │
│                                                              │
│  VAD Benefits:                                               │
│  ───────────                                                 │
│  • Reduces processing (only process speech)                 │
│  • Filters background noise                                 │
│  • Detects speech boundaries                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### Amazon Alexa for Warehouse Robots

Amazon uses **voice control** for warehouse operations:

```
┌────────────────────────────────────────────────────────┐
│         AMAZON WAREHOUSE VOICE CONTROL                  │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Application: Inventory Management                     │
│  ───────────────────────────────                        │
│                                                         │
│  Voice Commands:                                        │
│  ──────────────                                         │
│  • "Navigate to aisle B-12"                            │
│  • "Pick up item SKU-12345"                            │
│  • "Scan barcode"                                      │
│  • "Return to charging station"                        │
│                                                         │
│  Benefits:                                              │
│  ────────                                               │
│  • Hands-free operation                                │
│  • Faster task execution                               │
│  • Reduced training time                               │
│  • Multi-language support                              │
│                                                         │
│  Performance:                                           │
│  ───────────                                            │
│  • 95%+ recognition accuracy                           │
│  • < 500ms latency                                     │
│  • Works in noisy warehouse                            │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete Voice Control System

```
┌─────────────────────────────────────────────────────────────┐
│              VOICE CONTROL ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  Audio       │                                           │
│  │  Input       │                                           │
│  │  (USB Mic)   │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  PyAudio     │───►│    VAD       │───►│   Whisper    │  │
│  │  (Capture)   │    │  (webrtc)    │    │   (STT)      │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│                                                  │           │
│                                                  ▼           │
│                                         ┌──────────────┐   │
│                                         │  Command     │   │
│                                         │  Parser      │   │
│                                         └──────┬───────┘   │
│                                                │            │
│                                                ▼            │
│                                         ┌──────────────┐   │
│                                         │  LLM Bridge  │   │
│                                         │  (ROS2)      │   │
│                                         └──────────────┘   │
│                                                              │
│  ROS2 Topics:                                                │
│  • /audio/raw         ← Raw audio data                      │
│  • /audio/processed   ← VAD-filtered audio                  │
│  • /voice/text        ← Transcribed text                    │
│  • /voice/command     ← Parsed command                      │
│  • /cmd_vel           ← Robot velocity                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Whisper Voice Recognition Node

```python
#!/usr/bin/env python3
"""
Whisper-based voice recognition for robot control.
Module 4 - Chapter 2
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pyaudio
import whisper
import numpy as np
from webrtcvad import Vad
import threading


class WhisperVoiceNode(Node):
    """Voice recognition node using Whisper."""
    
    def __init__(self):
        super().__init__('whisper_voice_node')
        
        # Publisher for transcribed text
        self.text_pub = self.create_publisher(
            String,
            '/voice/text',
            10
        )
        
        # Load Whisper model
        self.declare_parameter('model_size', 'base')
        model_size = self.get_parameter('model_size').value
        self.get_logger().info(f'Loading Whisper model: {model_size}')
        self.model = whisper.load_model(model_size)
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_buffer = []
        self.is_speaking = False
        
        # VAD (Voice Activity Detection)
        self.vad = Vad(3)  # Aggressiveness level 3
        
        # Audio stream
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self.audio_callback
        )
        
        self.get_logger().info('Whisper Voice Node started')
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Process audio stream."""
        # Convert to numpy
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        
        # Voice Activity Detection
        is_voice = self.vad.is_speech(audio_data.tobytes(), self.sample_rate)
        
        if is_voice:
            self.audio_buffer.append(audio_data)
            if not self.is_speaking:
                self.is_speaking = True
                self.get_logger().debug('Speech detected')
        else:
            if self.is_speaking and len(self.audio_buffer) > 0:
                # End of speech - transcribe
                self.transcribe_buffer()
            self.audio_buffer = []
            self.is_speaking = False
        
        return (None, pyaudio.paContinue)
    
    def transcribe_buffer(self):
        """Transcribe audio buffer."""
        if len(self.audio_buffer) == 0:
            return
        
        # Concatenate audio
        audio_data = np.concatenate(self.audio_buffer)
        
        # Normalize
        audio_data = audio_data.astype(np.float32) / 32768.0
        
        # Transcribe
        result = self.model.transcribe(audio_data, language='en')
        text = result['text'].strip()
        
        if text:
            self.get_logger().info(f'Transcribed: {text}')
            
            # Publish
            msg = String()
            msg.data = text
            self.text_pub.publish(msg)
        
        # Clear buffer
        self.audio_buffer = []
    
    def destroy_node(self):
        """Cleanup."""
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        super().destroy_node()


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    node = WhisperVoiceNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 2: Voice Command Parser

```python
#!/usr/bin/env python3
"""
Parse voice commands into robot actions.
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class VoiceCommand:
    """Represents a parsed voice command."""
    intent: str
    params: Dict[str, str]
    confidence: float


class VoiceCommandParser:
    """Parse voice commands into structured actions."""
    
    def __init__(self):
        # Intent patterns
        self.patterns = {
            'navigate': [
                r'go to (.+)',
                r'move to (.+)',
                r'navigate to (.+)',
                r'walk to (.+)',
            ],
            'move_forward': [
                r'move forward',
                r'go forward',
                r'go ahead',
            ],
            'move_backward': [
                r'move backward',
                r'go backward',
                r'go back',
            ],
            'turn_left': [
                r'turn left',
                r'rotate left',
                r'spin left',
            ],
            'turn_right': [
                r'turn right',
                r'rotate right',
                r'spin right',
            ],
            'stop': [
                r'stop',
                r'halt',
                r'freeze',
                r'don\'t move',
            ],
            'pick_up': [
                r'pick up (.+)',
                r'grab (.+)',
                r'take (.+)',
            ],
            'place': [
                r'place (?:on|in) (.+)',
                r'put (?:on|in) (.+)',
                r'drop (?:on|in) (.+)',
            ],
        }
    
    def parse(self, text: str) -> Optional[VoiceCommand]:
        """Parse voice text into command."""
        text = text.lower().strip()
        
        # Try each pattern
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.match(pattern, text)
                if match:
                    # Extract parameters
                    params = self._extract_params(intent, match)
                    
                    return VoiceCommand(
                        intent=intent,
                        params=params,
                        confidence=0.9
                    )
        
        # No match found
        return None
    
    def _extract_params(self, intent: str, match) -> Dict[str, str]:
        """Extract parameters from regex match."""
        params = {}
        
        if intent in ['navigate', 'pick_up', 'place']:
            if match.groups():
                params['target'] = match.group(1).strip()
        
        return params


# Example usage
if __name__ == '__main__':
    parser = VoiceCommandParser()
    
    test_commands = [
        "Go to the kitchen",
        "Move forward",
        "Turn left",
        "Pick up the red block",
        "Place on the table",
        "Stop",
    ]
    
    for command in test_commands:
        result = parser.parse(command)
        if result:
            print(f"✓ '{command}' → {result.intent} {result.params}")
        else:
            print(f"✗ '{command}' → No match")
```

### Example 3: Voice-Controlled Robot Launch

```python
#!/usr/bin/env python3
"""
ROS2 Launch file for voice-controlled robot.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description for voice control."""
    
    # Arguments
    whisper_model = DeclareLaunchArgument(
        'whisper_model',
        default_value='base',
        description='Whisper model size (tiny, base, small, medium, large)'
    )
    
    # Whisper voice node
    whisper_node = Node(
        package='voice_control',
        executable='whisper_voice_node',
        name='whisper_voice_node',
        output='screen',
        parameters=[{
            'model_size': LaunchConfiguration('whisper_model'),
        }]
    )
    
    # Command parser
    parser_node = Node(
        package='voice_control',
        executable='command_parser',
        name='command_parser',
        output='screen'
    )
    
    # LLM bridge
    llm_bridge = Node(
        package='llm_robotics',
        executable='llm_robot_bridge',
        name='llm_robot_bridge',
        output='screen'
    )
    
    return LaunchDescription([
        whisper_model,
        whisper_node,
        parser_node,
        llm_bridge,
    ])


if __name__ == '__main__':
    generate_launch_description()
```

## Hands-on Lab

### Lab 2.1: Voice-Controlled Robot

**Objective**: Build a voice-controlled robot using Whisper and ROS2.

**Prerequisites**:
- Python 3.10+
- USB microphone
- ROS2 Humble
- OpenAI Whisper installed

**Duration**: 90 minutes

---

#### Step 1: Install Dependencies

```bash
# Install Whisper
pip3 install openai-whisper

# Install audio libraries
pip3 install pyaudio webrtcvad

# Install ROS2 packages
sudo apt install ros-humble-audio-common
```

#### Step 2: Create Voice Node

Create `whisper_voice_node.py`:

```python
# Copy Example 1 from above
```

#### Step 3: Create Command Parser

Create `command_parser.py`:

```python
# Copy Example 2 from above
```

#### Step 4: Create Launch File

Create `voice_control_launch.py`:

```python
# Copy Example 3 from above
```

#### Step 5: Test Voice Recognition

```bash
# Launch voice control system
ros2 launch voice_control voice_control_launch.py

# Speak commands
"Go to the kitchen"
"Move forward"
"Turn left"
"Stop"

# Monitor output
ros2 topic echo /voice/text
ros2 topic echo /voice/command
```

#### Step 6: Integrate with Robot

```bash
# Start robot simulation
gz sim robot_world.sdf

# Launch voice control
ros2 launch voice_control voice_control_launch.py

# Test voice commands on robot
"Navigate to the red block"
"Pick up the blue cup"
```

**Expected Result**:

Robot responds to voice commands, executes actions, provides audio feedback.

## Summary

### Key Takeaways

1. **Whisper** provides accurate, real-time speech recognition for robotics

2. **Voice Activity Detection** reduces processing by filtering silence

3. **Command Parsing** converts transcribed text to structured actions

4. **Hands-free Control** enables natural human-robot interaction

5. **Noise Robustness** is critical for real-world deployment

### Key Terms

| Term | Definition |
|------|------------|
| **Whisper** | OpenAI's speech-to-text model |
| **VAD** | Voice Activity Detection |
| **STT** | Speech-to-Text |
| **Intent** | The goal of a voice command |
| **Real-time** | Processing with minimal latency |

## Exercises

### Exercise 2.1: Model Comparison

1. Test different Whisper models (tiny, base, small, medium)
2. **Measure** accuracy and latency
3. **Compare** CPU/GPU performance
4. **Recommend** optimal model

### Exercise 2.2: Noise Robustness

1. Test voice recognition in different noise levels
2. **Measure** accuracy degradation
3. **Implement** noise cancellation
4. **Evaluate** improvement

### Exercise 2.3: Multi-language Support

1. Add support for a second language
2. **Test** language detection
3. **Implement** language switching
4. **Document** challenges

### Exercise 2.4: Command Vocabulary

1. Extend command vocabulary to 50+ commands
2. **Add** parameter extraction
3. **Test** command coverage
4. **Optimize** patterns

### Exercise 2.5: Research Question

Research **voice interfaces for robots**:

- Amazon Alexa for Robotics
- Google Assistant integration
- Custom voice assistants

**Write** a 500-word summary comparing approaches.

---

**Next Chapter**: [Chapter 3 — Cognitive Planning →](./chapter3-cognitive-planning.md)
