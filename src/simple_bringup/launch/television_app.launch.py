from launch import LaunchDescription
from launch_ros.actions import Node

"""
# launch dosyası
# launch dosyası ile node'ları tek yerden başlatabiliriz
# launch dosyası ile node'ları başlatırken parametreleri ve remap'leri de ayarlayabiliriz

ros2 launch simple_bringup television_app.launch.py

"""


def generate_launch_description():
    ld = LaunchDescription() # launch objesi oluşturuluyor
    remap_channel_topic = ("channel_something", "new_channel_something") # topic yeniden adlandırma, tuple olarak tanımlanıyor


    # çalıştırmak istediğimiz node tanımlanıyor
    television_publiser_node = Node(
        package="simple_py_pkg", # paket adı
        executable="channel_node", # çalıştırılabilir adı yabi setup.py içinde ki entry point
        name="new_channel_node",
        # burda yaptığımız adlandırma 
        # yada diğer durum ile bağlantılı bir değişiklikte her iki taraftada komut yer alması gerekmektedir
        remappings=[
            remap_channel_topic
        ],
        parameters=[
            {"parameter_1_int": 5},
            {"parametrer_2_string":"ROS2"}
        ]
    )

    reemote_publiser_node = Node(
        package="simple_py_pkg",
        executable="remote_controller_node",
        name="new_remote_controller_node",
        remappings=[
            remap_channel_topic
        ]
    )

    # NOde başlatılıyor
    ld.add_action(television_publiser_node)
    ld.add_action(reemote_publiser_node)



    return ld