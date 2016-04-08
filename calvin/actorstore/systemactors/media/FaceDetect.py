from calvin.actor.actor import Actor, ActionResult, condition
from calvin.utilities.calvinlogger import get_logger
from calvin.utilities.utils import absolute_filename
_log = get_logger(__name__)

class FaceDetect(Actor) :
    """
    Detect faces in a jpg-image

    Inputs:
        image: Image to analyze
    Outputs:
        faces: non-zero if face detected
    """

    def init(self):
        self.setup()

    def setup(self):
        self.use("calvinsys.media.image", shorthand="image")
        self.image = self["image"]

    def did_migrate(self):
        self.setup()

    @condition(['image'], ['faces'])
    def detect(self, image):
        found = self.image.detect_face(image)
        _log.info('From FaceDetect found = %s' % found)
        return ActionResult(production=(found, ))

    action_priority = (detect, )
    requires =  ['calvinsys.media.image']
