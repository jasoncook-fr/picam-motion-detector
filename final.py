import RPi.GPIO as GPIO
import time
from time import sleep
from picamera import PiCamera
from datetime import datetime
import os
import glob
from threading import  Thread
import sys

recordFlag = False
#--- delay values for sensor activated recording ---
sensorDelay = 0 # in seconds, change value for video recording timeout when no more movement is sensed
lastTime = 0
thisTime = 0
#--- delay values for kill switch ---
killDelay = 3 # in seconds, change value for time desired to hold down kill switch
killTime = 0
lastKillTime = 0

ledPin = 11
sensorPin = 7
stopSwitch = 13
camera = PiCamera(resolution=(1280, 720), framerate=25)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stopSwitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def converter():
    while True:
        filePath = glob.glob('/media/usb/*.h264')
        if filePath:
            os.system('for i in /media/usb/*.h264; do ffmpeg -i "$i" -codec copy  "${i%.*}.mp4"; rm "$i"; done')
            #print("------------ deleted %s" % filePath)
            sleep(.5) # add slight delay in case killswitch stops the process, to avoid returning to conversion

def killSwitch():
    while True:
        if GPIO.input(stopSwitch) == GPIO.LOW:
            killTime = int(time.time() - lastKillTime)
            if killTime >= killDelay:
                quickFlashLed()
                camera.stop_recording() # in case the camera is currently recording, stop it
                os.system('killall ffmpeg') # add this in case we are in process of converting last video
                os.system("sudo shutdown -h now")
                sleep(.1) # buffering time
        else:
            lastKillTime = time.time()
            sleep(.1) # buffering time

def quickFlashLed():
    for x in range(0,10):
        GPIO.output(ledPin, GPIO.HIGH)
        sleep(.1)
        GPIO.output(ledPin, GPIO.LOW)
        sleep(.1)

quickFlashLed()

try:
    t = Thread(target = killSwitch)
    t.daemon=True
    t.start()
    t = Thread(target = converter)
    t.daemon=True
    t.start()

    while True: # Run forever
        filename = "{0:%m}-{0:%d}-{0:%H}-{0:%M}-{0:%S}.h264".format(datetime.now())
        if GPIO.input(sensorPin) == GPIO.HIGH:
            GPIO.output(ledPin, GPIO.HIGH)
            recordFlag = True
            #print("Button was pushed!")
            camera.start_recording(filename, format='h264', quality=23)
            lastTime = time.time()
            while recordFlag == True:
                if GPIO.input(sensorPin) == GPIO.LOW:
                    thisTime = int(time.time() - lastTime)
                    #print("!!! SENSOR IS OFF !!! current time limit is "), thisTime 
                    sleep(.1) # buffering time. video recording gets choppy without it
                    if thisTime > sensorDelay:
                        recordFlag = False
                else:
                    lastTime = time.time()
                    sleep(1)

            camera.stop_recording()
            #print("recording finished!")
            os.system('mv /home/pi/camCapture/*.h264 /media/usb/')
            #print("!!!!!!!!!!!!!!!!  ALL DONE  !!!!!!!!!!!!!!!!!")
            GPIO.output(ledPin, GPIO.LOW)

except (KeyboardInterrupt, SystemExit):
    print '\n! Received keyboard interrupt, quitting threads.\n'
    sys.exit()
