---
sidebar_label: '5. Conversational Robotics'
---

# Chapter 5: Conversational Robotics Systems

## Learning Objectives

By the end of this chapter, you will be able to:

- Build voice-based interactive robot systems
- Implement multi-turn dialog with LLMs
- Integrate VLA (Vision-Language-Action) perception-action pipeline
- Create robots that maintain conversation context
- Deploy full conversational robotics systems

## Concept Explanation

### What are Conversational Robots?

**Conversational robots** engage in natural dialog while performing physical tasks:

```
┌─────────────────────────────────────────────────────────────┐
│              CONVERSATIONAL ROBOTICS                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Human: "Can you bring me a coffee?"                        │
│                                                              │
│         ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Robot Processing                         │   │
│  │                                                       │   │
│  │  1. Understand request (NLP)                         │   │
│  │  2. Check coffee availability (perception)           │   │
│  │  3. Plan actions (planning)                          │   │
│  │  4. Respond verbally (TTS)                           │   │
│  │     "Sure! I'll get you a coffee."                   │   │
│  │  5. Execute actions (control)                        │   │
│  └──────────────────────────────────────────────────────┘   │
│         ↓                                                    │
│  Robot: [Navigates to kitchen, makes coffee, returns]       │
│                                                              │
│  Human: "Thanks!"                                           │
│  Robot: "You're welcome! Anything else?"                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Capabilities:**

1. **Natural Dialog**: Multi-turn conversation
2. **Task Execution**: Physical action while talking
3. **Context Memory**: Remember conversation history
4. **Clarification**: Ask questions when uncertain
5. **Personality**: Consistent communication style

### VLA Pipeline Integration

**Vision-Language-Action (VLA)** integrates perception, understanding, and action:

```
┌─────────────────────────────────────────────────────────────┐
│                  VLA PIPELINE                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Vision     │    │   Language   │    │    Action    │  │
│  │  (Perceive)  │───►│ (Understand) │───►│  (Execute)   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│         │                   │                   │           │
│    • Cameras           • LLM              • Motor           │
│    • LiDAR             • Dialog           • Navigation      │
│    • Depth             • Planning         • Manipulation    │
│                                                              │
│  Integration Points:                                         │
│  ───────────────────                                         │
│  • Vision → Language: Describe scene                        │
│  • Language → Action: Execute commands                      │
│  • Action → Vision: Verify results                          │
│  • Vision → Action: Direct manipulation                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Multi-Turn Dialog Management

**Dialog state** tracks conversation progress:

```
┌─────────────────────────────────────────────────────────────┐
│              DIALOG STATE MANAGEMENT                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Dialog State:                                               │
│  ─────────────                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Current Goal: Serve coffee                          │   │
│  │  Sub-goals:                                          │   │
│  │    ✓ Navigate to kitchen                            │   │
│  │    ✓ Make coffee                                    │   │
│  │    ⏳ Return to user                                │   │
│  │  Conversation History:                               │   │
│  │    H: "Can you bring me coffee?"                    │   │
│  │    R: "Sure! How do you like it?"                   │   │
│  │    H: "With milk, please"                           │   │
│  │    R: "Got it! One coffee with milk."               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  State Transitions:                                          │
│  ─────────────────                                           │
│  Greeting → Request → Clarification → Execution → Complete  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### Figure 01 Conversational Humanoid

**Figure 01** demonstrates advanced conversational robotics:

```
┌────────────────────────────────────────────────────────┐
│         FIGURE 01 CONVERSATIONAL HUMANOID               │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Capabilities:                                          │
│  ────────────                                           │
│  • Natural language conversation                       │
│  • Task execution while talking                        │
│  • Context-aware responses                             │
│  • Multi-modal interaction                             │
│                                                         │
│  Example Interaction:                                   │
│  ──────────────────                                     │
│  Human: "I'm hungry, can you get me something?"        │
│  Figure 01:                                             │
│    "Let me check what's available."                    │
│    [Looks at table with cameras]                       │
│    "I see an apple and a sandwich. Which would you     │
│     prefer?"                                           │
│  Human: "The sandwich, please"                         │
│  Figure 01:                                             │
│    "Sure! Here you go."                                │
│    [Picks up sandwich, hands to human]                 │
│                                                         │
│  Key Technologies:                                      │
│  ────────────────                                       │
│  • LLM for dialog generation                           │
│  • Vision for object recognition                       │
│  • Manipulation for object handling                    │
│  • TTS for natural speech                              │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete Conversational Robot System

