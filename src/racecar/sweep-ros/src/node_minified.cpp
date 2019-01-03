
/*The MIT License (MIT)
 *
 * Copyright (c) 2017, Scanse, LLC
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
#define _USE_MATH_DEFINES

#include "ros/ros.h"
#include <pcl/point_types.h>
#include "sensor_msgs/PointCloud2.h"
#include "sensor_msgs/LaserScan.h"
#include <pcl/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sweep/sweep.hpp>
#include <math.h>

ros::Time ros_past, ros_now;
void publish_scan(ros::Publisher *pub,
                  const sweep::scan *scan, std::string frame_id)
{
    
    ros_now = ros::Time::now();
    sensor_msgs::LaserScan laser_msg;

    float angle;
    float range;
    int i = 0;
    
    laser_msg.angle_min = -M_PI;
    laser_msg.angle_max = M_PI;
    laser_msg.angle_increment = M_PI * 2 / 360;
    laser_msg.scan_time = ((ros::Duration)(ros_now - ros_past)).toSec();
    laser_msg.range_min = 0;
    laser_msg.range_max = 40;
    laser_msg.ranges.resize(360, INFINITY);

    for (const sweep::sample& sample : scan->samples)
    {
        range = sample.distance / 100.f;
        angle = ((float)sample.angle / 1000); //millidegrees to degrees
        laser_msg.ranges[(int)angle] = range;
        i++;
    }

    laser_msg.header.frame_id = frame_id;
    laser_msg.header.stamp = ros_now;
    
    ros_past = ros_now;
    pub->publish(laser_msg);
}


int main(int argc, char *argv[]) try
{
    //Initialize Node and handles
    ros::init(argc, argv, "sweep_node");
    ros::NodeHandle nh;
    ros::NodeHandle nh_private("~");

    //Get Serial Parameters
    std::string serial_port;
    nh_private.param<std::string>("serial_port", serial_port, "/dev/ttyUSB0");
    int serial_baudrate;
    nh_private.param<int>("serial_baudrate", serial_baudrate, 115200);

    //Get Scanner Parameters
    int rotation_speed;
    nh_private.param<int>("rotation_speed", rotation_speed, 5);

    int sample_rate;
    nh_private.param<int>("sample_rate", sample_rate, 500);

    //Get frame id Parameters
    std::string frame_id;
    nh_private.param<std::string>("frame_id", frame_id, "laser_frame");

    //Setup Publisher
    ros::Publisher scan_pub = nh.advertise<sensor_msgs::LaserScan>("scan", 1000);

    //Create Sweep Driver Object
    sweep::sweep device{serial_port.c_str()};

    //Send Rotation Speed
    device.set_motor_speed(rotation_speed);

    //Send Sample Rate
    device.set_sample_rate(sample_rate);

    ROS_INFO("expected rotation frequency: %d (Hz)", rotation_speed);

    //Start Scan
    device.start_scanning();

    while (ros::ok())
    {
        //Grab Full Scan
        const sweep::scan scan = device.get_scan();

        publish_scan(&scan_pub, &scan, frame_id);

        ros::spinOnce();
    }

    //Stop Scanning & Destroy Driver
    device.stop_scanning();
}

    catch (const sweep::device_error& e) {
      std::cerr << "Error: " << e.what() << std::endl;
}
