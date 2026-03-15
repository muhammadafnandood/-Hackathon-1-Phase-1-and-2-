# Module 3 Labs

This directory contains hands-on lab exercises for Module 3: AI Robot Brain (NVIDIA Isaac).

## Lab List

| Lab | Title | Duration | Difficulty |
|-----|-------|----------|------------|
| Lab 1 | Isaac Sim Setup | 90 min | Intermediate |
| Lab 2 | Synthetic Dataset | 90 min | Advanced |
| Lab 3 | Visual SLAM | 90 min | Advanced |
| Lab 4 | Nav2 Navigation | 90 min | Advanced |
| Lab 5 | RL Training | 120 min | Expert |

## Prerequisites

Before starting any lab, ensure you have:

- [ ] NVIDIA RTX GPU (minimum 6GB VRAM)
- [ ] Ubuntu 22.04 or WSL2
- [ ] ROS2 Humble installed
- [ ] Isaac Sim 4.0+ installed
- [ ] Python 3.10+ with dependencies
- [ ] PyTorch 2.0+ with CUDA

## Lab Environment Setup

### Quick Setup Script

```bash
# Install all dependencies
sudo apt update
sudo apt install -y ros-humble-nav2* \
                     ros-humble-slam-toolbox \
                     ros-humble-isaac-ros* \
                     python3-pip

pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
pip3 install numpy isaacgym
```

### Verification

```bash
# Verify ROS2
ros2 --version

# Verify Isaac Sim
python3 -c "import isaacgym; print('Isaac Sim OK')"

# Verify PyTorch with CUDA
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

## Submission Guidelines

For each lab, submit:

1. **Screenshots** of running simulation
2. **Recorded data** (rosbag files)
3. **Training plots** (for Lab 5)
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
- Ask on Discord #module3-help channel

## Additional Resources

- [Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim)
- [ROS2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [Nav2 Documentation](https://navigation.ros.org/)
- [Isaac ROS](https://github.com/NVIDIA-ISAAC-ROS)
