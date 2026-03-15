---
sidebar_label: '4. Multimodal Interaction'
---

# Chapter 4: Multimodal Robot Interaction

## Learning Objectives

By the end of this chapter, you will be able to:

- Combine voice, vision, and gesture inputs for robot control
- Implement context-aware robot behaviors
- Fuse multiple sensor modalities for robust perception
- Enhance human-robot interaction with multimodal understanding
- Build robots that understand natural human communication

## Concept Explanation

### What is Multimodal Interaction?

**Multimodal interaction** combines multiple input channels for natural human-robot communication:

```
┌─────────────────────────────────────────────────────────────┐
│              MULTIMODAL INTERACTION                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Human Input Modalities                                      │
│  ──────────────────────                                      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Voice      │  │    Vision    │  │   Gesture    │       │
│  │  (Speech)    │  │  (Cameras)   │  │  (Hands)     │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         └────────────────┬┴────────────────┘                │
│                          │                                  │
│                          ▼                                  │
│              ┌───────────────────────┐                     │
│              │  Multimodal Fusion    │                     │
│              │  (Combine & Resolve)  │                     │
│              └───────────┬───────────┘                     │
│                          │                                  │
│                          ▼                                  │
│              ┌───────────────────────┐                     │
│              │  Robot Understanding  │                     │
│              │  "Pick up THAT cup"   │                     │
│              │  (while pointing)     │                     │
│              └───────────┬───────────┘                     │
│                          │                                  │
│                          ▼                                  │
│              ┌───────────────────────┐                     │
│              │  Robot Action         │                     │
│              │  (Grasp indicated cup)│                     │
│              └───────────────────────┘                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Benefits:**

1. **Natural Communication**: Humans use multiple modalities naturally
2. **Robustness**: If one modality fails, others compensate
3. **Disambiguation**: Gestures resolve ambiguous references
4. **Rich Context**: Combined inputs provide more information
5. **Accessibility**: Multiple ways to interact

### Multimodal Fusion

**Fusion strategies** for combining modalities:

```
┌─────────────────────────────────────────────────────────────┐
│                  FUSION STRATEGIES                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Early Fusion (Feature-Level)                                │
│  ──────────────────────────                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐                         │
│  │ Voice  │  │ Vision │  │ Gesture│                         │
│  │Features│  │Features│  │Features│                         │
│  └───┬────┘  └───┬────┘  └───┬────┘                         │
│      │           │           │                               │
│      └───────────┼───────────┘                               │
│                  │                                           │
│                  ▼                                           │
│         ┌────────────────┐                                  │
│         │  Combined      │                                  │
│         │  Feature Vector│                                  │
│         └───────┬────────┘                                  │
│                 │                                           │
│                 ▼                                           │
│         ┌────────────────┐                                  │
│         │  Classification│                                  │
│         │  / Understanding                                │
│         └────────────────┘                                  │
│                                                              │
│  Late Fusion (Decision-Level)                                │
│  ──────────────────────────                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐                         │
│  │ Voice  │  │ Vision │  │ Gesture│                         │
│  │Underst.│  │Underst.│  │Underst.│                         │
│  └───┬────┘  └───┬────┘  └───┬────┘                         │
│      │           │           │                               │
│      └───────────┼───────────┘                               │
│                  │                                           │
│                  ▼                                           │
│         ┌────────────────┐                                  │
│         │  Decision      │                                  │
│         │  Fusion        │                                  │
│         │  (Voting/ML)   │                                  │
│         └────────────────┘                                  │
│                                                              │
│  Recommendation: Late Fusion for robotics                   │
│  (more flexible, easier to debug)                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Context-Aware Understanding

**Context** resolves ambiguity in human commands:

