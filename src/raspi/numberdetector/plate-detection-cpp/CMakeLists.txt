cmake_minimum_required (VERSION 3.0)
project (PlateDetection)
# The version number.
set (PlateDetection_VERSION_MAJOR 1)
set (PlateDetection_VERSION_MINOR 0)

find_package(OpenCV REQUIRED)
find_package(cppzmq)
 
 
# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
include_directories(include)
include_directories(lib/protobuf/pb)
 
# add the executable
add_executable(Main src/main.cpp src/PlateDetec.cpp src/ZeroMQ.cpp)


target_link_libraries(Main ${OpenCV_LIBS})
target_link_libraries(Main cppzmq)