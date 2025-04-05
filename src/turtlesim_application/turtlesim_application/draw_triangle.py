#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim_interfaces.msg import CornerDraw
from turtlesim_interfaces.msg import CornerStatus # bool mesajı
from turtlesim_interfaces.srv import CoordinateDraw
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
        self.corners_ = [] # kordinatları tutan bir liste
        self.corner_ = None #sırada ki kordinat

        self.publishers_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10) # turtle i yönlendirmek için bir publisher
        self.publishers_success = self.create_publisher(CornerStatus, "/corner_draw_success", 10) # kordinatların başarıyla çizildiğini bildiren bir publisher
        self.subscriber_ = self.create_subscription(Pose, "turtle1/pose", self.callback_turtle_pose, 10) # turtle'ın pozisyonunu almak için bir subscriber
        
        self.service = self.create_service(CoordinateDraw, "/coordinate_draw", self.call_catch_turtle) # kordinatları almak için bir service
        
        self.timer = self.create_timer(1, self.turtle_controller)
        self.get_logger().info("Draw Triangle Node has been started")

    # gelen kordinatları listeye ekler
    def call_catch_turtle(self, request, response):
        self.get_logger().info("Coordinate Draw Service has been called")
        self.corners_.append({"x": request.x, "y": request.y}) 
        self.corner_ = self.corners_[0] if len(self.corners_) > 0 else None
        self.get_logger().info(f"Coordinate received: ({self.corner_})")
        response.success = True
        return response

    # turtle pozisyonunu alır(x,y,theta)
    def callback_turtle_pose(self, msg):
        self.pose_ = msg

        
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
            self.publis_message_coordinate(True)
            self.get_logger().info(f"{self.corner_} has been drawn.")
        else:
            self.publis_message_coordinate(False)

        self.publishers_.publish(msg)
    
    # turtle'ın kordinatları başarıyla çizildiğinde mesaj gönderir
    def publis_message_coordinate(self, status=False):
        msgs = CornerStatus()
        msgs.status = status
        self.publishers_success.publish(msgs)
        self.get_logger().info("Triangle has been drawn.") if status else self.get_logger().info("Next corner is being drawn.")

# node başlatılır
def main(args=None):
    rclpy.init(args=args)
    node = DrawTriangle()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()