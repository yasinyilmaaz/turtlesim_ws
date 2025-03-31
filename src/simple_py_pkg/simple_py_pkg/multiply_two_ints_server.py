#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from simple_interface_pkg.srv import MultiplyTwoInts


class MultiplyTwoIntsServerNode(Node): #1
    def __init__(self):
        super().__init__("multiply_two_ints_server") # 2 
        self.server_ = self.create_service(MultiplyTwoInts, "multiply_two_ints", self.callback_multiply_two_ints)
        self.get_logger().info("Multiply Two Ints Server has been started.")

    def callback_multiply_two_ints(self, request, response):
        response.result = request.a * request.b # request il gönderilen değerler response alacak değer
        self.get_logger().info("Result: " + str(response.result))
        return response

        
def main(args=None):
    rclpy.init(args=args)
    node = MultiplyTwoIntsServerNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()