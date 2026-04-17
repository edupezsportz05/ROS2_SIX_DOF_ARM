from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_path = get_package_share_directory('six_dof_arm')

    urdf_file = os.path.join(pkg_path, 'urdf', 'six_dof_gazebo.urdf')
    world_file = os.path.join(pkg_path, 'worlds', 'empty.world')
    controllers_file = os.path.join(pkg_path, 'config', 'controllers.yaml')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([

        # Tell Gazebo where to find resources
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=pkg_path
        ),

        # Start Gazebo
	ExecuteProcess(
	    cmd=[
		'gz', 'sim',
		world_file,
		'-r',
	    ],
	    output='screen'
	),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        # Spawn robot
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'six_dof_arm',
                '-topic', 'robot_description',
                '-z', '0.1'
            ],
            output='screen'
        ),

        # Controllers
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster'],
            output='screen'
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['arm_controller'],
            output='screen'
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['gripper_controller'],
            output='screen'
        ),
    ])