```
┌─────────────────────────────────────────────────────────────┐
│          CONVERSATIONAL ROBOT SYSTEM                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  User        │                                           │
│  │  (Voice)     │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Speech-to-  │───►│  Dialog      │───►│  Text-to-    │  │
│  │  Text        │    │  Manager     │    │  Speech      │  │
│  │  (Whisper)   │    │  (LLM)       │    │  (TTS)       │  │
│  └──────────────┘    └──────┬───────┘    └──────────────┘  │
│                             │                                │
│                    ┌────────▼───────┐                       │
│                    │  Vision        │                       │
│                    │  (Perception)  │                       │
│                    └────────┬───────┘                       │
│                             │                                │
│                    ┌────────▼───────┐                       │
│                    │  Action        │                       │
│                    │  Planner       │                       │
│                    └────────┬───────┘                       │
│                             │                                │
│                    ┌────────▼───────┐                       │
│                    │  Robot         │                       │
│                    │  Controller    │                       │
│                    └────────────────┘                       │
│                                                              │
│  Dialog State: Maintains conversation context               │
│  Task State: Tracks action execution progress               │
│  Memory: Stores long-term knowledge about user              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Conversational Robot Node

```python
#!/usr/bin/env python3
"""
Conversational robot with dialog management.
Module 4 - Chapter 5
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai
import os
from typing import List, Dict


class ConversationalRobot(Node):
    """Conversational robot with dialog management."""
    
    def __init__(self):
        super().__init__('conversational_robot')
        
        # Initialize OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Subscribers
        self.voice_sub = self.create_subscription(
            String,
            '/voice/text',
            self.voice_callback,
            10
        )
        
        # Publishers
        self.response_pub = self.create_publisher(
            String,
            '/robot/response',
            10
        )
        
        self.cmd_pub = self.create_publisher(
            String,
            '/robot/command',
            10
        )
        
        # Dialog state
        self.conversation_history: List[Dict] = []
        self.current_task = None
        self.task_state = "idle"
        
        # System prompt
        self.system_prompt = """You are a helpful humanoid robot assistant.
You can:
- Navigate to locations
- Pick up and place objects
- Answer questions about your environment

Always respond in a friendly, concise manner.
If you need to perform an action, include it in your response like:
[ACTION: navigate to kitchen]
[ACTION: pick up cup]

Current capabilities:
- Navigate: kitchen, living room, bedroom
- Objects: cup, book, phone, remote
- Actions: pick up, place, open, close"""
        
        self.get_logger().info('Conversational Robot started')
    
    def voice_callback(self, msg: String):
        """Process user voice input."""
        user_text = msg.data
        self.get_logger().info(f'User: {user_text}')
        
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_text
        })
        
        # Get LLM response
        response = self.get_llm_response()
        
        # Extract actions from response
        actions = self.extract_actions(response)
        
        # Publish response (for TTS)
        response_msg = String()
        response_msg.data = self.clean_response(response)
        self.response_pub.publish(response_msg)
        
        # Execute actions
        for action in actions:
            self.execute_action(action)
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Limit history length
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_llm_response(self) -> str:
        """Get response from LLM."""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[-10:])  # Last 10 messages
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content
    
    def extract_actions(self, response: str) -> List[Dict]:
        """Extract actions from response."""
        import re
        
        actions = []
        action_pattern = r'\[ACTION:\s*([^\]]+)\]'
        
        matches = re.findall(action_pattern, response)
        
        for match in matches:
            parts = match.split()
            if len(parts) >= 2:
                action = {
                    "type": parts[0],
                    "target": " ".join(parts[1:])
                }
                actions.append(action)
        
        return actions
    
    def clean_response(self, response: str) -> str:
        """Remove action tags from response for TTS."""
        import re
        return re.sub(r'\[ACTION:[^\]]+\]', '', response).strip()
    
    def execute_action(self, action: Dict):
        """Execute robot action."""
        action_type = action.get('type')
        target = action.get('target')
        
        self.get_logger().info(f'Executing: {action_type} {target}')
        
        # Publish command
        cmd_msg = String()
        cmd_msg.data = f"{action_type}:{target}"
        self.cmd_pub.publish(cmd_msg)
        
        # Update task state
        self.current_task = action
        self.task_state = "executing"


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    robot = ConversationalRobot()
    
    try:
        rclpy.spin(robot)
    except KeyboardInterrupt:
        pass
    finally:
        robot.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 2: Dialog State Manager

```python
#!/usr/bin/env python3
"""
Dialog state management for conversational robots.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import time


