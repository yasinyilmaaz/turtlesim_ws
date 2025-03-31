#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

"""
# mesaj publisher (yayınlama) node
# yayınlanan mesajın tipi String

# ROS2 TOPİC KULLANIMI
# bir düğümdeki veri bir veya birden fazla başka düğüme gönderilirken topic kullanılır

# publisher: veri gönderen düğüm (yayınlama)
# subscriber: veri alan düğüm (takip etme)
# topic: veri gönderilen ve alınan kanal

# ros2 topic list : çalışan topic'leri listelemek için
# ros2 topic info /topic_name : topic hakkında bilgi almak için
# ros2 topic echo /topic_name : topic'ı dinlemek için


####################################3
# PARAMETRE KULLANIMI
ros2 param  list # parametreleri listelemek için eğer çalışan bir düğüm var ise  "use_sim_time" varsayılan olarak gelir.
ros2 param get /node_name param_name # parametreyi almak için
ros2 param set /node_name param_name value # parametreyi ayarlamak için
"""



class ChannelNode(Node): #1
    def __init__(self):
        super().__init__("channel_node") # 2 
        # declare parameter()
        self.declare_parameter("parameter_1_int")
        self.declare_parameter("parameter_2_string")
        #declare parameter()

        self.greeting_ = "Hi, awesome people :). "
        self.publisher_ = self.create_publisher(String, "channel_something", 10) # mesaj tipi , "topic adı", yayınlanan mesajların kuyrukta birikme sayısı
        self.timer_ = self.create_timer(0.5, self.publish_channel) # belli zaman aralığında çalışacak callback fonksiyonu
        self.get_logger().info("Channel Something has been publisher !") # çalışmaya başladığını gösterir

    # mesaj yayınlama
    def publish_channel(self):
        msg = String() # mesaj tipi
        msg.data = str(self.greeting_) + "welcam to the Channel Someting" # mesaj içeriği
        self.publisher_.publish(msg) # mesaj yayınlama

def main(args=None):
    rclpy.init(args=args)
    node = ChannelNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()