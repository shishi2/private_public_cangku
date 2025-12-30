sudo apt install xvfb
sudo apt install x11-apps -y

X11Forwarding yes
X11UseLocalhost yes

export DISPLAY=:0 

echo $DISPLAY

xauth list
echo $XAUTHORITY

xhost +SI:localuser:root
xhost +

touch /root/.Xauthority
xauth add ($(xauth list))

<!-- docker run -it --net host \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /datameta/linshuo/maby_fastlivo:/ws \
  --name ros_noetic_env \
  osrf/ros:noetic-desktop-full bash -->

<!-- docker start -ai ros_noetic_env -->
<!-- docker rm ros_noetic_env  -->

<!-- docker start ros_noetic_env
docker exec -it ros_noetic_env bash -->


<!-- catkin_make -->
<!-- source /opt/ros/noetic/setup.bash # 启动ROS # docker 中 在bashrc中自动启动 -->
<!-- source devel/setup.bash # 启动项目 -->

<!-- 
#### test
docker run -it --net host \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /datameta/linshuo/test_ros:/ws \
  --name ros_test \
  osrf/ros:noetic-desktop-full bash -->

  <!-- xhost +local:root -->
