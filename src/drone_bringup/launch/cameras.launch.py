# 文件路径: ~/ros2_ws/src/drone_bringup/launch/drone_sensors.launch.py
# [已修改] 強制對齊深度並匹配實際話題名稱

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    realsense_ros_dir = get_package_share_directory('realsense2_camera')

    sensors_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(realsense_ros_dir, 'launch', 'rs_multi_camera_launch.py')
        ),
        launch_arguments={
            # --- D435/D400 series camera ---
            'camera_name1': 'D400',            # [修改] 匹配您實際的話題名稱
            'serial_no1': '_146322077649',     # ❗ 必须是您D435的序列号
            'depth_module.profile1': '640,480,15',
            'rgb_camera.profile1': '640,480,15',
            'enable_depth1': 'true',
            'align_depth.enable1': 'true',     # [確保] 強制啟用深度對齊
            'pointcloud.enable1': 'true',

            # --- T265 camera ---
            'camera_name2': 'T265',            # [修改] 匹配您實際的話題名稱
            'serial_no2': '_230322111176',     # ❗ 必须是您T265的序列号
            'enable_pose2': 'true',
            'enable_fisheye12': 'false',
            'enable_fisheye22': 'false',
            'publish_odom_tf2': 'true',
            # 'topic_odom_in2': 'odom',
            # 'pose_frame_id2': 'T265_pose_frame',
        }.items()
    )


    static_tf_T265_link_to_T265_pose_frame = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_T265_link_to_T265_pose_frame',
        arguments=[
            '0.0', '0.0', '0.0', '0.0', '0.0', '0.0',
            'T265_pose_frame', 'T265_link'  # [修改] 匹配相機名稱
        ]
    )

    static_tf_T265_link_to_base_footprint = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_T265_link_to_base_footprint',
        arguments=[
            '-0.16', '0.0', '-0.02', '0.0', '0.0', '0.0',
            'T265_link', 'base_footprint'  # [修改] 匹配相機名稱
        ]
    )

    static_tf_T265_link_to_D400_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_T265_link_to_D400_link',
        arguments=[
            '0.0', '0.0', '0.0', '0.0', '0.0', '0.0',
            'T265_link', 'D400_link'  # [修改] 匹配相機名稱
        ]
    )

    return LaunchDescription([
        sensors_launch,
        # static_tf_T265_link_to_T265_pose_frame,
        static_tf_T265_link_to_base_footprint,
        # static_tf_T265_link_to_D400_link
    ])
   