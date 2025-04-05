#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim_interfaces.srv import CoordinateDraw

"""
servisleri kullanarak turtle'ı belirli koordinatlara yönlendiren bir node
Üçgen çizmen gerektiğim için 3 tane koordinat belirledim

"""

class CoordinateDrawServerNode(Node):
    def __init__(self):
        super().__init__("coordinate_info_server")
        self.get_logger().info("Coordinat info Server has been started.")

        self.get_coordinate(1.0, 1.0)
        self.get_coordinate(1.0, 10.0)
        self.get_coordinate(5.5, 5.5)

    # servise konum bilgisi gönderir
    def get_coordinate(self, x, y):
        # servise bağlanması için bekler ve bağlanır
        client_ = self.create_client(CoordinateDraw, "/coordinate_draw") # 3
        while not client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting again...")
        
        # servise gönderilecek olan x ve y koordinatları için bir istek oluşturur
        request = CoordinateDraw.Request()
        request.x = float(x)
        request.y = float(y)

        self.get_logger().info(f"Requesting {request.x} + {request.y}")
        future = client_.call_async(request)
        
        future.add_done_callback(self.callback_call_catch_turtle) # 4

    # Sunucudan gelen cevabı kontrol eder ve ekrana yazdırır
    def callback_call_catch_turtle(self, future):
        try: # response değeri alınana kadar hata yazdırılır
            response = future.result() 
            self.get_logger().info(f"process result {response.success}") # response yazdırıldı
        except Exception as e: 
            self.get_logger().error("Service call faild %r" % {e,})


# node aşlatır
def main(args=None):
    rclpy.init(args=args)
    node = CoordinateDrawServerNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()