#!/usr/bin/env python3

# 1. library
import rclpy
from rclpy.node import Node

# FOnksiyonel node oluşturuldu

# 2. Method
def main(args=None):
    rclpy.init(args=args) # Node begin
    node = Node("py_node") # Node oluşturulur

    # print("Hello World!")
    node.get_logger().info("Hello World!") # Çıktı Almak için


    # Node Yaşam döngüsü başlatılır
    rclpy.spin(node) # durdurulduğunda
    # Node yok edilir
    rclpy.shutdown()


# 3. "if __name__" block
# ben vu scritp çağırdığımda çalışacak
if __name__ == "__main__":
    main()