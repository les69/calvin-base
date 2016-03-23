import picamera as pi
import time
import datetime
from calvin.utilities.utils import absolute_filename

class CalvinPiCamera(object):

    def __init__(self):
        self.camera = pi.PiCamera()

    def get_picture(self):
        ts = time.time()
        pict_name = 'picture-%s.jpg' % datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.camera.capture(pict_name)
        return absolute_filename(__file__, pict_name)