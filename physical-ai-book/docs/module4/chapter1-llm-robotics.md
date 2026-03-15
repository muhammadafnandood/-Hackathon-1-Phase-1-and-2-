---
sidebar_label: '1. LLMs in Robotics'
---

# Chapter 1: Large Language Models in Robotics

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the role of Large Language Models (LLMs) in robot decision-making
- Connect natural language instructions with robot actions
- Implement LLM-based task planning for robotic systems
- Understand AI-native cognitive architectures for robotics
- Deploy LLM-powered robot control systems

## Concept Explanation

### What are LLMs in Robotics?

**Large Language Models (LLMs)** are transforming robotics by serving as the **cognitive brain** that translates human language into robot actions:

```
┌─────────────────────────────────────────────────────────────┐
│                  LLM-POWERED ROBOTICS                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Human Input              LLM Processing         Robot       │
│  ───────────              ──────────────         ──────      │
│                                                              │
│  "Pick up the red        ┌──────────────┐      Execute      │
│   block and put          │     LLM      │      Actions      │
│   it on the table"  ────►│  (GPT-4,     │─────►/cmd_vel     │
│                          │   Llama,     │      /joint_cmd   │
│                          │   etc.)      │      /gripper_cmd │
│                          └──────┬───────┘                   │
│                                 │                            │
│                                 ▼                            │
│                    ┌────────────────────────┐               │
│                    │  Action Sequence       │               │
│                    │  1. Navigate to block  │               │
│                    │  2. Detect red object  │               │
│                    │  3. Move arm to block  │               │
│                    │  4. Close gripper      │               │
│                    │  5. Move to table      │               │
│                    │  6. Open gripper       │               │
│                    └────────────────────────┘               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Capabilities:**

1. **Natural Language Understanding**: Parse human instructions
2. **Task Decomposition**: Break complex tasks into executable steps
3. **Context Awareness**: Understand environment and robot state
4. **Error Recovery**: Handle failures and replan
5. **Learning from Feedback**: Improve from human corrections

### LLM Architecture for Robotics

**LLM integration** requires specific architectural patterns:

```
┌─────────────────────────────────────────────────────────────┐
│              LLM-ROBOTICS ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  User        │                                           │
│  │  Interface   │  ← Voice, Text, GUI                      │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Speech-to-  │───►│     LLM      │───►│   Action     │  │
│  │  Text        │    │  (Language   │    │   Parser     │  │
│  │  (Whisper)   │    │   Model)     │    │              │  │
│  └──────────────┘    └──────┬───────┘    └──────┬───────┘  │
│                             │                   │           │
│                             │                   ▼           │
│                    ┌────────▼───────┐    ┌──────────────┐  │
│                    │  Context       │    │   ROS2       │  │
│                    │  Manager       │    │   Executor   │  │
│                    │  (Memory)      │    │              │  │
│                    └────────┬───────┘    └──────────────┘  │
│                             │                               │
│                    ┌────────▼───────┐                      │
│                    │  Perception    │                      │
│                    │  (Vision, etc) │                      │
│                    └────────────────┘                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Components:**

| Component | Purpose | Examples |
|-----------|---------|----------|
| **User Interface** | Human input channel | Microphone, keyboard, touchscreen |
| **Speech-to-Text** | Convert voice to text | Whisper, Google Speech API |
| **LLM** | Language understanding & planning | GPT-4, Llama 2, PaLM |
| **Action Parser** | Convert LLM output to commands | Custom ROS2 nodes |
| **Context Manager** | Maintain conversation & task state | Vector DB, Redis |
| **ROS2 Executor** | Execute robot actions | Nav2, MoveIt, custom nodes |
| **Perception** | Environment understanding | Cameras, LiDAR, depth sensors |

### Prompt Engineering for Robotics

**Effective prompts** are critical for reliable robot control:

