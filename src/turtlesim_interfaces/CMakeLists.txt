cmake_minimum_required(VERSION 3.8)
project(turtlesim_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
# Mesajları ve servisleri otomatik olarak derlemek ve kullanılabilir hale getirmek.
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Turtle.msg"
  "msg/TurtleArray.msg"
  "msg/CornerDraw.msg"
  "msg/CornerStatus.msg"
  "srv/CatchTurtles.srv"
  "srv/CoordinateDraw.srv"
)



ament_export_dependencies(rosidl_default_runtime)
ament_package()