```
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT-AWARE UNDERSTANDING                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Ambiguous Command:                                          │
│  ───────────────────                                         │
│  "Pick that up"                                              │
│                                                              │
│  Context Sources:                                            │
│  ───────────────                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Voice: "Pick that up"                               │   │
│  │  Vision: User pointing at red cup                    │   │
│  │  Gesture: Hand pointing direction detected           │   │
│  │  Environment: Red cup, blue cup, book on table       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Resolution:                                                 │
│  ──────────                                                  │
│  "that" + pointing gesture → red cup                        │
│                                                              │
│  Final Understanding:                                        │
│  ───────────────────                                         │
│  "Pick up the red cup that user is pointing at"             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### Tesla Optimus Multimodal Interface

**Tesla Optimus** uses multimodal interaction for natural communication:

```
┌────────────────────────────────────────────────────────┐
│         TESLA OPTIMUS MULTIMODAL INTERFACE              │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Input Modalities:                                      │
│  ────────────────                                       │
│  • Voice commands (Whisper-based STT)                  │
│  • Hand gestures (Vision-based)                        │
│  • Eye gaze (for attention)                            │
│  • Touch (for physical interaction)                    │
│                                                         │
│  Example Interaction:                                   │
│  ──────────────────                                     │
│  Human: "Put this there" (holding object, pointing)    │
│  Optimus:                                               │
│    1. Recognizes object in human hand (vision)         │
│    2. Detects pointing gesture (vision)                │
│    3. Understands voice command (audio)                │
│    4. Combines modalities to understand intent         │
│    5. Takes object and places at indicated location    │
│                                                         │
│  Key Technologies:                                      │
│  ────────────────                                       │
│  • Occupancy networks for 3D understanding             │
│  • End-to-end neural networks                          │
│  • Transformer-based fusion                            │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete Multimodal System

