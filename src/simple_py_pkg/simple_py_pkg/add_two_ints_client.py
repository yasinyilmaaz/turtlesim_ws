#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # request, response

# AddTwoInts mesaj tipi ile AddTwoIntsClientNode oluşturuldu
# AddTwoIntsClientNode: AddTwoInts mesaj tipi ile iki tane integer değeri toplayan bir client node oluşturuldu
# client node server node'a istek gönderir ve server node'dan gelen response'ı alır
        
def main(args=None):
    rclpy.init(args=args)
    node = Node("add_two_ints_client") # 3
    
    # servis server bekliyor
    client_ = node.create_client(AddTwoInts, "add_two_ints") # istemci oluşturuldu


    while not client_.wait_for_service(1.0): # server hazır olana kadar bekle
        # [WARRING]: 
        node.get_logger().warn(" Waiting for server (Add Two Ints)")

    request = AddTwoInts.Request() # request çağrıldı
    request.a = 15
    request.b = 4
    # servis yanıtını beklediğimiz için asenkrond çalıştırıyoruz
    # server bir istek aldığında yanıt verir
    future = client_.call_async(request) # istemciye request gönderildi
    rclpy.spin_until_future_complete(node, future) # işlem tamamlanana kadar bekle

    #
    try:
        response = future.result() # sonuç alınırsa response değişkenine atanır. alınmaz ise hata mesajı yazdırılır
        node.get_logger().info("Result: " + str(response.sum)) # response yazdırıldı
    except Exception as e: # sonuç alınamazsa hata mesajı yazdırılır
        node.get_logger().error("Service call faild %r" % {e,})



    rclpy.shutdown() # rclpy kapatılır


if __name__ == "__main__":
    main()

"""# Terminalde çalıştırmak için:"""