#!/usr/bin/env python3
"""
Simple Gazebo Simulation Launch Script
Module 2 - Chapter 1

This script launches a simple Gazebo simulation with the simple_world.sdf file.

Usage:
    python3 launch_simulation.py
    
Or with custom world:
    python3 launch_simulation.py --world path/to/world.sdf
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Launch Gazebo simulation with specified world file'
    )
    
    parser.add_argument(
        '--world', '-w',
        type=str,
        default='simple_world.sdf',
        help='Path to SDF world file (default: simple_world.sdf)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run Gazebo in headless mode (no GUI)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def check_gazebo_installed():
    """Check if Gazebo is installed."""
    try:
        result = subprocess.run(
            ['gz', 'sim', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"✓ Gazebo found: {result.stdout.strip()}")
            return True
        else:
            print("✗ Gazebo not found")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("✗ Gazebo not found. Please install Gazebo Harmonic first.")
        print("  Run: bash install_gazebo.sh")
        return False


def find_world_file(world_path):
    """Find the world file in common locations."""
    world_file = Path(world_path)
    
    # Check if file exists at given path
    if world_file.exists():
        return str(world_file)
    
    # Check in current directory
    current_dir = Path(__file__).parent
    local_path = current_dir / world_path
    if local_path.exists():
        return str(local_path)
    
    # Check in worlds subdirectory
    worlds_dir = current_dir / 'worlds'
    worlds_path = worlds_dir / world_path
    if worlds_path.exists():
        return str(worlds_path)
    
    return None


def launch_gazebo(world_file, headless=False, verbose=False):
    """Launch Gazebo with the specified world file."""
    cmd = ['gz', 'sim']
    
    if headless:
        cmd.append('-s')  # Server mode (headless)
    
    if verbose:
        cmd.append('-v')  # Verbose output
    
    cmd.append(world_file)
    
    print(f"\nLaunching Gazebo with: {world_file}")
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        # Launch Gazebo
        process = subprocess.run(
            cmd,
            check=True,
            text=True
        )
        
        return process.returncode == 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Gazebo exited with error: {e.returncode}")
        return False
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user")
        return True
    except Exception as e:
        print(f"\n✗ Error launching Gazebo: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print("Module 2 - Chapter 1: Simple Simulation Launch")
    print("=" * 60)
    print()
    
    # Parse arguments
    args = parse_arguments()
    
    # Check Gazebo installation
    if not check_gazebo_installed():
        print("\nInstallation instructions:")
        print("  Ubuntu: bash install_gazebo.sh")
        print("  Other:  See https://gazebosim.org/docs/latest/install")
        sys.exit(1)
    
    # Find world file
    world_file = find_world_file(args.world)
    
    if world_file is None:
        print(f"\n✗ World file not found: {args.world}")
        print("\nSearched in:")
        print(f"  - {args.world}")
        print(f"  - {Path(__file__).parent / args.world}")
        print(f"  - {Path(__file__).parent / 'worlds' / args.world}")
        sys.exit(1)
    
    print(f"✓ World file found: {world_file}")
    
    # Launch Gazebo
    success = launch_gazebo(world_file, args.headless, args.verbose)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