class DialogState(Enum):
    """Dialog states."""
    GREETING = "greeting"
    LISTENING = "listening"
    PROCESSING = "processing"
    CLARIFYING = "clarifying"
    EXECUTING = "executing"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a task."""
    description: str
    subtasks: List[str] = field(default_factory=list)
    completed_subtasks: List[str] = field(default_factory=list)
    status: str = "pending"


class DialogStateManager:
    """Manage dialog state for conversational robot."""
    
    def __init__(self):
        self.state = DialogState.GREETING
        self.conversation_history: List[Dict] = []
        self.current_task: Optional[Task] = None
        self.user_preferences: Dict = {}
        self.context: Dict = {}
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
    
    def get_context_summary(self) -> str:
        """Get summary of conversation context."""
        if not self.conversation_history:
            return "No conversation history"
        
        # Get last few messages
        recent = self.conversation_history[-6:]
        
        summary = "Recent conversation:\n"
        for msg in recent:
            summary += f"{msg['role']}: {msg['content']}\n"
        
        if self.current_task:
            summary += f"\nCurrent task: {self.current_task.description}"
            summary += f"\nProgress: {len(self.current_task.completed_subtasks)}/{len(self.current_task.subtasks)}"
        
        return summary
    
    def start_task(self, description: str, subtasks: List[str]):
        """Start a new task."""
        self.current_task = Task(
            description=description,
            subtasks=subtasks
        )
        self.state = DialogState.EXECUTING
    
    def complete_subtask(self, subtask: str):
        """Mark subtask as complete."""
        if self.current_task and subtask in self.current_task.subtasks:
            if subtask not in self.current_task.completed_subtasks:
                self.current_task.completed_subtasks.append(subtask)
            
            # Check if task is complete
            if len(self.current_task.completed_subtasks) >= len(self.current_task.subtasks):
                self.current_task.status = "complete"
                self.state = DialogState.COMPLETE
    
    def set_user_preference(self, key: str, value):
        """Store user preference."""
        self.user_preferences[key] = value
    
    def get_user_preference(self, key: str, default=None):
        """Get user preference."""
        return self.user_preferences.get(key, default)
    
    def update_context(self, key: str, value):
        """Update context."""
        self.context[key] = value
    
    def get_context(self, key: str, default=None):
        """Get context value."""
        return self.context.get(key, default)


# Example usage
if __name__ == '__main__':
    manager = DialogStateManager()
    
    # Simulate conversation
    manager.add_message("user", "Can you bring me coffee?")
    manager.add_message("assistant", "Sure! How do you like your coffee?")
    manager.add_message("user", "With milk, please")
    
    # Store preference
    manager.set_user_preference("coffee", "with milk")
    
    # Start task
    manager.start_task(
        "Bring coffee to user",
        ["Navigate to kitchen", "Make coffee", "Return to user", "Serve coffee"]
    )
    
    # Complete subtasks
    manager.complete_subtask("Navigate to kitchen")
    manager.complete_subtask("Make coffee")
    
    # Get context
    print("Context Summary:")
    print(manager.get_context_summary())
    
    print(f"\nUser prefers coffee: {manager.get_user_preference('coffee')}")
```

### Example 3: Full VLA Integration

```python
#!/usr/bin/env python3
"""
Full VLA (Vision-Language-Action) integration.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
import numpy as np


class VLAIntegrator(Node):
    """Integrate Vision-Language-Action pipeline."""
    
    def __init__(self):
        super().__init__('vla_integrator')
        
        # Subscribers
        self.voice_sub = self.create_subscription(
            String,
            '/voice/text',
            self.voice_callback,
            10
        )
        
        self.vision_sub = self.create_subscription(
            Image,
            '/camera/image',
            self.vision_callback,
            10
        )
        
        # Publishers
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        self.tts_pub = self.create_publisher(
            String,
            '/tts/text',
            10
        )
        
        # State
        self.latest_image = None
        self.detected_objects = []
        self.current_instruction = None
        
        self.get_logger().info('VLA Integrator started')
    
    def voice_callback(self, msg: String):
        """Process voice instruction."""
        instruction = msg.data
        self.current_instruction = instruction
        
        self.get_logger().info(f'Instruction: {instruction}')
        
        # Process with vision context
        self.process_vla(instruction)
    
    def vision_callback(self, msg: Image):
        """Process vision input."""
        # Convert ROS image to OpenCV
        self.latest_image = self.ros_to_cv2(msg)
        
        # Detect objects
        self.detected_objects = self.detect_objects(self.latest_image)
    
    def process_vla(self, instruction: str):
        """Process VLA pipeline."""
        # Get vision context
        vision_context = self.get_vision_context()
        
        # Combine with language
        full_context = f"Instruction: {instruction}\nVision: {vision_context}"
        
        self.get_logger().info(f'Full context: {full_context}')
        
        # Generate action (simplified - would use LLM in practice)
        action = self.generate_action(instruction, vision_context)
        
        # Execute
        self.execute_action(action)
        
        # Respond
        self.respond(action)
    
    def get_vision_context(self) -> str:
        """Get vision context."""
        if not self.detected_objects:
            return "No objects detected"
        
        return f"Detected: {', '.join(self.detected_objects)}"
    
    def detect_objects(self, image) -> List[str]:
        """Detect objects in image (simplified)."""
        # In practice, use YOLO, DETR, etc.
        # For demo, return placeholder
        return ["cup", "table", "chair"]
    
    def generate_action(self, instruction: str, context: str) -> Dict:
        """Generate action from instruction and context."""
        # Simplified action generation
        if "navigate" in instruction.lower() or "go" in instruction.lower():
            return {"type": "navigate", "target": "kitchen"}
        elif "pick" in instruction.lower():
            return {"type": "pick", "object": "cup"}
        else:
            return {"type": "unknown"}
    
    def execute_action(self, action: Dict):
        """Execute action."""
        action_type = action.get('type')
        
        if action_type == "navigate":
            cmd = Twist()
            cmd.linear.x = 0.3
            self.cmd_pub.publish(cmd)
        elif action_type == "pick":
            # Control arm/gripper (not shown)
            pass
    
    def respond(self, action: Dict):
        """Generate verbal response."""
        action_type = action.get('type')
        
        if action_type == "navigate":
            response = "I'm on my way."
        elif action_type == "pick":
            response = "I've got it."
        else:
            response = "I understand."
        
        msg = String()
        msg.data = response
        self.tts_pub.publish(msg)
    
    def ros_to_cv2(self, ros_image):
        """Convert ROS image to OpenCV format."""
        # Simplified conversion
        return np.frombuffer(ros_image.data, dtype=np.uint8).reshape(
            (ros_image.height, ros_image.width, -1)
        )


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    integrator = VLAIntegrator()
    
    try:
        rclpy.spin(integrator)
    except KeyboardInterrupt:
        pass
    finally:
        integrator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Hands-on Lab

