#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # geometry bilgisi için gerekli olan kütüphane x y z konumları için

"""
# Service server node

Service nedir?
Service, bir düğümden diğerine veri göndermek için kullanılan bir iletişim şeklidir.
topicte bir veri devamlı olarak gönderilirken, service'de çağırıldıklarında veri sağlanır.

request: istemci tarafından gönderilen veri
response: sunucu(server) tarafından döndürülen veri
Service'ler genellikle bir istemci ve bir sunucu arasında çalışır.


ros2 interface show service example_interfaces/srv/AddTwoInts # servis mesajı hakkında bilgi almaktadır. içinde request ve response vardır

ros2 service list # çalışan servisleri listelemek için
ros2 service info /add_two_ints # servis hakkında bilgi almak için
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 1, b: 2}" # servisi çağırmak için



"""

class AddTwoIntsServerNode(Node): #1
    def __init__(self):
        super().__init__("add_two_ints_server") # 2 
        self.server_ = self.create_service(AddTwoInts, "add_two_ints", self.callback_add_two_ints)
        self.get_logger().info("Add Two Ints Server has been started.")

    def callback_add_two_ints(self, request, response):
        response.sum = request.a + request.b # request il gönderilen değerler response alacak değer
        self.get_logger().info("Result: " + str(response.sum))
        return response

        
def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServerNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()