---
sidebar_label: '3. Cognitive Planning'
---

# Chapter 3: Cognitive Planning with LLMs

## Learning Objectives

By the end of this chapter, you will be able to:

- Convert natural language instructions into ROS2 action sequences
- Understand task decomposition for complex robot behaviors
- Integrate perception and planning with LLMs
- Implement cognitive architectures for robot decision-making
- Handle multi-step tasks with error recovery

## Concept Explanation

### What is Cognitive Planning?

**Cognitive planning** is the process of converting high-level instructions into executable action sequences:

```
┌─────────────────────────────────────────────────────────────┐
│                  COGNITIVE PLANNING                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  High-Level Instruction                                      │
│  ──────────────────────                                      │
│  "Clean the table"                                           │
│                                                              │
│         ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LLM Planner                              │   │
│  │                                                       │   │
│  │  1. Understand goal: table should be clean           │   │
│  │  2. Identify objects: cup, plate, crumbs             │   │
│  │  3. Generate plan:                                    │   │
│  │     - Navigate to table                              │   │
│  │     - Detect objects                                 │   │
│  │     - Pick up cup                                    │   │
│  │     - Place in sink                                  │   │
│  │     - Pick up plate                                  │   │
│  │     - Place in dishwasher                            │   │
│  │     - Wipe crumbs                                    │   │
│  └──────────────────────────────────────────────────────┘   │
│         ↓                                                    │
│  Low-Level Actions                                           │
│  ───────────────                                             │
│  /cmd_vel, /arm_joint_cmd, /gripper_cmd                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Capabilities:**

1. **Goal Understanding**: Interpret what the user wants
2. **Task Decomposition**: Break into executable steps
3. **Resource Allocation**: Assign actions to robot capabilities
4. **Temporal Reasoning**: Order actions correctly
5. **Error Recovery**: Handle failures and replan

### Task Decomposition

**Complex tasks** are decomposed into primitive actions:

```
┌─────────────────────────────────────────────────────────────┐
│              TASK DECOMPOSITION HIERARCHY                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Level 1: Abstract Goal                                     │
│  ─────────────────────                                      │
│  "Serve drinks to guests"                                   │
│                                                              │
│         ↓分解                                                 │
│  Level 2: Sub-tasks                                         │
│  ─────────────────                                          │
│  • Locate drinks                                             │
│  • Pick up drinks                                            │
│  • Find guests                                               │
│  • Serve each guest                                          │
│                                                              │
│         ↓分解                                                 │
│  Level 3: Primitive Actions                                  │
│  ────────────────────                                        │
│  • Navigate to kitchen                                       │
│  • Detect refrigerator                                       │
│  • Open refrigerator                                         │
│  • Grasp drink can                                           │
│  • Close refrigerator                                        │
│  • Navigate to living room                                   │
│  • Detect person 1                                           │
│  • Offer drink                                               │
│  • ...                                                       │
│                                                              │
│         ↓分解                                                 │
│  Level 4: Motor Commands                                     │
│  ──────────────────                                          │
│  • /cmd_vel: (0.3, 0.0)                                     │
│  • /arm_joint: [0.5, -0.3, 0.8, ...]                        │
│  • /gripper: close                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### LLM as Cognitive Planner

**LLMs excel** at planning due to their world knowledge:

