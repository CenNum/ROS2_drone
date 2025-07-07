from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    
    rtabmap_common_params = {
        'frame_id': 'D400_link', 
        'odom_frame_id': 'odom_frame',
        'subscribe_depth': True,
        'subscribe_rgb': True,
        'subscribe_odom_info': False,
        'approx_sync': True,
        # ⬇️ [修改] 新增此參數，放寬時間同步的容忍度到 0.1 秒
        'approx_sync_max_interval': 0.1,
        'wait_for_transform': 0.2,
        'use_sim_time': use_sim_time,
        'Rtabmap/DetectionRate': '2',
        'Vis/MinInliers': '10',
        'Grid/CellSize': '0.05',
    }

    # 根據您最新的話題列表進行精確對應
    rtabmap_remaps = [
        ('rgb/image', '/D400/color/image_raw'),
        ('rgb/camera_info', '/D400/color/camera_info'),
        ('depth/image', '/D400/aligned_depth_to_color/image_raw'),
        ('odom', '/T265/pose/sample'),
    ]

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', 
            default_value='False',
            description='Use simulation (Gazebo) clock if true'),

        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            parameters=[rtabmap_common_params],
            remappings=rtabmap_remaps,
            output='screen',
        ),

        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            name='rtabmap_viz',
            parameters=[rtabmap_common_params],
            remappings=rtabmap_remaps,
            output='screen',
        )
    ])