#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from simple_interface_pkg.srv import MultiplyTwoInts
from functools import partial

class MultiplyTwoIntsServerNode(Node): #1
    def __init__(self):
        super().__init__("multiply_two_ints_client") # 2 

        self.call_multiply_two_ints_server(7,8)
        self.call_multiply_two_ints_server(1,-2)
        self.call_multiply_two_ints_server(4,7)
        self.call_multiply_two_ints_server(7,-2)


    # server ile iletişim kuracak fonksiyon
    def call_multiply_two_ints_server(self, a, b):
        client_ = self.create_client(MultiplyTwoInts, "multiply_two_ints") # istemci oluşturuldu
        while not client_.wait_for_service(1.0): # server hazır olana kadar bekle
            self.get_logger().warn("Waiting for server (Add Two Ints)")

        request = MultiplyTwoInts.Request() # request oluşturuldu
        request.a = a
        request.b = b

        future = client_.call_async(request)
        # future = asenkron bir şekilde server ile iletişim kuruldu
        # colback içinde colback fonksiyonu çağrıldı
        future.add_done_callback(partial(self.callback_call_multiply_two_ints, a=a, b=b)) # 4
        # partial = fonksiyona birden fazla parametre göndermek için kullanılır
        

    # sonuçları yazdıracak fonksiyon
    def callback_call_multiply_two_ints(self, future, a, b):
        try:
            response = future.result() # işlem tamamlandıktan sonra response alındı
            self.get_logger().info("Result: " + str(response.result)) # response yazdırıldı
        except Exception as e: # sonuç alınamazsa hata mesajı yazdırılır
            self.get_logger().error("Service call faild %r" % {e,})

def main(args=None):
    rclpy.init(args=args)
    node = MultiplyTwoIntsServerNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()