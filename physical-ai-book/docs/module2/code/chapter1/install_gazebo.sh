#!/bin/bash
# Gazebo Harmonic Installation Script for Ubuntu 22.04
# This script installs Gazebo Harmonic and ROS2 Humble integration

set -e  # Exit on error

echo "=========================================="
echo "Gazebo Harmonic Installation Script"
echo "=========================================="

# Check if running on Ubuntu
if [ ! -f /etc/lsb-release ]; then
    echo "Error: This script is designed for Ubuntu only"
    exit 1
fi

# Add Gazebo repository
echo "Adding Gazebo repository..."
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list'

# Add Gazebo keys
echo "Adding Gazebo keys..."
wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

# Update package list
echo "Updating package list..."
sudo apt update

# Install Gazebo Harmonic
echo "Installing Gazebo Harmonic..."
sudo apt install -y gazebo18 libgazebo18-dev

# Install ROS2 Gazebo packages (if ROS2 is installed)
if command -v ros2 &> /dev/null; then
    echo "Installing ROS2 Gazebo packages..."
    sudo apt install -y ros-humble-gazebo-ros-pkg
fi

# Verify installation
echo ""
echo "Verifying installation..."
gz sim --version

echo ""
echo "=========================================="
echo "Gazebo Harmonic installed successfully!"
echo "=========================================="
echo ""
echo "To test the installation, run:"
echo "  gz sim empty_world.sdf"
echo ""
echo "For ROS2 integration, source your ROS2 setup:"
echo "  source /opt/ros/humble/setup.bash"
echo ""
