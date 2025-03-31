#!/usr/bin/env python3
import rclpy
import random
import math
from rclpy.node import Node
from functools import partial
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from turtlesim_interfaces.msg import Turtle # kaplumbağa mesajı
from turtlesim_interfaces.msg import TurtleArray # kaplumbağa dizisi mesajı

from turtlesim_interfaces.srv import CatchTurtles # kaplumbağa yakalama servisi

class SoawnTurtleNode(Node):
    def __init__(self):
        super().__init__("node")
        self.name_ = "turtle"
        self.counter_ = 1 # ilk oluşan kaplumbağanın sayısı ismi turtle1 olduğu için 1 olarak başlatıldı
        self.new_turtles_ = [] # oluşan kaplumbağaların listesi
        self.new_turtle_publisher_ = self.create_publisher(TurtleArray, "new_turtles", 10) # yeni oluşan kaplumbağlar için publisher yayınlanır
        
        self.catch_turtle_service_ = self.create_service(CatchTurtles, "catch_turtle", self.callback_catch_turtle) 
        self.timer_ = self.create_timer(5.0, self.spawn_turtle) # 5 saniyelik


    def callback_catch_turtle(self, request, response):
        self.call_kill_server(request.name)
        response.success= True
        return response

    # yeni oluşan kablumbağ verileri yayınlamayı sağlar
    def publish_new_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.new_turtles_
        self.new_turtle_publisher_.publish(msg)

    # random olarak turtle oluşturur
    def spawn_turtle(self):
        self.counter_ += 1 # isimlendirme için sayacı artır
        turtle_name = self.name_ + str(self.counter_) # turtle ismi
        # ekran boyutumuz (11,11)
        x = random.uniform(0.5, 10.5) # 0 - 11 arasında rastgele x değeri
        y = random.uniform(0.5, 10.5) # 0 - 11 arasında rastgele y değeri
        theta = random.uniform(0.0, 2*math.pi) # 0 - 2*pi arasında rastgele theta değeri
        self.call_spawn_turtle_server(x, y, theta, turtle_name) # 3
        
    # turtle oluşturma işlemi için server ile iletişim kuracak fonksiyon
    def call_spawn_turtle_server(self, x, y, theta, turtle_name):
        client_ = self.create_client(Spawn, "/spawn") # istemci oluşturuldu
        while not client_.wait_for_service(1.0): # server hazır olana kadar bekle
            self.get_logger().warn("Waiting for server (Spawn Turtles)")

        # request değerleri atanır
        request = Spawn.Request() # request çağrıldı
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name

        future = client_.call_async(request)
        # servis yanıtını beklediğimiz için asenkrond çalıştırıyoruz
        # server bir istek aldığında yanıt verir
        future.add_done_callback(partial(self.callback_call_spawn_ints, x=x, y=y, theta=theta, turtle_name=turtle_name)) # 4
        # partial = fonksiyona birden fazla parametre göndermek için kullanılır
        

    
    # turtle oluşturma işlemi gerçekleştirilecek callback fonksiyonu
    def callback_call_spawn_ints(self, future, x, y, theta, turtle_name):
        try: # response değeri alınana kadar hata yazdırılır
            response = future.result() # işlem tamamlandıktan sonra response alındı
            if response.name != "":
                self.get_logger().info("Turtle: " + response.name + "is created!") # response yazdırıldı
                new_turtle = Turtle() # yeni kaplumbağa çağrıldı
                new_turtle.name = response.name
                new_turtle.x = x
                new_turtle.y = y
                new_turtle.theta = theta
                self.new_turtles_.append(new_turtle) # oluşan turtle listesine eklendi
                self.publish_new_turtles() # yeni kaplumbağa yayınlandı
        except Exception as e: 
            self.get_logger().error("Service call faild %r" % {e,})
    
    # silme işlemi için server ile iletişim kuracak fonksiyon
    def call_kill_server(self, turtle_name):
        client_ = self.create_client(Kill, "/kill") # istemci çağrıldı
        while not client_.wait_for_service(1.0): # server hazır olana kadar bekle
            self.get_logger().warn("Waiting for server (kill Turtles)")

        request = Kill.Request() # request çağrıldı
        request.name = turtle_name

        future = client_.call_async(request)
        # future = asenkron bir şekilde server ile iletişim kuruldu
        # colback içinde colback fonksiyonu çağrıldı
        future.add_done_callback(partial(self.callback_call_kill_turtle,turtle_name=turtle_name)) # 4
        # partial = fonksiyona birden fazla parametre göndermek için kullanılır
    
    # silme işlemi gerçekleştirilecek callback fonksiyonu
    def callback_call_kill_turtle(self, future, turtle_name):
        try: # response değeri alınana kadar hata yazdırılır
            response = future.result() # işlem tamamlandıktan sonra response alındı
            for (i, turtle) in enumerate(self.new_turtles_):
                if turtle_name == turtle.name:
                    del self.new_turtles_[i]
                    self.publish_new_turtles()
                    break
        except Exception as e: 
            self.get_logger().error("Service call faild %r" % {e,})

# başlatıcı fonksiyon
def main(args=None):
    rclpy.init(args=args)
    node = SoawnTurtleNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()