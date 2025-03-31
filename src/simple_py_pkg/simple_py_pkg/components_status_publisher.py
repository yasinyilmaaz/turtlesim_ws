#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from simple_interface_pkg.msg import ComponentsStatus # mesa tipi import edildi

"""
# arayüz bileşenlerinin durumunu kontrol eden bir node
iki arayüz bileşeni var:
1. msg 
2. srv

"""


class ComponentsStatusPublisherNode(Node): #1
    def __init__(self):
        super().__init__("components_status_publisher") # 2 
        self.components_status_publisher_ = self.create_publisher(ComponentsStatus, "components_status", 10)
        self.timer_ = self.create_timer(1.0, self.publish_components_status)
        self.get_logger().info("Components Status has been publisher !")

    # mesaj yayınlama fonksiyonu
    def publish_components_status(self):
        # mesaj içinde ki bilgileri dolduruyoruz
        msg = ComponentsStatus()
        msg.camera_is_ready = True
        msg.lidar_is_ready = True
        msg.motor_is_ready =True
        msg.debug_message = "Everything is going well !"
        self.components_status_publisher_.publish(msg) # mesajı yayınlıyoruz

# main ile node başlatılıyor
def main(args=None):
    rclpy.init(args=args)
    node = ComponentsStatusPublisherNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()