from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()



    # çalıştırmak istediğimiz node tanımlanıyor
    turtlesim_node = Node(
        package="turtlesim", # paket adı
        executable="turtlesim_node", # çalıştırılacak node adı 
    )

    triagle_corner = Node(
        package="turtlesim_application",
        executable="triangle_corner_node",
    )

    draw_triangle = Node(
        package="turtlesim_application",
        executable="draw_triangle_node",
    )
    spawn_turtle = Node(
        package="turtlesim_application",
        executable="spawn_turtles_node",
    )

    go_to_loc = Node(
        package="turtlesim_application",
        executable="go_to_location_node",
    )

    # Düğümler sırayla başlatılır
    ld.add_action(turtlesim_node)
    ld.add_action(triagle_corner)
    ld.add_action(draw_triangle)
    ld.add_action(spawn_turtle)
    ld.add_action(go_to_loc)


    return ld