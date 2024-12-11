cmake_minimum_required(VERSION 3.30)
project(ImageEditor)

set(CMAKE_CXX_STANDARD 20)

# Update OpenCV directory
set(OpenCV_DIR "C:/tools/opencv/build")
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/")

# Find OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIB_DIRS})

add_executable(ImageEditor main.cpp)

# Link OpenCV libraries
target_link_libraries(ImageEditor ${OpenCV_LIBS})
