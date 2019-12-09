import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
from picamera import PiCamera
from datetime import datetime
import os

camera = PiCamera()

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    filename = "{0:%m}-{0:%d}-{0:%H}-{0:%M}-{0:%S}.h264".format(datetime.now())
    if GPIO.input(7) == GPIO.HIGH:
        print("Button was pushed!")
        camera.start_recording(filename, resize=(1024, 768))
	sleep(30)
        camera.stop_recording()
        print("recording finished!")
	os.system("mv /home/pi/camCapture/%s /media/usbkey/videos/" % filename)
	#os.system('for i in /media/usbkey/videos/*.h264; do ffmpeg -i "$i" -codec copy  "${i%.*}.mp4"; rm "$i"; done')
	print("!!!!!!!!!!!!!!!!  ALL DONE  !!!!!!!!!!!!!!!!!")