```
┌─────────────────────────────────────────────────────────────┐
│              ROBOTICS PROMPT STRUCTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  System Prompt:                                              │
│  ──────────────                                              │
│  "You are a robotics assistant that converts natural         │
│   language into ROS2 action sequences. Always output         │
│   valid JSON with action names and parameters."              │
│                                                              │
│  Context:                                                    │
│  ─────────                                                   │
│  "Robot is a bipedal humanoid with 2 arms, 2 legs,          │
│   gripper hands. Current location: kitchen.                  │
│   Objects detected: red block, blue cup, table."             │
│                                                              │
│  User Instruction:                                           │
│  ──────────────────                                          │
│  "Pick up the red block and put it on the table"            │
│                                                              │
│  Expected Output Format:                                     │
│  ──────────────────────                                      │
│  {                                                           │
│    "actions": [                                              │
│      {"action": "navigate", "target": "red_block"},         │
│      {"action": "detect", "object": "red_block"},           │
│      {"action": "approach", "object": "red_block"},         │
│      {"action": "grasp", "gripper": "left"},                │
│      {"action": "navigate", "target": "table"},             │
│      {"action": "place", "location": "table"}               │
│    ]                                                         │
│  }                                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Best Practices:**

1. **Be Explicit**: Define exact output format
2. **Provide Context**: Include robot capabilities and environment
3. **Constrain Output**: Use JSON schemas, enums
4. **Include Safety**: Add collision avoidance constraints
5. **Handle Ambiguity**: Ask clarifying questions when needed

## Real Robotics Example

### Tesla Optimus with LLM Control

Tesla's **Optimus humanoid** uses LLM-like systems for task planning:

```
┌────────────────────────────────────────────────────────┐
│         TESLA OPTIMUS LANGUAGE-BASED CONTROL            │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Application: Factory Assembly                         │
│  ────────────────────────────                           │
│                                                         │
│  Human Instruction:                                     │
│  "Install the battery pack in the chassis"             │
│                                                         │
│  LLM Decomposition:                                     │
│  ─────────────────                                      │
│  1. Locate battery pack (vision)                       │
│  2. Navigate to battery location                       │
│  3. Grasp battery with both hands                      │
│  4. Navigate to chassis                                │
│  5. Align battery with mounting points                 │
│  6. Insert battery and secure                          │
│  7. Verify installation                                │
│                                                         │
│  Key Technologies:                                      │
│  ────────────────                                       │
│  • Vision-Language-Action models                       │
│  • Neural planning networks                            │
│  • End-to-end learning from demonstration              │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**Key Insights:**

- LLMs enable **zero-shot task learning** (no programming needed)
- **Natural language** is the new programming interface for robots
- **Multimodal models** (vision + language + action) are the future

## Architecture Overview

### Complete LLM-Robotics System

