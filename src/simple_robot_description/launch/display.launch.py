from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_path

"""
Oluşturulan robotun rviz ortamında görselleştirilir

urdf dosya formatında oluşturulan robot robot_state_publisher ile /tf paylaşılır
robot_state_publisher ile eklem bilgileri paylaşılır
bu veriler rviz ortamında görselleştirilir
"""

def generate_launch_description():

    # verilen adresler birleştiriliyor
    # get_package_share_path: kaynak dosyanın tam yolunu almak için kullanılır
    urdf_path = os.path.join(get_package_share_path("simple_robot_description"), "urdf", "simple_robot.urdf")

    # xacro ile urdf dosyasını işler
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    # Robot durum bilgilerini /tf topic'ine yayınlar
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}],
    )

    # Eklemleri manuel kontrol için GUI paneli açar
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        
    )

    # rviz başlatır
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
    )

    # hepsini çalıştırır
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz2_node,
    ])