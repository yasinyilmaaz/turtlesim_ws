#!/usr/bin/env python3
import rclpy
import math
import sys
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from functools import partial
from turtlesim_interfaces.srv import CatchTurtles
from turtlesim_interfaces.msg import TurtleArray, Turtle

"""
Turtle1 kablumbağası için bir hedefe gitme ve hedefi yok etmesini sağlayan uygulama
"""

class GoToLocationNode(Node):
    def __init__(self):
        super().__init__("go_to_loc_node")
        self.get_logger().info("Go To Location Node has been started!")
        self.coeff = 0.85 # gidilecek konumda daha yumuşak bir duruş sağlamk için
        self.pose_threshold_linear = 0.2 # doğrusal hata
        self.pose_threshold_angular = 0.01 # açısal hata

        #self.target_x = 2.0 # float(sys.argv[1]) # 0.0 - 11.0 [INFO: default loc_x ~ 5.5]
        #self.target_y = 8.0 # float(sys.argv[2]) # 0.0 - 11.0 [INFO: default loc_y ~ 5.5]
        # koordinatlara erişim için
        self.new_turtle_subscriber_ = self.create_subscription(TurtleArray, "/new_turtles",self.callback_turtles, 10)
        self.pose_ = None # kaplumbağanın pozisyonu
        self.new_turtle_to_catch_= None # yakalanacak kaplumbağa

        
        self.publishers_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscriber_ = self.create_subscription(Pose, "turtle1/pose", self.callback_turtle_pose, 10)
        
        self.timer = self.create_timer(1, self.turtle_controller)

    # turtle pozisyonunu alır(x,y,theta)
    def callback_turtle_pose(self, msg):
        self.pose_ = msg

    # yakalanacak kaplumbağanın bilgilerini alır
    def callback_turtles(self, msg):
        if len(msg.turtles) > 0:
            self.new_turtle_to_catch_ = msg.turtles[0]

    #
    def turtle_controller(self):
        # eğer kaplumbağa yoksa veya yakalanacak kaplumbağa yoksa hata almamak için geri döner
        if self.pose_ == None or self.new_turtle_to_catch_ == None:
            return

        # kaplumbağanın ile hedef arasında mesafe hesaplanır
        msg = Twist()
        dist_x =self.new_turtle_to_catch_.x - self.pose_.x # x mesafe
        dist_y = self.new_turtle_to_catch_.y - self.pose_.y # y mesafe
        distance = math.sqrt(dist_x**2 + dist_y**2) # mesafe
        target_theta = math.atan2(dist_y, dist_x) # açısal değeri

        # açısal değer kontrol edilir ve açısal hız atanır
        if abs(target_theta- self.pose_.theta) > self.pose_threshold_angular: # hedef açısal değeri
            msg.angular.z = float(target_theta - self.pose_.theta) * self.coeff # açısal hız

        else:
            # doğrusal hız kontrol edilir ve doğrusal hız atanır
            if distance >= self.pose_threshold_linear: #  hedef mesafesi
                msg.linear.x = distance * self.coeff
            else:
                msg.linear.x = 0.0
                msg.angular.z = 0.0 # vardığında dönmemesi için
                self.call_catch_turtle_server(self.new_turtle_to_catch_.name) # robotu yok etmek için
                self.new_turtle_to_catch_ = None # servisin edğeri sıfırlar
                self.get_logger().info("Success!")

        self.publishers_.publish(msg)

    # turtle yok etme işlemi için server ile iletişim kuracak fonksiyon
    def call_catch_turtle_server(self, turtle_name):
        client_ = self.create_client(CatchTurtles, "/catch_turtle") # istemci oluşturuldu
        while not client_.wait_for_service(1.0): # server hazır olana kadar bekle
            self.get_logger().warn("Waiting for server (kill Turtles)")

        request = CatchTurtles.Request() # request çağrılır
        request.name = turtle_name

        future = client_.call_async(request)
        # future = asenkron bir şekilde server ile iletişim kuruldu
        # colback içinde colback fonksiyonu çağrıldı
        future.add_done_callback(partial(self.callback_call_catch_turtle,turtle_name=turtle_name)) # 4
        # partial = fonksiyona birden fazla parametre göndermek için kullanılır
    
    # Sunucudan gelen cevabı kontrol eder ve ekrana yazdırır
    def callback_call_catch_turtle(self, future, turtle_name):
        try: # response değeri alınana kadar hata yazdırılır
            response = future.result() 
            self.get_logger().info("Turtle: " + turtle_name + "is catched!") # response yazdırıldı
        except Exception as e: 
            self.get_logger().error("Service call faild %r" % {e,})

# başlangıç fonksiyonu
def main(args=None):
    rclpy.init(args=args)
    node = GoToLocationNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()