```
┌─────────────────────────────────────────────────────────────┐
│              COMPLETE LLM-ROBOTICS SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  Voice       │                                           │
│  │  Input       │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Whisper     │───►│  GPT-4/      │───►│  Action      │  │
│  │  (STT)       │    │  Llama       │    │  Parser      │  │
│  └──────────────┘    └──────┬───────┘    └──────┬───────┘  │
│                             │                   │           │
│                    ┌────────▼───────┐          │           │
│                    │  RAG Chatbot   │          │           │
│                    │  (Context)     │          │           │
│                    └────────┬───────┘          │           │
│                             │                   │           │
│                    ┌────────▼───────┐          ▼           │
│                    │  Perception    │    ┌──────────────┐  │
│                    │  (Vision)      │    │   ROS2       │  │
│                    │                │    │   Actions    │  │
│                    └────────────────┘    └──────────────┘  │
│                                                              │
│  ROS2 Topics:                                                │
│  • /voice_command      ← Transcribed speech                 │
│  • /llm_plan           ← Action sequence from LLM           │
│  • /parsed_actions     ← Parsed ROS2 commands               │
│  • /cmd_vel            ← Robot velocity                     │
│  • /joint_commands     ← Joint positions                    │
│  • /gripper_commands   ← Gripper control                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: LLM-ROS2 Bridge Setup

```python
#!/usr/bin/env python3
"""
LLM-ROS2 Bridge: Convert natural language to robot actions.
Module 4 - Chapter 1
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import openai
import json
import os


class LLMRobotBridge(Node):
    """Bridge LLM outputs to ROS2 actions."""
    
    def __init__(self):
        super().__init__('llm_robot_bridge')
        
        # Initialize OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Subscribers
        self.voice_sub = self.create_subscription(
            String,
            '/voice_command',
            self.voice_callback,
            10
        )
        
        # Publishers
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        # Action mapping
        self.action_map = {
            'move_forward': self.move_forward,
            'move_backward': self.move_backward,
            'turn_left': self.turn_left,
            'turn_right': self.turn_right,
            'stop': self.stop,
        }
        
        self.get_logger().info('LLM Robot Bridge started')
    
    def voice_callback(self, msg: String):
        """Process voice command."""
        voice_text = msg.data
        self.get_logger().info(f'Received voice command: {voice_text}')
        
        # Get action plan from LLM
        action_plan = self.get_llm_plan(voice_text)
        
        # Execute actions
        if action_plan:
            self.execute_plan(action_plan)
    
    def get_llm_plan(self, instruction: str) -> dict:
        """Get action plan from LLM."""
        system_prompt = """You are a robotics assistant. Convert natural language 
        instructions into a sequence of robot actions. Output valid JSON only.
        
        Available actions:
        - move_forward: Move forward (params: distance_meters)
        - move_backward: Move backward (params: distance_meters)
        - turn_left: Turn left (params: angle_degrees)
        - turn_right: Turn right (params: angle_degrees)
        - stop: Stop all motion (params: none)
        
        Example output:
        {
            "actions": [
                {"action": "move_forward", "params": {"distance_meters": 1.0}},
                {"action": "turn_right", "params": {"angle_degrees": 90}},
                {"action": "move_forward", "params": {"distance_meters": 0.5}}
            ]
        }"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": instruction}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            plan_text = response.choices[0].message.content
            plan = json.loads(plan_text)
            
            self.get_logger().info(f'LLM Plan: {plan}')
            return plan
            
        except Exception as e:
            self.get_logger().error(f'LLM error: {e}')
            return None
    
    def execute_plan(self, plan: dict):
        """Execute action plan."""
        actions = plan.get('actions', [])
        
        for action_item in actions:
            action_name = action_item.get('action')
            params = action_item.get('params', {})
            
            if action_name in self.action_map:
                self.get_logger().info(f'Executing: {action_name} with {params}')
                self.action_map[action_name](**params)
    
    def move_forward(self, distance_meters: float):
        """Move robot forward."""
        cmd = Twist()
        cmd.linear.x = 0.3  # m/s
        duration = distance_meters / cmd.linear.x
        
        self.cmd_pub.publish(cmd)
        rclpy.sleep_once(duration=duration)
        self.stop()
    
    def move_backward(self, distance_meters: float):
        """Move robot backward."""
        cmd = Twist()
        cmd.linear.x = -0.3
        duration = distance_meters / abs(cmd.linear.x)
        
        self.cmd_pub.publish(cmd)
        rclpy.sleep_once(duration=duration)
        self.stop()
    
    def turn_left(self, angle_degrees: float):
        """Turn robot left."""
        cmd = Twist()
        cmd.angular.z = 0.5  # rad/s
        angle_rad = angle_degrees * 3.14159 / 180.0
        duration = angle_rad / cmd.angular.z
        
        self.cmd_pub.publish(cmd)
        rclpy.sleep_once(duration=duration)
        self.stop()
    
    def turn_right(self, angle_degrees: float):
        """Turn robot right."""
        cmd = Twist()
        cmd.angular.z = -0.5
        angle_rad = angle_degrees * 3.14159 / 180.0
        duration = angle_rad / abs(cmd.angular.z)
        
        self.cmd_pub.publish(cmd)
        rclpy.sleep_once(duration=duration)
        self.stop()
    
    def stop(self):
        """Stop robot."""
        cmd = Twist()
        self.cmd_pub.publish(cmd)


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    bridge = LLMRobotBridge()
    
    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        bridge.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 2: Prompt Template for Robotics