```
┌─────────────────────────────────────────────────────────────┐
│              MULTIMODAL SYSTEM ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Microphone  │  │   Cameras    │  │  Depth/IMU   │       │
│  │  Array       │  │  (Stereo)    │  │  Sensors     │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         ▼                 ▼                 ▼                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Speech-to-  │  │  Object      │  │  Gesture     │       │
│  │  Text        │  │  Detection   │  │  Recognition │       │
│  │  (Whisper)   │  │  (YOLO)      │  │  (MediaPipe) │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         └────────────────┬┴────────────────┘                │
│                          │                                  │
│                          ▼                                  │
│              ┌───────────────────────┐                     │
│              │  Multimodal Fusion    │                     │
│              │  (LLM-based)          │                     │
│              └───────────┬───────────┘                     │
│                          │                                  │
│                          ▼                                  │
│              ┌───────────────────────┐                     │
│              │  Intent Understanding │                     │
│              └───────────┬───────────┘                     │
│                          │                                  │
│                          ▼                                  │
│              ┌───────────────────────┐                     │
│              │  Robot Action         │                     │
│              │  Execution            │                     │
│              └───────────────────────┘                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Multimodal Fusion Node

```python
#!/usr/bin/env python3
"""
Multimodal fusion for robot interaction.
Module 4 - Chapter 4
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point
from sensor_msgs.msg import Image
import time


class MultimodalFusionNode(Node):
    """Fuse multiple input modalities."""
    
    def __init__(self):
        super().__init__('multimodal_fusion_node')
        
        # Subscribers
        self.voice_sub = self.create_subscription(
            String,
            '/voice/text',
            self.voice_callback,
            10
        )
        
        self.gesture_sub = self.create_subscription(
            Point,
            '/gesture/point',
            self.gesture_callback,
            10
        )
        
        self.vision_sub = self.create_subscription(
            String,
            '/vision/objects',
            self.vision_callback,
            10
        )
        
        # Publisher for fused understanding
        self.understanding_pub = self.create_publisher(
            String,
            '/multimodal/understanding',
            10
        )
        
        # State
        self.latest_voice = None
        self.latest_gesture = None
        self.latest_vision = None
        self.voice_timestamp = None
        
        # Fusion window (seconds)
        self.fusion_window = 2.0
        
        self.get_logger().info('Multimodal Fusion Node started')
    
    def voice_callback(self, msg: String):
        """Process voice input."""
        self.latest_voice = msg.data
        self.voice_timestamp = time.time()
        
        self.get_logger().info(f'Voice: {msg.data}')
        
        # Trigger fusion
        self.attempt_fusion()
    
    def gesture_callback(self, msg: Point):
        """Process gesture input."""
        self.latest_gesture = msg
        
        self.get_logger().info(
            f'Gesture: pointing at ({msg.x:.2f}, {msg.y:.2f}, {msg.z:.2f})'
        )
    
    def vision_callback(self, msg: String):
        """Process vision input."""
        self.latest_vision = msg.data
        
        self.get_logger().info(f'Vision: {msg.data}')
    
    def attempt_fusion(self):
        """Attempt multimodal fusion."""
        if self.latest_voice is None:
            return
        
        # Check if other modalities are recent
        current_time = time.time()
        
        if self.voice_timestamp is None:
            return
        
        time_diff = current_time - self.voice_timestamp
        
        if time_diff > self.fusion_window:
            # Voice is too old, clear
            self.latest_voice = None
            return
        
        # Perform fusion
        understanding = self.fuse_modalities()
        
        if understanding:
            # Publish understanding
            msg = String()
            msg.data = understanding
            self.understanding_pub.publish(msg)
            
            self.get_logger().info(f'Fused understanding: {understanding}')
            
            # Clear state
            self.latest_voice = None
            self.latest_gesture = None
    
    def fuse_modalities(self) -> str:
        """Fuse modalities into understanding."""
        voice = self.latest_voice or ""
        gesture = self.latest_gesture
        vision = self.latest_vision or ""
        
        # Simple rule-based fusion
        understanding = voice
        
        # Add gesture context
        if gesture:
            understanding += f" [pointing at {gesture.x:.1f},{gesture.y:.1f}]"
        
        # Add vision context
        if vision:
            understanding += f" [objects: {vision}]"
        
        return understanding


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    node = MultimodalFusionNode()
    
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

### Example 2: Gesture Recognition

```python
#!/usr/bin/env python3
"""
Hand gesture recognition for robot control.
"""

import cv2
import mediapipe as mp
import numpy as np


class GestureRecognizer:
    """Recognize hand gestures."""
    
    def __init__(self):
        # MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gesture states
        self.current_gesture = None
        self.pointing_direction = None
    
    def detect_gesture(self, frame) -> dict:
        """Detect gesture from camera frame."""
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process
        results = self.hands.process(rgb_frame)
        
        gesture_info = {
            'gesture': None,
            'pointing_direction': None,
            'hand_present': False
        }
        
        if results.multi_hand_landmarks:
            gesture_info['hand_present'] = True
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Get landmark positions
                landmarks = hand_landmarks.landmark
                
                # Detect pointing gesture
                if self._is_pointing(landmarks):
                    gesture_info['gesture'] = 'pointing'
                    gesture_info['pointing_direction'] = \
                        self._get_pointing_direction(landmarks, frame.shape)
                
                # Detect open hand
                elif self._is_open_hand(landmarks):
                    gesture_info['gesture'] = 'open_hand'
                
                # Detect fist
                elif self._is_fist(landmarks):
                    gesture_info['gesture'] = 'fist'
                
                # Draw landmarks
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        
        return gesture_info
    
    def _is_pointing(self, landmarks) -> bool:
        """Check if hand is pointing."""
        # Index finger extended
        index_extended = landmarks[8].y < landmarks[6].y
        
        # Other fingers curled
        middle_curled = landmarks[12].y > landmarks[10].y
        ring_curled = landmarks[16].y > landmarks[14].y
        pinky_curled = landmarks[20].y > landmarks[18].y
        
        return index_extended and middle_curled and ring_curled and pinky_curled
    
    def _get_pointing_direction(self, landmarks, frame_shape) -> tuple:
        """Get pointing direction."""
        # Get wrist and index finger tip
        wrist = landmarks[0]
        index_tip = landmarks[8]
        
        # Calculate direction
        dx = index_tip.x - wrist.x
        dy = index_tip.y - wrist.y
        
        # Normalize
        length = np.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length
        
        return (dx, dy, 0)  # 3D direction
    
    def _is_open_hand(self, landmarks) -> bool:
        """Check if hand is open."""
        # All fingers extended
        for finger_tip, finger_pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            if landmarks[finger_tip].y > landmarks[finger_pip].y:
                return False
        return True
    
    def _is_fist(self, landmarks) -> bool:
        """Check if hand is fist."""
        # All fingers curled
        for finger_tip, finger_pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            if landmarks[finger_tip].y < landmarks[finger_pip].y:
                return False
        return True


# Example usage
if __name__ == '__main__':
    recognizer = GestureRecognizer()
    
    # Open camera
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Detect gesture
        gesture_info = recognizer.detect_gesture(frame)
        
        # Display
        if gesture_info['gesture']:
            cv2.putText(
                frame,
                f"Gesture: {gesture_info['gesture']}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
        
        cv2.imshow('Gesture Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
```

### Example 3: Context-Aware Command Parser

```python
#!/usr/bin/env python3
"""
Parse commands with multimodal context.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MultimodalContext:
    """Context from multiple modalities."""
    voice_text: str
    pointing_direction: Optional[tuple]
    detected_objects: List[str]
    object_locations: Dict[str, tuple]


