from calvin.actor.actor import Actor, ActionResult, condition, guard
from calvin.utilities.calvinlogger import get_logger
import time
from calvin.calvinsys.media.calvinpicamera import CalvinPiCamera
_log = get_logger(__name__)

class FacebookAlarm(Actor):
    """
    Detect faces in a jpg-image

    Outputs:
        faces: non-zero if face detected
    """

    def init(self, delay=1.5):
        self.delay = delay
        self.use('calvinsys.events.timer', shorthand='timer')
        self.timer = None
        self.setup()

    def setup(self):
        self.timer = self['timer'].repeat(self.delay)
        self.use("calvinsys.media.image", shorthand="image")
        self.use("'calvinsys.web.facebook'", shorthand="facebook")
        self.use("'calvinsys.media.calvinpicamera'", shorthand="picamera")
        self.image = self["image"]
        self.picture = None
        time.sleep(self.delay)
        _log.info('Completed setup')

    def did_migrate(self):
        self.setup()

    @condition([], ['faces'])
    @guard(lambda self: self.picture)
    def detect(self):
        pict = open(self.picture)
        found = self.image.detect_face(pict.read())
        _log.info('From FaceDetect found = %s' % found)

        if found:
            _log.info('Posting on user wall')
            self['facebook'].post_picture({'picture' : self.picture, 'message' :'Hey look who \'s there'})

        time.sleep(self.delay)
        self.picture = None
        return ActionResult(production=(self.picture, ))

    @condition([], [])
    @guard(lambda self: self.picture is None)
    def take_picture(self):
        _log.info('Taking a picture')
        self.picture = self['picamera'].get_picture()
        time.sleep(self.delay)
        return ActionResult()

    action_priority = (take_picture, detect )
    requires = ['calvinsys.media.image', 'calvinsys.web.facebook', 'calvinsys.media.calvinpicamera']