```python
#!/usr/bin/env python3
"""
Prompt templates for LLM-based robot control.
"""

from typing import List, Dict
import json


class RoboticsPromptBuilder:
    """Build prompts for robotics LLM applications."""
    
    def __init__(self, robot_type: str = "humanoid"):
        self.robot_type = robot_type
        self.system_prompts = {
            "humanoid": self._humanoid_system_prompt(),
            "mobile_base": self._mobile_base_system_prompt(),
            "manipulator": self._manipulator_system_prompt(),
        }
    
    def _humanoid_system_prompt(self) -> str:
        """System prompt for humanoid robot."""
        return """You are an AI assistant controlling a bipedal humanoid robot.
        
Robot Capabilities:
- Walk forward/backward
- Turn left/right
- Pick up objects with left/right hand
- Place objects on surfaces
- Navigate to locations
- Detect objects by color and shape

Safety Constraints:
- Never move faster than 0.5 m/s
- Always avoid collisions
- Ask for clarification if instruction is ambiguous
- Stop if obstacle detected

Output Format:
Always output valid JSON with this structure:
{
    "understanding": "Brief summary of what you understood",
    "actions": [
        {"action": "action_name", "params": {"param1": value1}}
    ],
    "clarification_needed": false
}"""
    
    def _mobile_base_system_prompt(self) -> str:
        """System prompt for mobile base robot."""
        return """You are an AI assistant controlling a mobile robot base.
        
Robot Capabilities:
- Move forward/backward
- Rotate in place
- Navigate to coordinates
- Avoid obstacles

Output Format:
{
    "actions": [
        {"action": "navigate", "params": {"x": 1.0, "y": 2.0}}
    ]
}"""
    
    def _manipulator_system_prompt(self) -> str:
        """System prompt for robot arm."""
        return """You are an AI assistant controlling a robot arm.
        
Robot Capabilities:
- Move end-effector to XYZ coordinates
- Open/close gripper
- Pick and place objects

Output Format:
{
    "actions": [
        {"action": "move_to", "params": {"x": 0.5, "y": 0.0, "z": 0.3}},
        {"action": "grasp", "params": {}}
    ]
}"""
    
    def build_prompt(self, instruction: str, context: Dict = None) -> List[Dict]:
        """Build complete prompt for LLM."""
        system_prompt = self.system_prompts.get(
            self.robot_type, 
            self._humanoid_system_prompt()
        )
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add context if provided
        if context:
            context_str = json.dumps(context, indent=2)
            messages.append(
                {"role": "system", "content": f"Current context:\n{context_str}"}
            )
        
        # Add user instruction
        messages.append(
            {"role": "user", "content": instruction}
        )
        
        return messages


# Example usage
if __name__ == '__main__':
    builder = RoboticsPromptBuilder(robot_type="humanoid")
    
    instruction = "Pick up the red block and put it on the table"
    
    context = {
        "robot_location": "kitchen",
        "detected_objects": ["red block", "blue cup", "table"],
        "battery_level": 85
    }
    
    messages = builder.build_prompt(instruction, context)
    
    print("Prompt Messages:")
    for msg in messages:
        print(f"\n{msg['role'].upper()}:")
        print(msg['content'][:200] + "...")
```

### Example 3: LLM Action Parser

```python
#!/usr/bin/env python3
"""
Parse LLM output into executable ROS2 actions.
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class RobotAction:
    """Represents a robot action."""
    name: str
    params: Dict[str, Any]
    preconditions: List[str]
    postconditions: List[str]


class LLMActionParser:
    """Parse LLM output into robot actions."""
    
    def __init__(self):
        self.action_schemas = {
            "navigate": {
                "required_params": ["target"],
                "optional_params": ["speed", "timeout"],
                "defaults": {"speed": 0.3, "timeout": 30.0}
            },
            "grasp": {
                "required_params": ["object"],
                "optional_params": ["gripper", "force"],
                "defaults": {"gripper": "left", "force": 50}
            },
            "place": {
                "required_params": ["location"],
                "optional_params": ["orientation"],
                "defaults": {"orientation": "top"}
            },
            "detect": {
                "required_params": ["object_type"],
                "optional_params": ["color", "size"],
                "defaults": {}
            }
        }
    
    def parse(self, llm_output: str) -> List[RobotAction]:
        """Parse LLM output into actions."""
        try:
            # Parse JSON
            plan = json.loads(llm_output)
            
            # Extract actions
            actions_data = plan.get('actions', [])
            
            # Validate and convert
            actions = []
            for action_data in actions_data:
                action = self._validate_action(action_data)
                if action:
                    actions.append(action)
            
            return actions
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from LLM: {e}")
    
    def _validate_action(self, action_data: Dict) -> RobotAction:
        """Validate action against schema."""
        action_name = action_data.get('action')
        params = action_data.get('params', {})
        
        # Check if action exists
        if action_name not in self.action_schemas:
            raise ValueError(f"Unknown action: {action_name}")
        
        schema = self.action_schemas[action_name]
        
        # Check required params
        for req_param in schema['required_params']:
            if req_param not in params:
                raise ValueError(
                    f"Missing required parameter '{req_param}' for action '{action_name}'"
                )
        
        # Apply defaults
        for opt_param, default_value in schema['optional_params'].items():
            if opt_param not in params:
                params[opt_param] = default_value
        
        # Create action
        return RobotAction(
            name=action_name,
            params=params,
            preconditions=action_data.get('preconditions', []),
            postconditions=action_data.get('postconditions', [])
        )


# Example usage
if __name__ == '__main__':
    parser = LLMActionParser()
    
    llm_output = """
    {
        "actions": [
            {
                "action": "navigate",
                "params": {"target": "red_block"}
            },
            {
                "action": "grasp",
                "params": {"object": "red_block", "gripper": "left"}
            },
            {
                "action": "navigate",
                "params": {"target": "table"}
            },
            {
                "action": "place",
                "params": {"location": "table"}
            }
        ]
    }
    """
    
    actions = parser.parse(llm_output)
    
    print("Parsed Actions:")
    for i, action in enumerate(actions):
        print(f"\n{i+1}. {action.name}")
        print(f"   Params: {action.params}")
        print(f"   Preconditions: {action.preconditions}")
        print(f"   Postconditions: {action.postconditions}")
```

