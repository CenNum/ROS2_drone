import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
import xacro 

def generate_launch_description():

    # ... (前面的代码保持不变) ...
    pkg_share = get_package_share_directory('drone_description')
    urdf_file_name = 'drone.urdf.xacro'
    urdf_path = os.path.join(pkg_share, 'urdf', urdf_file_name)
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # 将xacro文件处理成urdf字符串
    robot_description_raw = xacro.process_file(urdf_path).toxml()

    # ======================= 节点 =======================

    # 1. robot_state_publisher 节点
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            # 使用处理后的urdf字符串
            'robot_description': robot_description_raw
        }]
    )

    # ... (后面的 joint_state_publisher_gui_node 和 rviz_node 保持不变) ...
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(pkg_share, 'rviz', 'display.rviz')],
        output='screen'
    )


    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])