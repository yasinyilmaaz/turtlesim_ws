#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

# Hazır bir template oluşturuldu
# Bu template'i kullanarak yeni bir node oluşturulabilir

# Burada bir node oluşturulacak
# Node kalıtım olarak metodlarını ve fonksiyonlarını miras olarak alır
# super () fonksiyonu ile üst sınıfın __init__ fonksiyonu çağrılır
# Bu sayede üst sınıfın özellikleri kullanılabilir


class CustomNodeName(Node): #1
    def __init__(self):
        super().__init__("node_name") # 2: her node için benzersiz bir isim verilmelidir


def main(args=None):
    rclpy.init(args=args)
    node = CustomNodeName() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()