#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

"""
Belli bir süre aralığında teminatöre "hello word" yazdıran bir node oluşturulmuştur

# Her değişiklikte sonra build edilmeli
# Ros2 değişkenliklerden sonra "_" eklenir. (opsiyonel)
# eğer her değişiklikten sonra build etmek istemiyorsak -- symlink-install
# colcon build --packages-select --symlink-install

# DÜĞÜM ADLANDIRMA
# node isimleri benzersiz olmalıdır
# ros2'de node aynı isimde çalışması durumunda hata verir ama çalışır
# ros2 run simple_py_pkg counter_node --ros-args --remap __node:=abc
--remap __node:=abc : node ismi değiştirilir

# RQT ve RQT_GRAPH
# rqt, rqt_graph: ros2 node'ları ve topic'leri görselleştirmek için kullanılır

# DENEME
# ros2 kurduktan sonra denemek için
ros2 run demo-nodes-cpp talker

# NODE
# ros2 node list : çalışan node'ları listelemek için
# ros2 node info /node_name : node hakkında bilgi almak için


# TURTLESİM
# turtlesim: ros2'deki bir simülasyon aracıdır
 # kurulum 
 # sudo apt install ros-humble-turtlesim

 # çalıştırmak için 
# ros2 run turtlesim turtlesim_node : turtlesim node'u çalıştırmak için
# ros2 run turtlesim turtle_teleop_key : turtlesim haraket node'u çalıştırmak için

"""







class CounterNode(Node): #1
    def __init__(self):
        super().__init__("counter_node") # Node başlatılır ve isimlendirilir
        self.counter_ = 0
        self.create_timer(0.5, self.timer_callback) # belli zaman aralığında çalışacak


    #  callback fonksiyonu belli bir süre aralığında çalışır
    def timer_callback(self):
        self.counter_ += 1 
        self.get_logger().info("Hello world!! - " + str(self.counter_))


#Node çağırır
def main(args=None):
    rclpy.init(args=args)
    node = CounterNode() # 3
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()