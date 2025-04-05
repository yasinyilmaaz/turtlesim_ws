#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim_interfaces.msg import CornerDraw

"""
konum kordinatlarını tutan ve her bir kordinatı sırayla yayınlayan node

"""

class TriangleCornerNode(Node):
    def __init__(self):
        super().__init__("triangle_corner_node")
        # kordinatları tutan bir liste
        self.corners_ = [
            {"x": 1.0, "y": 1.0},
            {"x": 1.0, "y": 10.0},
            {"x": 5.5, "y": 5.5}
        ]
        self.counter_ = 0 # kordinatları sırayla yayınlamak için bir sayaç
        self.publishers_corner_ = self.create_publisher(CornerDraw, "/corner_draw", 10) # kordinatları yayınlamak için bir publisher
        self.timer_ = self.create_timer(1, self.corner_creater) # 1 saniyede bir kordinat yayınlamak için bir timer
        self.get_logger().info("Triangle Corner Node has been started")

    # kordinatları sırayla yayınlayan callback fonksiyonu
    def corner_creater(self):
        if self.counter_ >= len(self.corners_): # eğer tüm kordinatlar yayınlandıysa
            self.get_logger().info("All corners have been drawn.")
            return
        # sırayla kordinatları alınır
        x = self.corners_[self.counter_]["x"]
        y = self.corners_[self.counter_]["y"]
        
        # kordinatları yayınlamak için bir mesaj oluşturulur
        corner_msg = CornerDraw()
        corner_msg.x = x
        corner_msg.y = y
        self.counter_ += 1 
        self.publishers_corner_.publish(corner_msg)
        self.get_logger().info(f"Corner drawn at: ({x}, {y})")

# çalıştırılacak node tanımlanıyor
def main(args=None):
    rclpy.init(args=args)
    node = TriangleCornerNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()