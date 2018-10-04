from picamera import PiCamera
import time
import datetime
from subprocess import call

camera = PiCamera()

# get time stamp to name image
ts = time.time()
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M')
path = "/home/pi/deepclean/output_images/" + timeStamp + ".jpg"
print(path)

# take picture
camera.start_preview()
time.sleep(5)
camera.capture(path)
camera.stop_preview()

# rotate image 180 due to installation orientation
#call(["convert", path, "-rotate", "180", path])