### Lab 5.1: Build Conversational Robot

**Objective**: Create a full conversational robot with VLA integration.

**Prerequisites**:
- Python 3.10+
- ROS2 Humble
- OpenAI API key
- Chapters 1-4 completed

**Duration**: 120 minutes

---

#### Step 1: Create Conversational Robot Node

Create `conversational_robot.py`:

```python
# Copy Example 1 from above
```

#### Step 2: Create Dialog State Manager

Create `dialog_manager.py`:

```python
# Copy Example 2 from above
```

#### Step 3: Create VLA Integrator

Create `vla_integrator.py`:

```python
# Copy Example 3 from above
```

#### Step 4: Integration Test

```bash
# Start all nodes
ros2 launch conversational_robot full_system_launch.py

# Test conversation
# Say: "Can you bring me a coffee?"
# Robot should respond and execute actions
```

#### Step 5: Multi-Turn Test

```bash
# Test multi-turn dialog
Human: "I'm hungry"
Robot: "What would you like to eat?"
Human: "Get me an apple"
Robot: "Sure! I'll get you an apple."
```

#### Step 6: Evaluate System

```bash
# Test 10 different instructions
# Measure:
# - Response time
# - Action accuracy
# - Dialog naturalness
# - Task completion rate
```

**Expected Result**:

Robot engages in natural conversation, understands instructions, executes tasks, maintains context across multiple turns.

## Summary

### Key Takeaways

1. **Conversational Robots** combine dialog with physical action execution

2. **Dialog Management** tracks conversation state and task progress

3. **VLA Integration** combines vision, language, and action seamlessly

4. **Multi-Turn Dialog** requires context memory and state tracking

5. **Full System** integrates STT, LLM, TTS, perception, and control

### Key Terms

| Term | Definition |
|------|------------|
| **Conversational Robot** | Robot that engages in dialog while acting |
| **Dialog State** | Current state of conversation |
| **VLA** | Vision-Language-Action integration |
| **Multi-Turn** | Conversation with multiple exchanges |
| **Context Memory** | Remembering conversation history |

## Exercises

### Exercise 5.1: Dialog Flow Design

1. Design dialog flow for 5 tasks
2. **Map** all possible user responses
3. **Implement** state machine
4. **Test** edge cases

### Exercise 5.2: Personality Development

1. Define robot personality traits
2. **Customize** LLM prompts
3. **Test** consistency
4. **Evaluate** user perception

### Exercise 5.3: Error Handling

1. Identify failure modes
2. **Implement** recovery dialogs
3. **Test** with ambiguous inputs
4. **Measure** user satisfaction

### Exercise 5.4: Long-Term Memory

1. Implement user preference storage
2. **Add** recall in conversations
3. **Test** personalization
4. **Evaluate** user experience

### Exercise 5.5: Research Assignment

Research **conversational robotics**:

- MIT Jibo
- Amazon Astro
- Google Assistant robots
- Research prototypes

**Write** a 600-word summary comparing dialog capabilities.

---

## Module 4 Complete! 🎉

You have learned:
- LLMs for robot decision-making
- Voice-to-action with Whisper
- Cognitive planning with LLMs
- Multimodal interaction (voice + vision + gesture)
- Conversational robotics systems

**Next Module**: [Module 5 — Capstone Project →](../capstone/autonomous-humanoid.md)
