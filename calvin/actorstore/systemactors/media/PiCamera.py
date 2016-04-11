from calvin.actor.actor import Actor, ActionResult, manage, condition, guard


class PiCamera(Actor):

    """
    When input trigger goes high fetch image from given device.

    Inputs:
      trigger: binary input
    Outputs:
      image: generated image
    """

    @manage([])
    def init(self):
        self.setup()

    def setup(self):
        self.use("calvinsys.media.calvinpicamera", shorthand="picamera")

    def did_migrate(self):
        self.setup()

    @condition(action_input=['trigger'], action_output=['image', 'picture'])
    @guard(lambda self, trigger : trigger)
    def get_image(self, trigger):
        #image = self['picamera'].get_picture_stream()
        image = self['picamera'].get_picture()
        stream = open(image,'r').read()
        return ActionResult(production=(stream, image ))

    @condition(action_input=['trigger'])
    def empty(self, trigger):
        return ActionResult()

    action_priority = (get_image, empty)
    requires =  ["calvinsys.media.calvinpicamera"]
