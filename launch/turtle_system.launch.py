import os
import launch.actions
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch.actions import LogInfo
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnShutdown, OnProcessExit

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    explore = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
            FindPackageShare("turtle_exploration"), '/launch', '/turtle_exploration.launch.py'])   
    )

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("turtlebot3_gazebo"), '/launch', '/turtlebot3_big_house.launch.py'])   
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("turtlebot3_cartographer"), '/launch', '/cartographer.launch.py']),
            launch_arguments={'use_sim_time': 'True'}.items()         
    )

    pose_est = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("turtle_pose_estimation"), '/launch', '/turtle_pose_estimation.py'])
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("turtlebot3_navigation2"), '/launch', '/navigation2.launch.py']),
            launch_arguments={'use_sim_time': 'True', 'map': '$HOME/turtlebot3_ws/turtle_launch/good_map.yaml'}.items()    
    )

    exploration_timer = launch.actions.TimerAction(
        period=7.0,
        actions=[
            LogInfo(msg="Timer Finished"),
            explore
        ]
    )

    nav2_event = RegisterEventHandler(
        OnProcessExit(
            target_action=explore,
            on_exit=[
                LogInfo(msg='Exploration Done'),
                nav2,
                pose_est
            ]
        )
    )

    return LaunchDescription([
        exploration_timer,
        simulation,
        slam,
        nav2_event
    ])