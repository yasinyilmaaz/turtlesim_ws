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
from turtlesim_interfaces.msg import CornerStatus
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
        self.status = False # kaplumbağaların durumu
        # koordinatlara erişim için
        self.new_turtle_subscriber_ = self.create_subscription(TurtleArray, "/new_turtles",self.callback_turtles, 10)
        self.pose_ = None # kaplumbağanın pozisyonu
        self.new_turtle_to_catch_= None # yakalanacak kaplumbağa

        
        self.publishers_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscriber_ = self.create_subscription(Pose, "turtle1/pose", self.callback_turtle_pose, 10)
        self.subscriber_corner_ = self.create_subscription(CornerStatus, "/corner_draw_success", self.callback_turtle_status, 10) # kordinatların başarıyla çizildiğini bildiren bir publisher
        self.timer = self.create_timer(1, self.turtle_controller)

    def callback_turtle_status(self, msg):
        self.get_logger().info(f"Status turtle is called! = {msg.status}")
        self.status = msg.status # gelen mesajın verisi alındı

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
        # status kontrol edilme sebebi eğer konum servisi çaılışır ise ilk onu yapacak sonrasında öldürme işlemini
        if self.pose_ == None or self.new_turtle_to_catch_ == None or self.status == False:
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