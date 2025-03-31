#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

# Düğüm içinde parametere gönderimi
# roboto komut gönderme girişler değiştiğinde komut gönderme gibi işlerde

class RobotCommandNode(Node): #1
    def __init__(self):
        super().__init__("robot_command") # 2
        # ikinci verilen parametre eğer hiç değer girilmez ise çalışır
        self.declare_parameter("command_to_publish","wait for command..") # parametre tanımlama

        self.command_ = self.get_parameter("command_to_publish").value # parametreyi alma
        self.command_publisher_ = self.create_publisher(String, "command", 10)
        self.command_timer_ = self.create_timer(1.0, self.publish_command)

        self.get_logger().info("Robot Command has been published")


    def publish_command(self):
        msg = String()
        msg.data = self.command_ # parametreyi mesaj içine koyma
        self.command_publisher_.publish(msg)




def main(args=None):
    rclpy.init(args=args)
    node = RobotCommandNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()