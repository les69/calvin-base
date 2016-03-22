import picamera as pi
import time
import datetime



class CalvinPiCamera(object):

    def __init__(self):
        self.camera = pi.PiCamera()

    def get_picture(self):
        ts = time.time()
        return self.camera.capture('picture-%s.jpg' % datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))