## Hands-on Lab

### Lab 1.1: LLM-ROS2 Integration

**Objective**: Connect an LLM (GPT-4) to ROS2 for natural language robot control.

**Prerequisites**:
- Python 3.10+
- ROS2 Humble
- OpenAI API key
- Basic Python and ROS2 knowledge

**Duration**: 90 minutes

---

#### Step 1: Install Dependencies

```bash
# Install OpenAI Python SDK
pip3 install openai

# Install ROS2 packages
sudo apt install ros-humble-geometry-msgs ros-humble-std-msgs

# Set OpenAI API key
export OPENAI_API_KEY='sk-your-api-key-here'
```

#### Step 2: Create LLM Bridge Node

Create `llm_robot_bridge.py`:

```python
# Copy Example 1 from above
```

#### Step 3: Create Prompt Builder

Create `prompt_builder.py`:

```python
# Copy Example 2 from above
```

#### Step 4: Create Action Parser

Create `action_parser.py`:

```python
# Copy Example 3 from above
```

#### Step 5: Test with Simulated Robot

```bash
# Start simulation
gz sim empty_world.sdf

# Start LLM bridge
python3 llm_robot_bridge.py

# Send voice command (in another terminal)
ros2 topic pub /voice_command std_msgs/msg/String "{data: 'move forward 1 meter'}"
```

#### Step 6: Verify Actions

```bash
# Monitor robot commands
ros2 topic echo /cmd_vel

# Check LLM logs
# Should see parsed actions and executed commands
```

**Expected Result**:

LLM parses natural language instruction, generates action sequence, robot executes commands.

## Summary

### Key Takeaways

1. **LLMs** serve as the cognitive brain for robots, translating language to actions

2. **Prompt Engineering** is critical for reliable robot control

3. **Action Parsing** converts LLM output to executable ROS2 commands

4. **Safety Constraints** must be built into the LLM system

5. **Context Management** enables multi-turn conversations and task continuity

### Key Terms

| Term | Definition |
|------|------------|
| **LLM** | Large Language Model (GPT-4, Llama, etc.) |
| **Prompt Engineering** | Designing effective prompts for LLMs |
| **Action Parser** | Converts LLM output to robot commands |
| **VLA** | Vision-Language-Action models |
| **Zero-Shot Learning** | Performing tasks without explicit training |

## Exercises

### Exercise 1.1: Prompt Design

1. Create prompts for 5 different robot tasks
2. **Test** with GPT-4
3. **Analyze** output quality
4. **Refine** prompts for consistency

### Exercise 1.2: Action Schema Extension

1. Add 3 new action types to the parser
2. **Define** parameters and constraints
3. **Test** with LLM output
4. **Validate** parsing accuracy

### Exercise 1.3: Context Management

1. Implement conversation history
2. **Add** context to prompts
3. **Test** multi-turn dialog
4. **Evaluate** context relevance

### Exercise 1.4: Error Handling

1. Add error detection for invalid LLM output
2. **Implement** retry logic
3. **Add** clarification questions
4. **Test** with ambiguous instructions

### Exercise 1.5: Research Assignment

Research **LLM applications in robotics**:

- Google RT-2
- Tesla Optimus
- Figure 01
- MIT's Code as Policies

**Write** a 500-word summary comparing 2 approaches.

---

**Next Chapter**: [Chapter 2 — Voice-to-Action Commands →](./chapter2-voice-to-action.md)
