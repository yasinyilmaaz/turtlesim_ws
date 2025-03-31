#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

"""

    ROS2 kullanarak bir turtle simülasyonunda bir turtle'ın kontrol etmek için bir düğüm oluşturur
    Bu düğüm, belirli bir doğrusal hız ve yarıçap kullanarak açısal hızı hesaplar ve bu bilgiyi bir mesaj olarak yayınlar
    Bu kodu çalıştırmak için terminalden şu komutu kullanabilirsiniz:
        ros2 run turtlesim_py_pkg vel_controller 2.0 1.0
    turtle'ın 2 birim/saniye hızla ve 1 birim yarıçap etrafında dönmesini sağlar
    bir düğüm oluşturuldu ve bir yayıncı (publisher) tanımlandı
    Yayıncı, belirli bir konuya (topic) mesaj gönderir. Bu durumda, "/turtle1/cmd_vel" konusuna bir Twist mesajı(doğrusal ve açısal hız) gönderilir
"""



class VelPublisherNode(Node):
    def __init__(self):
        super().__init__("vel_contoller_node")
        self.publishers_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(1, self.publisher_vel)

        self.get_logger().info("Velocity Controller Node has been started!")

    def publisher_vel(self):
        msg = Twist() #  msg Twist türünde bir mesaj oluşturur
        # w = v/r
        #Terminalden değerleri alındı
        linear_x = float(sys.argv[1])
        radius =  float(sys.argv[2])
        
        msg.linear.x = linear_x # x konumunda değişim
        msg.linear.y = 0.0 # y konumunda değişim
        msg.angular.z = float(linear_x/radius) # radian=  -3.14 & +3.14
        self.publishers_.publish(msg)


# başlama fonksiyonu
def main(args=None):
    rclpy.init(args=args)
    node = VelPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()