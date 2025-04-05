#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim_interfaces.msg import CornerDraw
from turtlesim_interfaces.msg import CornerStatus # bool mesajı
from geometry_msgs.msg import Twist

"""
triangle_corner yayınladığı /corner_draw topic'ine gelen kordinatları sırayla alır ve turtle'ı o kordinata yönlendirir
gelen kordinatlar bittiğinde turtle durur ve /corner_draw_success mesajı ile spawn_turtle topic'ine True mesajı gönderir
"""

class DrawTriangle(Node):
    def __init__(self):
        super().__init__("draw_triangle")

        self.pose_ = None # turtle'ın pozisyonunu tutan bir değişken
        self.coeff = 0.85 # hız katsayısı
        self.pose_threshold_linear = 0.2 # doğrusal hız eşiği
        self.pose_threshold_angular = 0.01 # açısal hız eşiği     

        self.publishers_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10) # turtle i yönlendirmek için bir publisher
        self.corners_ = [] # kordinatları tutan bir liste
        self.corner_ = None #sırada ki kordinat
        self.publishers_success = self.create_publisher(CornerStatus, "/corner_draw_success", 10) # kordinatların başarıyla çizildiğini bildiren bir publisher
        self.subscriber_ = self.create_subscription(Pose, "turtle1/pose", self.callback_turtle_pose, 10) # turtle'ın pozisyonunu almak için bir subscriber
        self.subscriber_corner_ = self.create_subscription(CornerDraw, "/corner_draw", self.call_draw_corner, 10) # kordinatları almak için bir subscriber
        self.timer = self.create_timer(1, self.turtle_controller)
        self.get_logger().info("Draw Triangle Node has been started")

    # turtle pozisyonunu alır(x,y,theta)
    def callback_turtle_pose(self, msg):
        self.pose_ = msg

    # kordinarlar alır
    def call_draw_corner(self, msg):
        self.corners_.append({"x": msg.x, "y": msg.y}) # gelen kordinatları listeye ekler
        self.corner_ = self.corners_[0] if len(self.corners_) > 0 else None
        self.get_logger().info(f"Corner received: ({msg.x}, {msg.y})")
        
    # turtle'ı kordinata yönlendirir
    def turtle_controller(self):
        if self.pose_ is None or self.corner_ is None:
            self.get_logger().warn("Pose or corner not set yet.")
            return
        # turtle'ın pozisyonunu alır
        msg = Twist()
        dist_x = self.corner_["x"] - self.pose_.x # x mesafesi
        dist_y = self.corner_["y"] - self.pose_.y # y mesafesi
        distance = math.sqrt(dist_x**2 + dist_y**2) # gidilecek noktaya olan mesafe
        target_theta = math.atan2(dist_y, dist_x) # hedef açısı

        if abs(target_theta - self.pose_.theta) > self.pose_threshold_angular:
            msg.angular.z = float(target_theta - self.pose_.theta) * self.coeff # açısal hız
        else:
            # doğrusal hız kontrol edilir ve doğrusal hız atanır
            if distance >= self.pose_threshold_linear: #  hedef mesafesi
                msg.linear.x = distance * self.coeff
            else:
                msg.linear.x = 0.0
                msg.angular.z = 0.0 # vardığında dönmemesi için
                self.corners_.pop(0) # kordinatları sırayla alır
                self.corner_ = self.corners_[0] if len(self.corners_) > 0 else None
                # gidilmeyen kordinat var mı kontrol edilir ve ona göre mesaj gönderilir
                if len(self.corners_) == 0:
                    msgs = CornerStatus()
                    msgs.status = True
                    self.publishers_success.publish(msgs)
                    self.get_logger().info("Triangle has been drawn.")
                else:
                    msgs = CornerStatus()
                    msgs.status = False
                    self.publishers_success.publish(msgs)
                    self.get_logger().info("Next corner is being drawn.")
        self.publishers_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = DrawTriangle()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()