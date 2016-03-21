import picamera as pi
import time
import datetime



class PiCamera(object):

    def __init__(self):
        self.camera = pi.PiCamera()

    def get_picture(self):
        ts = time.time()
        return self.camera.capture('picture-%s',datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))