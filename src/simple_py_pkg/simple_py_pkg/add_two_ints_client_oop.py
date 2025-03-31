#!/usr/bin/env python3
# sistemdeki doğru python sürümünü çalıştırır
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial

"""
# AddTwoIntsClientNode: AddTwoInts mesaj tipi ile iki tane integer değeri toplayan bir client node oluşturuldu
iki callback fonksiyonu var:
1. call_add_two_ints_server: server ile iletişim kuracak fonksiyon
2. callback_call_add_two_ints: sonuçları yazdıracak fonksiyon
# client node server node'a istek gönderir ve server node'dan gelen response'ı alır
# client node server ile iletişim kurarken iki tane integer değeri toplar

ros2 service type /clear # servis tipini gösterir
ros2 service list # çalışan servisleri listelemek için
ros2 service show /add_two_ints # servis hakkında bilgi almak için
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 1, b: 2}" # servisi çağırmak için



ros2 run simple_py_pkg add_two_ints_server_node --ros-args -r add_two_ints:=new_client
ros2 run simple_py_pkg add_two_ints_client_oop_node --ros-args -r add_two_ints:=new_client
"""

class AddTwoIntsServerNode(Node): #1
    def __init__(self):
        super().__init__("add_two_ints_client") # 2 

        self.call_add_two_ints_server(7,8)
        self.call_add_two_ints_server(1,-2)
        self.call_add_two_ints_server(4,7)
        self.call_add_two_ints_server(7,-2)


    # server ile iletişim kuracak fonksiyon
    def call_add_two_ints_server(self, a, b):
        #### yeniden isimlendirme yapıldığında server name de değişir bu yüzden server ve client isimleri aynı olmalı
        client_ = self.create_client(AddTwoInts, "add_two_ints") # istemci oluşturuldu
        while not client_.wait_for_service(1.0): # server hazır olana kadar bekle
            self.get_logger().warn("Waiting for server (Add Two Ints)")

        request = AddTwoInts.Request() # request oluşturuldu
        request.a = a
        request.b = b

        future = client_.call_async(request)
        # future = asenkron bir şekilde server ile iletişim kuruldu
        # colback içinde colback fonksiyonu çağrıldı
        future.add_done_callback(partial(self.callback_call_add_two_ints, a=a, b=b)) # 4
        # partial = fonksiyona birden fazla parametre göndermek için kullanılır
        

    # sonuçları yazdıracak fonksiyon
    def callback_call_add_two_ints(self, future, a, b):
        try:
            response = future.result() # işlem tamamlandıktan sonra response alındı
            self.get_logger().info("Result: " + str(response.sum)) # response yazdırıldı
        except Exception as e: # sonuç alınamazsa hata mesajı yazdırılır
            self.get_logger().error("Service call faild %r" % {e,})

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServerNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()