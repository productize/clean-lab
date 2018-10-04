from cv2 import *
import time
import datetime


cam = VideoCapture(0)
success, img = cam.read()
# If image taken
if success:
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M')
    date = timeStamp[:10]
    path = "/home/alvaro/Documents/DeepCleaning/images/" + date + "/"
    # Create folder for the day
    if not os.path.isdir(path):
        os.makedirs(path)
    imwrite(path + timeStamp + ".jpg", img)
