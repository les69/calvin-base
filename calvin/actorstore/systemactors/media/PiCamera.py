from calvin.actor.actor import Actor, ActionResult, manage, condition, guard


class PiCamera(Actor):

    """
    When input trigger goes high fetch image from given device.

    Inputs:
      trigger: binary input
    Outputs:
      stream: image stream
      image: generated image file

    """

    @manage([])
    def init(self):
        self.setup()

    def setup(self):
        self.use("calvinsys.media.calvinpicamera", shorthand="picamera")
        self.camera = self['picamera']
        self.image = None

    def did_migrate(self):
        self.setup()

    @condition(action_input=[], action_output=['stream', 'image'])
    @guard(lambda self: self.image is not None and self.camera.picture_taken is True)
    def get_image(self):
        stream = open(self.image, 'r').read()
        image = self.image
        self.image = None
        return ActionResult(production=(stream, image))

    @condition(action_input=['trigger'], action_output=[])
    @guard(lambda self, trigger : trigger)
    def take_picture(self, trigger):
        self.image = self['picamera'].get_picture()
        return ActionResult()


    action_priority = (take_picture, get_image)
    requires =  ["calvinsys.media.calvinpicamera"]