class ContextAwareParser:
    """Parse commands with multimodal context."""
    
    def __init__(self):
        self.demonstrative_words = ['this', 'that', 'these', 'those', 'it']
    
    def parse(self, context: MultimodalContext) -> Dict:
        """Parse command with context."""
        voice = context.voice_text.lower()
        pointing = context.pointing_direction
        objects = context.detected_objects
        locations = context.object_locations
        
        # Check for demonstrative reference
        has_demonstrative = any(
            word in voice for word in self.demonstrative_words
        )
        
        if has_demonstrative and pointing:
            # Resolve "that" to pointed object
            target_object = self._resolve_pointing(
                pointing, objects, locations
            )
            
            # Replace demonstrative with object
            resolved_command = self._replace_demonstrative(
                voice, target_object
            )
        else:
            resolved_command = voice
            target_object = None
        
        # Parse action
        action = self._parse_action(resolved_command)
        
        return {
            'action': action,
            'target': target_object,
            'original_command': context.voice_text,
            'resolved_command': resolved_command,
            'used_gesture': pointing is not None
        }
    
    def _resolve_pointing(
        self,
        pointing: tuple,
        objects: List[str],
        locations: Dict[str, tuple]
    ) -> Optional[str]:
        """Resolve pointing direction to object."""
        if not objects:
            return None
        
        # Find closest object to pointing direction
        best_object = None
        best_score = -1
        
        for obj in objects:
            if obj in locations:
                obj_loc = locations[obj]
                
                # Calculate alignment with pointing direction
                score = self._calculate_alignment(pointing, obj_loc)
                
                if score > best_score:
                    best_score = score
                    best_object = obj
        
        return best_object
    
    def _calculate_alignment(
        self,
        pointing: tuple,
        object_location: tuple
    ) -> float:
        """Calculate alignment between pointing and object."""
        # Simple dot product
        dot = sum(p * o for p, o in zip(pointing, object_location))
        return dot
    
    def _replace_demonstrative(
        self,
        command: str,
        target_object: Optional[str]
    ) -> str:
        """Replace demonstrative with object name."""
        if not target_object:
            return command
        
        for word in self.demonstrative_words:
            if word in command:
                return command.replace(word, f"the {target_object}")
        
        return command
    
    def _parse_action(self, command: str) -> str:
        """Parse action from command."""
        command = command.lower()
        
        if 'pick' in command or 'grab' in command:
            return 'pick_up'
        elif 'place' in command or 'put' in command:
            return 'place'
        elif 'move' in command:
            return 'move'
        elif 'navigate' in command or 'go' in command:
            return 'navigate'
        elif 'stop' in command:
            return 'stop'
        else:
            return 'unknown'