```
┌─────────────────────────────────────────────────────────────┐
│                  LLM PLANNING PROCESS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Input:                                                      │
│  ─────                                                       │
│  Instruction: "Make me a coffee"                            │
│  Context: Robot in kitchen, coffee machine detected         │
│  Capabilities: Navigate, grasp, pour, operate appliances    │
│                                                              │
│         ↓                                                    │
│  LLM Reasoning:                                              │
│  ────────────                                                │
│  1. Parse instruction                                        │
│  2. Retrieve relevant knowledge                              │
│  3. Consider constraints                                     │
│  4. Generate action sequence                                 │
│  5. Validate feasibility                                     │
│                                                              │
│         ↓                                                    │
│  Output:                                                     │
│  ──────                                                      │
│  Plan: [                                                     │
│    {action: navigate, target: coffee_machine},              │
│    {action: grasp, object: coffee_pod},                     │
│    {action: insert, object: coffee_pod, into: machine},     │
│    {action: press_button, button: start},                   │
│    {action: grasp, object: mug},                            │
│    {action: place_under, object: mug, under: spout},        │
│    {action: wait, duration: 30},                            │
│    {action: serve, target: user}                            │
│  ]                                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### Figure 01 Humanoid with LLM Planning

**Figure 01** uses LLMs for task planning in factory settings:

```
┌────────────────────────────────────────────────────────┐
│         FIGURE 01 LLM-BASED PLANNING                    │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Application: Factory Material Handling                │
│  ─────────────────────────────────                      │
│                                                         │
│  Human Instruction:                                     │
│  "Move these boxes to the shipping area"               │
│                                                         │
│  LLM Planning Process:                                  │
│  ────────────────────                                   │
│  1. Identify boxes (perception)                        │
│  2. Determine shipping area location                   │
│  3. Plan pick sequence (largest first)                 │
│  4. Generate navigation path                           │
│  5. Execute pick-and-place for each box                │
│  6. Verify completion                                  │
│                                                         │
│  Key Technologies:                                      │
│  ────────────────                                       │
│  • Vision-Language-Action models                       │
│  • Hierarchical task networks                          │
│  • Real-time replanning                                │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete Cognitive Planning System

```
┌─────────────────────────────────────────────────────────────┐
│              COGNITIVE PLANNING SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  User        │                                           │
│  │  Instruction │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  LLM         │───►│  Task        │───►│  Action      │  │
│  │  Planner     │    │  Decomposer  │    │  Executor    │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │           │
│         │          ┌────────▼───────┐          │           │
│         │          │  Perception    │          │           │
│         │          │  (Object Det)  │          │           │
│         │          └────────┬───────┘          │           │
│         │                   │                   │           │
│         │          ┌────────▼───────┐          │           │
│         └─────────►│  World Model   │◄─────────┘           │
│                    │  (State)       │                      │
│                    └────────────────┘                      │
│                                                              │
│  Feedback Loop:                                              │
│  ─────────────                                               │
│  • Monitor execution                                         │
│  • Detect failures                                           │
│  • Trigger replanning                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: LLM Task Planner

```python
#!/usr/bin/env python3
"""
LLM-based task planner for robot actions.
Module 4 - Chapter 3
"""

import openai
import json
import os
from typing import List, Dict


class LLMTaskPlanner:
    """Plan robot tasks using LLM."""
    
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        self.system_prompt = """You are a robotics task planner. 
        Convert high-level instructions into sequences of robot actions.
        
        Available primitive actions:
        - navigate(target): Move to target location
        - detect(object_type): Search for object
        - approach(object): Move close to object
        - grasp(object): Pick up object
        - place(location): Put object at location
        - open(container): Open container
        - close(container): Close container
        - press(button): Press button
        - wait(duration): Wait for duration seconds
        - serve(target): Serve item to target
        
        Output format (JSON):
        {
            "goal": "Brief goal description",
            "steps": [
                {"action": "action_name", "params": {"param": "value"}},
                ...
            ],
            "estimated_duration": 30.0
        }"""
    
    def plan(self, instruction: str, context: Dict = None) -> Dict:
        """Generate plan from instruction."""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add context
        if context:
            context_str = json.dumps(context, indent=2)
            messages.append(
                {"role": "system", "content": f"Context:\n{context_str}"}
            )
        
        # Add instruction
        messages.append(
            {"role": "user", "content": instruction}
        )
        
        # Get LLM response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.3,
            max_tokens=1000
        )
        
        plan_text = response.choices[0].message.content
        
        # Parse JSON
        try:
            plan = json.loads(plan_text)
            return plan
        except json.JSONDecodeError:
            return {"error": "Failed to parse plan", "raw": plan_text}


