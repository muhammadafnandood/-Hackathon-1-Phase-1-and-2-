# Module 2 Labs

This directory contains hands-on lab exercises for Module 2: The Digital Twin (Gazebo & Unity).

## Lab List

| Lab | Title | Duration | Difficulty |
|-----|-------|----------|------------|
| Lab 1 | Simulation Setup | 60 min | Beginner |
| Lab 2 | Gazebo Mobile Robot | 90 min | Intermediate |
| Lab 3 | Sensor Data Recording | 90 min | Intermediate |
| Lab 4 | Unity Visualization | 90 min | Advanced |
| Lab 5 | Complete Digital Twin | 120 min | Advanced |

## Prerequisites

Before starting any lab, ensure you have:

- [ ] Ubuntu 22.04 or WSL2
- [ ] ROS2 Humble installed
- [ ] Gazebo Harmonic installed
- [ ] Python 3.10+ with dependencies
- [ ] (Optional) Unity 2021+ for Labs 4-5

## Lab Environment Setup

### Quick Setup Script

```bash
# Install all dependencies
sudo apt update
sudo apt install -y ros-humble-gazebo-ros-pkg \
                     ros-humble-rosbridge-suite \
                     python3-pip

pip3 install rclpy numpy filterpy matplotlib
```

### Verification

```bash
# Verify ROS2
ros2 --version

# Verify Gazebo
gz sim --version

# Verify Python packages
python3 -c "import rclpy; import numpy; import filterpy; print('OK')"
```

## Submission Guidelines

For each lab, submit:

1. **Screenshots** of running simulation
2. **Recorded data** (rosbag files)
3. **Analysis plots** (for Lab 3)
4. **Short report** (300-500 words)

## Grading Rubric

| Criteria | Points |
|----------|--------|
| Lab completion | 50% |
| Code correctness | 25% |
| Analysis quality | 15% |
| Report clarity | 10% |

## Getting Help

- Check TROUBLESHOOTING.md in each lab directory
- Review chapter content for theory
- Ask on Discord #module2-help channel

## Additional Resources

- [Gazebo Documentation](https://gazebosim.org/docs)
- [ROS2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [Unity ROS# Guide](https://github.com/siemens/ros-sharp)
