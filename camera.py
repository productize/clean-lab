# Copyright 2018 Productize SPRL

from picamera import PiCamera
import time
import datetime
from subprocess import call

def take_picture(path, rotate=False):
	with PiCamera() as camera:
		camera.start_preview()
		time.sleep(2)
		camera.capture(path)
		camera.stop_preview()

	if (rotate):
		# rotate image 180 due to installation orientation
		call(["convert", path, "-rotate", "180", path])