# Example usage
if __name__ == '__main__':
    planner = LLMTaskPlanner()
    
    instruction = "Make me a coffee"
    
    context = {
        "robot_location": "kitchen",
        "detected_objects": [
            "coffee_machine", "coffee_pods", "mug", "sink"
        ],
        "robot_capabilities": [
            "navigate", "grasp", "place", "press"
        ]
    }
    
    plan = planner.plan(instruction, context)
    
    print("Generated Plan:")
    print(json.dumps(plan, indent=2))
```

### Example 2: Plan Executor

```python
#!/usr/bin/env python3
"""
Execute planned actions on robot.
"""

import rclpy
from rclpy.node import Node
from typing import List, Dict, Any
import time


class PlanExecutor(Node):
    """Execute planned action sequences."""
    
    def __init__(self):
        super().__init__('plan_executor')
        
        # Action handlers
        self.action_handlers = {
            'navigate': self.execute_navigate,
            'detect': self.execute_detect,
            'approach': self.execute_approach,
            'grasp': self.execute_grasp,
            'place': self.execute_place,
            'open': self.execute_open,
            'close': self.execute_close,
            'press': self.execute_press,
            'wait': self.execute_wait,
            'serve': self.execute_serve,
        }
        
        # Execution state
        self.current_step = 0
        self.plan = None
        self.success = False
    
    def execute_plan(self, plan: Dict) -> bool:
        """Execute complete plan."""
        self.plan = plan
        steps = plan.get('steps', [])
        
        self.get_logger().info(f'Executing plan: {plan.get("goal")}')
        self.get_logger().info(f'Total steps: {len(steps)}')
        
        for i, step in enumerate(steps):
            self.current_step = i
            action_name = step.get('action')
            params = step.get('params', {})
            
            self.get_logger().info(
                f'Step {i+1}/{len(steps)}: {action_name}({params})'
            )
            
            # Execute action
            if action_name in self.action_handlers:
                success = self.action_handlers[action_name](**params)
                
                if not success:
                    self.get_logger().error(
                        f'Action {action_name} failed at step {i+1}'
                    )
                    
                    # Try recovery
                    if not self.execute_recovery(action_name, params):
                        return False
            else:
                self.get_logger().error(f'Unknown action: {action_name}')
                return False
        
        self.get_logger().info('Plan execution completed successfully')
        return True
    
    def execute_navigate(self, target: str) -> bool:
        """Execute navigate action."""
        self.get_logger().info(f'Navigating to {target}')
        # Publish to /cmd_vel or Nav2
        time.sleep(2.0)  # Simulate navigation
        return True
    
    def execute_detect(self, object_type: str) -> bool:
        """Execute detect action."""
        self.get_logger().info(f'Detecting {object_type}')
        # Run object detection
        time.sleep(1.0)  # Simulate detection
        return True
    
    def execute_approach(self, object: str) -> bool:
        """Execute approach action."""
        self.get_logger().info(f'Approaching {object}')
        # Move close to object
        time.sleep(1.5)
        return True
    
    def execute_grasp(self, object: str) -> bool:
        """Execute grasp action."""
        self.get_logger().info(f'Grasping {object}')
        # Control gripper
        time.sleep(1.0)
        return True
    
    def execute_place(self, location: str) -> bool:
        """Execute place action."""
        self.get_logger().info(f'Placing at {location}')
        # Move and release
        time.sleep(1.5)
        return True
    
    def execute_open(self, container: str) -> bool:
        """Execute open action."""
        self.get_logger().info(f'Opening {container}')
        # Open container
        time.sleep(1.0)
        return True
    
    def execute_close(self, container: str) -> bool:
        """Execute close action."""
        self.get_logger().info(f'Closing {container}')
        # Close container
        time.sleep(1.0)
        return True
    
    def execute_press(self, button: str) -> bool:
        """Execute press action."""
        self.get_logger().info(f'Pressing {button}')
        # Press button
        time.sleep(0.5)
        return True
    
    def execute_wait(self, duration: float) -> bool:
        """Execute wait action."""
        self.get_logger().info(f'Waiting for {duration} seconds')
        time.sleep(duration)
        return True
    
    def execute_serve(self, target: str) -> bool:
        """Execute serve action."""
        self.get_logger().info(f'Serving to {target}')
        # Move to target and present
        time.sleep(2.0)
        return True
    
    def execute_recovery(self, failed_action: str, params: Dict) -> bool:
        """Attempt recovery from failed action."""
        self.get_logger().warn(f'Attempting recovery for {failed_action}')
        
        # Simple recovery: retry once
        if failed_action in self.action_handlers:
            self.get_logger().info('Retrying action...')
            time.sleep(0.5)
            return self.action_handlers[failed_action](**params)
        
        return False


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    executor = PlanExecutor()
    
    # Example plan
    plan = {
        "goal": "Make coffee",
        "steps": [
            {"action": "navigate", "params": {"target": "coffee_machine"}},
            {"action": "grasp", "params": {"object": "coffee_pod"}},
            {"action": "open", "params": {"container": "coffee_machine"}},
            {"action": "place", "params": {"location": "coffee_machine"}},
            {"action": "close", "params": {"container": "coffee_machine"}},
            {"action": "press", "params": {"button": "start"}},
            {"action": "wait", "params": {"duration": 30.0}},
            {"action": "serve", "params": {"target": "user"}},
        ]
    }
    
    success = executor.execute_plan(plan)
    
    if success:
        executor.get_logger().info('Plan completed!')
    else:
        executor.get_logger().error('Plan failed!')
    
    executor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 3: Cognitive Architecture

