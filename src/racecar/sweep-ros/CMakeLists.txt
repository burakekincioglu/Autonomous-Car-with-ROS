cmake_minimum_required(VERSION 2.8.3)
project(sweep_ros)

find_package(catkin REQUIRED
  COMPONENTS
    pcl_conversions
    pcl_msgs
    rosconsole
    roscpp
    sensor_msgs
)

find_package(PCL REQUIRED)
find_package(Sweep REQUIRED)
find_package(Threads REQUIRED)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Wextra")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -Wextra")

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS}
)

## Add link directories
link_directories(
  ${PCL_LIBRARY_DIRS}
)

catkin_package(
  CATKIN_DEPENDS sensor_msgs
)

add_executable(sweep_node src/node.cpp)
add_executable(sweep_node_minified src/node_minified.cpp)

target_link_libraries(sweep_node ${catkin_LIBRARIES} ${LIBSWEEP_LIBRARY})
target_link_libraries(sweep_node_minified ${catkin_LIBRARIES} ${LIBSWEEP_LIBRARY})

target_include_directories(sweep_node SYSTEM PRIVATE ${LIBSWEEP_INCLUDE_DIR})
target_include_directories(sweep_node_minified SYSTEM PRIVATE ${LIBSWEEP_INCLUDE_DIR})

install(TARGETS sweep_node
        ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
        LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
        RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
install(TARGETS sweep_node_minified
        ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
        LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
        RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
