# Module 3 Code Examples

This directory contains executable code examples for all chapters in Module 3: AI Robot Brain (NVIDIA Isaac).

## Directory Structure

```
code/
├── chapter1/          # NVIDIA Isaac Platform
│   ├── install_isaac_sim.sh
│   ├── isaac_sim_robot.py
│   ├── bridge_config.py
│   └── isaac_ros2_launch.py
├── chapter2/          # Synthetic Data and Simulation
│   ├── generate_data.py
│   ├── randomization_config.py
│   └── coco_exporter.py
├── chapter3/          # Visual SLAM
│   ├── visual_slam_launch.py
│   ├── vslam_integrator.py
│   └── sensor_fusion_ekf.py
├── chapter4/          # Nav2 Navigation
│   ├── nav2_config_humanoid.yaml
│   ├── nav2_launch.py
│   └── nav2_goal_publisher.py
└── chapter5/          # Reinforcement Learning
    ├── train_rl.py
    ├── policy_deploy.py
    └── sim_to_real.py
```

## Prerequisites

### Software Requirements

- **Ubuntu 22.04** (or WSL2 on Windows)
- **NVIDIA GPU** (RTX 3060 or better recommended)
- **CUDA 11.7+**
- **ROS2 Humble Hawksbill**
- **NVIDIA Isaac Sim 4.0+**
- **Python 3.10+**
- **PyTorch 2.0+ with CUDA**

### Installation

Follow the installation guides in each chapter directory:

- Chapter 1: `chapter1/install_isaac_sim.sh`
- Chapter 1: See textbook for detailed setup instructions

## Running Examples

### Chapter 1 - Isaac Sim Platform

```bash
cd chapter1
bash install_isaac_sim.sh
python3 isaac_sim_robot.py
```

### Chapter 2 - Synthetic Data

```bash
cd chapter2
python3 generate_data.py --config randomization_config.py
python3 coco_exporter.py
```

### Chapter 3 - Visual SLAM

```bash
cd chapter3
ros2 launch visual_slam_launch.py
python3 vslam_integrator.py
```

### Chapter 4 - Nav2 Navigation

```bash
cd chapter4
ros2 launch nav2_launch.py map:=my_map.yaml
python3 nav2_goal_publisher.py --goal 2.0 3.0 1.57
```

### Chapter 5 - Reinforcement Learning

```bash
cd chapter5
python3 train_rl.py --env bipedal --algo ppo
python3 policy_deploy.py --checkpoint checkpoint_final.pt
```

## Testing

Each chapter includes test scripts to verify the examples work correctly.

## Troubleshooting

See individual chapter README files for troubleshooting guides.

## License

Apache 2.0 - Same as the textbook