```python
#!/usr/bin/env python3
"""
Cognitive architecture for robot decision-making.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import time


@dataclass
class Belief:
    """Represents robot's belief about the world."""
    fact: str
    confidence: float
    timestamp: float


@dataclass
class Goal:
    """Represents a goal."""
    description: str
    priority: int
    achieved: bool = False


class CognitiveArchitecture:
    """Cognitive architecture for robot."""
    
    def __init__(self):
        # Belief base
        self.beliefs: List[Belief] = []
        
        # Current goals
        self.goals: List[Goal] = []
        
        # Current plan
        self.current_plan: Optional[Dict] = None
        
        # Execution state
        self.executing = False
    
    def add_belief(self, fact: str, confidence: float = 1.0):
        """Add new belief."""
        belief = Belief(
            fact=fact,
            confidence=confidence,
            timestamp=time.time()
        )
        self.beliefs.append(belief)
    
    def add_goal(self, description: str, priority: int = 5):
        """Add new goal."""
        goal = Goal(
            description=description,
            priority=priority
        )
        self.goals.append(goal)
    
    def get_context(self) -> Dict:
        """Get current context for LLM."""
        return {
            "beliefs": [b.fact for b in self.beliefs[-10:]],  # Last 10 beliefs
            "goals": [g.description for g in self.goals if not g.achieved],
            "executing": self.executing,
            "has_plan": self.current_plan is not None
        }
    
    def update_from_perception(self, perception_data: Dict):
        """Update beliefs from perception."""
        # Example: object detection
        if 'objects' in perception_data:
            for obj in perception_data['objects']:
                self.add_belief(f"Detected {obj['type']} at {obj['location']}")
        
        # Example: robot state
        if 'battery' in perception_data:
            self.add_belief(f"Battery level: {perception_data['battery']}%")
    
    def select_next_goal(self) -> Optional[Goal]:
        """Select highest priority unachieved goal."""
        unachieved = [g for g in self.goals if not g.achieved]
        
        if not unachieved:
            return None
        
        # Sort by priority
        unachieved.sort(key=lambda g: g.priority, reverse=True)
        
        return unachieved[0]
    
    def mark_goal_achieved(self, goal_description: str):
        """Mark goal as achieved."""
        for goal in self.goals:
            if goal.description == goal_description:
                goal.achieved = True
                break


# Example usage
if __name__ == '__main__':
    cognitive = CognitiveArchitecture()
    
    # Add initial beliefs
    cognitive.add_belief("Robot is in kitchen", 1.0)
    cognitive.add_belief("Coffee machine is operational", 0.9)
    
    # Add goal
    cognitive.add_goal("Make coffee for user", priority=8)
    
    # Get context for LLM
    context = cognitive.get_context()
    
    print("Cognitive State:")
    print(f"Beliefs: {context['beliefs']}")
    print(f"Goals: {context['goals']}")
    print(f"Executing: {context['executing']}")
```

