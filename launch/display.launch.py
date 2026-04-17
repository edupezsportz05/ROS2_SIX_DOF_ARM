from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
import os

def generate_launch_description():

    urdf_file = os.path.join(
        os.getenv('HOME'),
        'dev_ws/src/six_dof_arm/urdf/six_dof.urdf'
    )

    robot_description = ParameterValue(
        Command(['cat ', urdf_file]),
        value_type=str
    )

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),

        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[
                {'robot_description': robot_description},
                os.path.join(
                    os.getenv('HOME'),
                    'dev_ws/src/six_dof_arm/config/controllers.yaml'
                )
            ],
            output='screen'
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster']
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['arm_controller']
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['gripper_controller']
        ),
    ])
