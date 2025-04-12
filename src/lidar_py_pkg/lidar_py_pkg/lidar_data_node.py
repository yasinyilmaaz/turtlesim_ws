#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

"""
Lidar mesaj tipindeki verilerini almak ve mesaj göndermek için bir node oluşturuyoruz.
kullanım:
    lidarın ölçtüğü mesafe bilgilerini kullanarak eğer 2.5 metreden daha yakın bir nesne varsa
    robotu durdur. 
"""

class LidarDataNode(Node):
    def __init__(self):
        super().__init__("lidar_data_node")

        # lidar verilerini almak için bir /lidar/out konusuna abone ol
        self.subscriber_ = self.create_subscription(LaserScan, "/lidar/out", self.callback_data, 10)
        self.get_logger().info("Lİdar node has been started")
        # robotun hareket etmesi için bir /cmd_vel yayınını oluştur
        self.publisher_ = self.create_publisher(Twist,"/cmd_vel",10)

    def callback_data(self, msg):
        # min değerleri alma sebebi sonsuz değerlerin atılmak istenmesi
        min_lidar_data = min(msg.ranges) # lidar dönen değerler ranges listesinde tutulur. uzaklık mesafesini sonsuz ise inf değeri  döner
        # ros2 run lidar_py_pkg lidar_py_pkg_node --- düğüm komutu ile bu değerleri alabiliriz
        
        
        # lidar verilerini işleme

        velocity = Twist()
        velocity.linear.x = 0.5
        velocity.linear.y = 0.0
        velocity.angular.z = 0.0

        # eğer lidarımız bir nesneye uzaklık 2.5 metreden az ise durdur 
        if min_lidar_data <= 2.5:
            velocity.linear.x = 0.0
            velocity.linear.y = 0.0
            velocity.angular.z = 0.0
            self.get_logger().info("Obstacle detected! Stopping and turning.")
        
        self.publisher_.publish(velocity)

        self.get_logger().info("Lidar Data: " + str(min_lidar_data))

# node oluşturma ve başlatma
def main(args=None):
    rclpy.init(args=args)
    node = LidarDataNode()
    rclpy.spin(node)
    rclpy.shutdown()

    if __name__ == "__main__":
        main()