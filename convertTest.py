import os
import glob
from time import sleep
 
while True:
    # Get a list of all the file paths that ends with .txt from in specified directory
    filePath = glob.glob('/media/usbkey/videos/*.h264')

    # As file at filePath is deleted now, so we should check if file exists or not not before deleting them
    if filePath:
        os.system('for i in /media/usbkey/videos/*.h264; do ffmpeg -i "$i" -codec copy  "${i%.*}.mp4"; rm "$i"; done')
        print("------------ deleted %s" % filePath)
    else:
        print("Can not delete the file as it doesn't exists")
        sleep(1)