## Hands-on Lab

### Lab 3.1: Cognitive Planning Implementation

**Objective**: Implement LLM-based cognitive planning for a robot.

**Prerequisites**:
- Python 3.10+
- ROS2 Humble
- OpenAI API key
- Chapter 1 & 2 completed

**Duration**: 120 minutes

---

#### Step 1: Create Task Planner

Create `task_planner.py`:

```python
# Copy Example 1 from above
```

#### Step 2: Create Plan Executor

Create `plan_executor.py`:

```python
# Copy Example 2 from above
```

#### Step 3: Create Cognitive Architecture

Create `cognitive_arch.py`:

```python
# Copy Example 3 from above
```

#### Step 4: Integration Test

```bash
# Start simulation
gz sim kitchen_world.sdf

# Run cognitive architecture
python3 cognitive_arch.py

# Send high-level instruction
python3 send_instruction.py "Clean up the kitchen"
```

#### Step 5: Monitor Execution

```bash
# View plan
ros2 topic echo /current_plan

# View execution status
ros2 topic echo /execution_status

# View robot commands
ros2 topic echo /cmd_vel
```

**Expected Result**:

Robot receives high-level instruction, generates plan, executes actions, achieves goal.

## Summary

### Key Takeaways

1. **Cognitive Planning** converts high-level goals into executable actions

2. **LLMs** provide world knowledge for task decomposition

3. **Plan Execution** requires monitoring and error recovery

4. **Cognitive Architecture** maintains beliefs, goals, and plans

5. **Feedback Loops** enable adaptive behavior

### Key Terms

| Term | Definition |
|------|------------|
| **Task Decomposition** | Breaking complex tasks into steps |
| **Cognitive Architecture** | System for belief/goal/plan management |
| **Plan Executor** | Component that runs action sequences |
| **Recovery** | Handling execution failures |
| **World Model** | Robot's representation of environment |

## Exercises

### Exercise 3.1: Plan Optimization

1. Generate plans for 10 different tasks
2. **Analyze** plan efficiency
3. **Optimize** prompt for shorter plans
4. **Compare** before/after

### Exercise 3.2: Error Recovery

1. Simulate action failures
2. **Implement** recovery strategies
3. **Test** replanning
4. **Measure** success rate

### Exercise 3.3: Multi-Goal Planning

1. Add multiple simultaneous goals
2. **Implement** goal prioritization
3. **Test** interleaved execution
4. **Evaluate** efficiency

### Exercise 3.4: Learning from Feedback

1. Add human feedback mechanism
2. **Implement** plan refinement
3. **Test** improvement over time
4. **Document** learning process

### Exercise 3.5: Research Assignment

Research **cognitive architectures for robotics**:

- SOAR
- ACT-R
- ICARUS
- LLM-based approaches

**Write** a 600-word summary comparing 2 architectures.

---

**Next Chapter**: [Chapter 4 — Multimodal Interaction →](./chapter4-multimodal-interaction.md)
