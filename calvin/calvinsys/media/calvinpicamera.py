import picamera as pi
import time
import datetime

class CalvinPiCamera(object):

    def __init__(self):
        self.camera = pi.PiCamera()

    def get_picture(self):
        ts = time.time()
        pict_name = 'picture-%s.jpg' % datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.camera.capture(pict_name)
        return pict_name

    def get_picture_stream(self):
        picture = self.get_picture()
        return open(picture).read()


def register(node=None, actor=None):
    return CalvinPiCamera()