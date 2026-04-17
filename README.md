# ROS2 6DOF Arm Simulation

This project contains a 6-DOF robotic arm simulation built using:

- ROS 2 Jazzy
- Gazebo Harmonic
- ros2_control
- MoveIt 2

## Features

- URDF-based robot model
- Gazebo simulation with physics
- ros2_control integration
- MoveIt-ready configuration

## Usage

```bash
colcon build
source install/setup.bash
ros2 launch six_dof_arm gazebo.launch.py
