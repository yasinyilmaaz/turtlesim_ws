cmake_minimum_required(VERSION 3.8) # Cmake minimum versiyon
project(simple_interface_pkg) # Proje adı

# GNU C++ veya Clang kullanılıyorsa, derleyici uyarılarını etkinleştir
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
  # -wall: Tüm genel uyarıları etkinleştirir.
  # -Wextra: Ekstra uyarıları açar.
  # -Wpedantic: Standart dışı kodlamalara karşı katı kurallar uygular.
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
# rosidl_default_generators:mesaj ve srv türlerini otomatik olarak oluşturmayı sağlayan modülleri ekler


# mesaj, srv dosyaları için gerekli bağımlılıkları bul
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/ComponentsStatus.msg" # mesaj formatı
  "srv/MultiplyTwoInts.srv" # servis formatı
  )

ament_export_dependencies(roidl_Default_runtime) # bağımlılıkları dışa aktarma
ament_package()# ament paketlenebilir hae getirilir