# Example usage
if __name__ == '__main__':
    parser = ContextAwareParser()
    
    # Example 1: With pointing
    context1 = MultimodalContext(
        voice_text="Pick that up",
        pointing_direction=(0.5, 0.3, 0.1),
        detected_objects=['red_cup', 'blue_cup', 'book'],
        object_locations={
            'red_cup': (0.5, 0.3, 0.5),
            'blue_cup': (-0.3, 0.2, 0.4),
            'book': (0.1, -0.4, 0.3)
        }
    )
    
    result1 = parser.parse(context1)
    print("Example 1 (with pointing):")
    print(f"  Original: {context1.voice_text}")
    print(f"  Resolved: {result1['resolved_command']}")
    print(f"  Target: {result1['target']}")
    print(f"  Action: {result1['action']}")
    
    # Example 2: Without pointing
    context2 = MultimodalContext(
        voice_text="Pick up the red cup",
        pointing_direction=None,
        detected_objects=['red_cup', 'blue_cup'],
        object_locations={}
    )
    
    result2 = parser.parse(context2)
    print("\nExample 2 (without pointing):")
    print(f"  Original: {context2.voice_text}")
    print(f"  Resolved: {result2['resolved_command']}")
    print(f"  Target: {result2['target']}")
    print(f"  Action: {result2['action']}")
```

## Hands-on Lab

### Lab 4.1: Multimodal Robot Interaction

**Objective**: Build a robot that understands voice + gesture commands.

**Prerequisites**:
- Python 3.10+
- Webcam
- Microphone
- ROS2 Humble
- MediaPipe installed

**Duration**: 120 minutes

---

#### Step 1: Install Dependencies

```bash
# Install MediaPipe
pip3 install mediapipe

# Install OpenCV
pip3 install opencv-python

# Install ROS2 packages
sudo apt install ros-humble-sensor-msgs
```

#### Step 2: Create Gesture Recognizer

Create `gesture_recognizer.py`:

```python
# Copy Example 2 from above
```

#### Step 3: Create Fusion Node

Create `multimodal_fusion.py`:

```python
# Copy Example 1 from above
```

#### Step 4: Create Context Parser

Create `context_parser.py`:

```python
# Copy Example 3 from above
```

#### Step 5: Integration Test

```bash
# Start camera node
python3 gesture_camera_node.py

# Start voice node
python3 whisper_voice_node.py

# Start fusion node
python3 multimodal_fusion.py

# Test combined commands
# Say "Pick that up" while pointing at object
```

#### Step 6: Evaluate Performance

```bash
# Test 10 commands with gestures
# Measure accuracy
# Test 10 commands without gestures
# Compare accuracy
```

**Expected Result**:

Robot understands "Pick that up" + pointing gesture, correctly identifies target object, executes action.

## Summary

### Key Takeaways

1. **Multimodal Interaction** combines voice, vision, and gestures for natural communication

2. **Fusion Strategies** include early (feature-level) and late (decision-level) fusion

3. **Context Awareness** resolves ambiguous references using multiple modalities

4. **Gesture Recognition** enables pointing and hand signal understanding

5. **Robustness** improves when modalities complement each other

### Key Terms

| Term | Definition |
|------|------------|
| **Multimodal** | Using multiple input/output channels |
| **Fusion** | Combining information from multiple modalities |
| **Gesture Recognition** | Detecting and interpreting hand gestures |
| **Context-Aware** | Understanding commands using situational context |
| **Demonstrative** | Words like "this", "that" that reference objects |

## Exercises

### Exercise 4.1: Fusion Strategy Comparison

1. Implement early fusion
2. Implement late fusion
3. **Compare** accuracy and latency
4. **Recommend** optimal approach

### Exercise 4.2: Gesture Vocabulary

1. Define 10 hand gestures
2. **Train** gesture classifier
3. **Test** recognition accuracy
4. **Document** confusion matrix

### Exercise 4.3: Ambiguity Resolution

1. Create ambiguous commands dataset
2. **Test** resolution with/without gestures
3. **Measure** improvement
4. **Analyze** failure cases

### Exercise 4.4: Multi-Person Interaction

1. Detect multiple people
2. **Track** who is speaking/gesturing
3. **Associate** commands with correct person
4. **Test** in group setting

### Exercise 4.5: Research Assignment

Research **multimodal HRI systems**:

- Honda ASIMO
- SoftBank Pepper
- Boston Dynamics Atlas
- Research prototypes

**Write** a 600-word summary comparing interaction modalities.

---

**Next Chapter**: [Chapter 5 — Conversational Robotics →](./chapter5-conversational-robotics.md)
