# picam-motion-detector
Project takes video recording when a person triggers a motion sensor.
Video is converted to MP4 and transfered to an external USB device. 
File names are named by date and time of recording.
Final code requires a raspberry pi, raspberry camera, PIR sensor, push button and led

Dependencies are as follows:

sudo apt-get install ffmpeg python-picamera

external drive to be preared and automounted as /media/usb 

example entry in /etc/fstab file:

/dev/sda1 /media/usb vfat auto,nofail,noatime,users,rw,uid=pi,gid=pi 0 0

uid=pi and gid=pi allows us to write without need of administrative privileges

The code must be inside directory /home/pi/camCapture/

Otherwise the directory must be changed in the code (obviously) 
