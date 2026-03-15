# Module 2 Code Examples

This directory contains executable code examples for all chapters in Module 2: The Digital Twin (Gazebo & Unity).

## Directory Structure

```
code/
├── chapter1/          # Introduction to Robot Simulation
│   ├── install_gazebo.sh
│   ├── install_unity.md
│   ├── simple_world.sdf
│   └── launch_simulation.py
├── chapter2/          # Gazebo Simulation Environment
│   ├── simple_robot.urdf
│   ├── gazebo_world.sdf
│   ├── gazebo_launch.py
│   └── simple_controller.py
├── chapter3/          # Physics and Sensors
│   ├── biped_humanoid.urdf
│   ├── walking_controller.py
│   ├── sensor_fusion.py
│   ├── record_data.py
│   └── analyze_data.py
├── chapter4/          # Unity Robot Visualization
│   ├── RobotController.cs
│   ├── CameraController.cs
│   ├── LidarVisualizer.cs
│   ├── unity_streamer.py
│   └── ROS_BRIDGE_SETUP.md
└── chapter5/          # Building the Digital Twin
    ├── digital_twin_launch.py
    ├── synchronizer.py
    ├── sensor_fusion_ekf.py
    ├── humanoid_digital_twin.urdf
    └── validate_twin.py
```

## Prerequisites

### Software Requirements

- **Ubuntu 22.04** (or WSL2 on Windows)
- **ROS2 Humble Hawksbill**
- **Gazebo Harmonic**
- **Python 3.10+**
- **Unity 2021+ HDRP** (for Chapter 4-5)

### Installation

Follow the installation guides in each chapter directory:

- Chapter 1: `chapter1/install_gazebo.sh`
- Chapter 1: `chapter1/install_unity.md`

## Running Examples

### Chapter 1 - Simple Simulation

```bash
cd chapter1
bash install_gazebo.sh
python3 launch_simulation.py
```

### Chapter 2 - Mobile Robot

```bash
cd chapter2
ros2 launch gazebo_launch.py
ros2 run my_robot simple_controller
```

### Chapter 3 - Biped Walking

```bash
cd chapter3
ros2 launch biped_launch.py
python3 record_data.py
python3 analyze_data.py
```

### Chapter 4 - Unity Visualization

1. Open Unity project
2. Import ROS# package
3. Attach scripts to robot
4. Run ROS bridge
5. Press Play in Unity

### Chapter 5 - Digital Twin

```bash
cd chapter5
ros2 launch digital_twin_launch.py
```

## Testing

Each chapter includes test scripts to verify the examples work correctly.

## Troubleshooting

See individual chapter README files for troubleshooting guides.

## License

Apache 2.0 - Same as the textbook
