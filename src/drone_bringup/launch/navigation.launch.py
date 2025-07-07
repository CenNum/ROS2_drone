# ~/ros2_ws/src/drone_bringup/launch/navigation.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('drone_bringup')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # 配置文件路径
    map_file = os.path.join(pkg_share, 'maps', 'my_map.yaml')
    nav2_params_file = os.path.join(pkg_share, 'params', 'nav2_params.yaml')

    # 启动Nav2
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_file,
            'params_file': nav2_params_file,
            'use_sim_time': 'False' # 我们使用真实硬件
        }.items()
    )

    # 启动深度图转LaserScan节点
    depth_to_scan_node = Node(
        package='depthimage_to_laserscan',
        executable='depthimage_to_laserscan_node',
        name='depthimage_to_laserscan',
        remappings=[
            ('image', '/d435/depth/image_rect_raw'),
            ('camera_info', '/d435/depth/camera_info'),
            ('scan', '/scan') # Nav2默认监听/scan话题
        ],
        parameters=[{
            'output_frame': 'd435_link', # 与你的TF匹配
            'range_min': 0.2, # 根据无人机安全距离设置
            'range_max': 5.0, # 根据D435有效范围设置
        }]
    )

    return LaunchDescription([
        nav2_launch,
        depth_to_scan_node,
    ])
