cmake_minimum_required(VERSION 3.8)
project(simple_robot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# rviz dosyasında kayıtlı başlatma durumu
# launch ros2 uygulamalarının beraber tek seferde çaıştırma ayarları bulunmaktadır.

install(DIRECTORY urdf launch
  DESTINATION share/${PROJECT_NAME}/
  )

ament_package()
