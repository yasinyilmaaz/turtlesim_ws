#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

"""
# remote controller node: bu node bir televizyon kanalını kontrolü

# mesaj subscriber (abone olma) node
# yayınlanan mesajın tipi String

#### callback fonksiyonu
bir olayın gerçekleştiğinde otomatik olarak çağrılan bir fonksiyondur. 


# publisher veriyi yayınlar
# publisher bir abonenin callback fonksiyonunda yada main fonksiyonunda çalışırtırılır.


# subscriber bir publisher'a abone olur ve mesajı alır
# subscriber veriyi alır ve gösterir

# eğer publisher paylaşım durur ise subscriber'da durur ama kapanmaz

"""

class RemoteControllerNode(Node): #1
    def __init__(self):
        super().__init__("remote_controller_node") # 2 
        self.subscriber_ = self.create_subscription(String, "channel_something",self.callback_television,10) # mesaj tipi , "abone olunacak topic adı", callback fonksiyonu, yayınlanan mesajların kuyrukta birikme sayısı
        self.get_logger().info("remote controller has been subscribed !")



    def callback_television(self, msg):
        self.get_logger().info(msg.data) # mesajı alır ve loglar

def main(args=None):
    rclpy.init(args=args)
    node = RemoteControllerNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()