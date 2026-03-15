---
sidebar_label: '5. Robot Nervous System'
---

# Chapter 5: Robot Nervous System

## Building the Complete System

This chapter integrates all previous concepts into a complete robotic nervous system architecture.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROBOT NERVOUS SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │  SENSORS     │────▶│   BRAIN      │────▶│   ACTUATORS  │    │
│  │  (Input)     │     │  (Process)   │     │  (Output)    │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │ - Camera     │     │ - AI Agent   │     │ - Motors     │    │
│  │ - IMU        │     │ - Planning   │     │ - Servos     │    │
│  │ - LiDAR      │     │ - Decision   │     │ - Grippers   │    │
│  │ - Force      │     │ - Learning   │     │ - LEDs       │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Complete Integration Example

### Main System Node

```python
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String, Float64, Bool
from sensor_msgs.msg import JointState
import numpy as np

class RobotNervousSystem(Node):
    def __init__(self):
        super().__init__('robot_nervous_system')
        
        # === SENSORY LAYER ===
        # Proprioceptive sensors (body awareness)
        self.joint_state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10)
        
        # Exteroceptive sensors (environment)
        self.collision_sub = self.create_subscription(
            Bool,
            'collision_detected',
            self.collision_callback,
            10)
        
        # === CENTRAL PROCESSING ===
        self.brain_state = 'IDLE'
        self.current_action = None
        self.emergency_stop = False
        
        # === MOTOR LAYER ===
        self.motor_command_pub = self.create_publisher(
            JointState,
            'motor_commands',
            10)
        
        self.status_pub = self.create_publisher(
            String,
            'system_status',
            10)
        
        # Control loop timer
        timer_period = 0.01  # 100 Hz
        self.timer = self.create_timer(timer_period, self.control_loop)
        
        self.get_logger().info('Robot Nervous System initialized')
    
    def joint_state_callback(self, msg):
        """Process proprioceptive feedback"""
        # Update internal state based on joint positions
        self.current_joint_positions = msg.position
        self.current_joint_velocities = msg.velocity
    
    def collision_callback(self, msg):
        """Process emergency signals"""
        if msg.data:
            self.emergency_stop = True
            self.brain_state = 'EMERGENCY'
            self.get_logger().warn('COLLISION DETECTED!')
    
    def control_loop(self):
        """Main control loop - the 'spinal cord'"""
        if self.emergency_stop:
            self.execute_emergency_stop()
            return
        
        # Perception -> Decision -> Action cycle
        sensory_data = self.gather_sensory_data()
        decision = self.brain_process(sensory_data)
        self.execute_action(decision)
    
    def gather_sensory_data(self):
        """Collect all sensory inputs"""
        return {
            'joints': getattr(self, 'current_joint_positions', None),
            'emergency': self.emergency_stop,
            'timestamp': self.get_clock().now().to_msg()
        }
    
    def brain_process(self, sensory_data):
        """Central processing - AI decision making"""
        # This is where your AI agent logic goes
        if sensory_data['joints'] is None:
            return {'action': 'WAIT', 'reason': 'No sensor data'}
        
        # Example: Simple reflex behavior
        # In practice, this would be your AI model
        return {
            'action': 'MOVE',
            'target_positions': self.generate_movement_pattern()
        }
    
    def generate_movement_pattern(self):
        """Generate coordinated movement"""
        # Example: Simple walking pattern
        return [0.1, 0.2, -0.1, -0.2, 0.0, 0.0]
    
    def execute_action(self, decision):
        """Execute decided action"""
        if decision['action'] == 'MOVE':
            msg = JointState()
            msg.position = decision['target_positions']
            msg.velocity = [0.5] * len(decision['target_positions'])
            msg.effort = [10.0] * len(decision['target_positions'])
            self.motor_command_pub.publish(msg)
        
        # Publish status
        status_msg = String()
        status_msg.data = f"State: {self.brain_state}, Action: {decision['action']}"
        self.status_pub.publish(status_msg)
    
    def execute_emergency_stop(self):
        """Emergency stop - highest priority"""
        msg = JointState()
        # Zero all commands
        msg.position = [0.0] * 6
        msg.velocity = [0.0] * 6
        msg.effort = [0.0] * 6
        self.motor_command_pub.publish(msg)
        
        status_msg = String()
        status_msg.data = "EMERGENCY STOP ACTIVE"
        self.status_pub.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    
    # Create the nervous system node
    nervous_system = RobotNervousSystem()
    
    # Use multi-threaded executor for parallel processing
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(nervous_system)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        nervous_system.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Launch File for Complete System

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        # Robot State Publisher (URDF)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('my_robot'),
                '/launch/display.launch.py'
            ])
        ),
        
        # Nervous System (Main AI Controller)
        Node(
            package='my_robot',
            executable='robot_nervous_system',
            name='robot_nervous_system',
            output='screen'
        ),
        
        # Sensor Fusion Node
        Node(
            package='my_robot',
            executable='sensor_fusion',
            name='sensor_fusion',
            output='screen'
        ),
        
        # Motor Controller
        Node(
            package='my_robot',
            executable='motor_controller',
            name='motor_controller',
            output='screen'
        ),
    ])
```

## Testing the System

```bash
# Build the workspace
cd ~/ros2_ws
colcon build --packages-select my_robot
source install/setup.bash

# Launch the complete system
ros2 launch my_robot nervous_system.launch.py

# Monitor system status in another terminal
ros2 topic echo /system_status

# Send test commands
ros2 topic pub /collision_detected std_msgs/msg/Bool "{data: true}"
```

## Summary

You've now built a complete robot nervous system with:

1. ✅ **Sensory Layer** - Processing sensor inputs
2. ✅ **Central Processing** - AI decision making
3. ✅ **Motor Layer** - Executing actions
4. ✅ **Emergency Systems** - Safety reflexes
5. ✅ **Integration** - All components working together

## Next Steps

- Add machine learning models for intelligent behavior
- Implement more sophisticated movement patterns
- Add vision processing for environment understanding
- Create learning algorithms for adaptation
