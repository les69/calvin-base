from calvin.actor.actor import Actor, ActionResult, condition, guard
from calvin.utilities.calvinlogger import get_logger

from runtime.south.plugins.media.defaultimpl.picamera import PiCamera
from utilities.utils import absolute_filename
_log = get_logger(__name__)

class FaceDetect(Actor) :
    """
    Detect faces in a jpg-image

    Inputs:
        image: Image to analyze
    Outputs:
        faces: non-zero if face detected
    """

    def init(self, delay=3):
        self.delay = delay
        self.use('calvinsys.events.timer', shorthand='timer')
        self.timer = None
        self.setup()

    def setup(self):
        self.timer = self['timer'].repeat(self.delay)
        self.use("calvinsys.media.image", shorthand="image")
        self.camera = PiCamera()
        self.image = self["image"]
        self.picture = None

    def did_migrate(self):
        self.setup()

    @condition([], ['faces'])
    @guard(lambda self: self.picture)
    def detect(self):
        found = self.image.detect_face(self.picture)
        _log.info('From FaceDetect found = %s' % found)
        return ActionResult(production=(found, ))

    @condition([], [])
    @guard(lambda self, _: self.timer and self.timer.triggered)
    def take_picture(self, token):
        self.timer.ack()
        self.picture = self.camera.get_picture()
        return ActionResult()

    action_priority = (take_picture, detect )
    requires =  ['calvinsys.media.image']
