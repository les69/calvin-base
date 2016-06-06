from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.utilities.calvinlogger import get_logger
import base64
import json
_log = get_logger(__name__)


class TestRec(Actor):

    """
    Get contents of URL

    Input:
      token : token
    Output:
      file: JSON dictionary
    """
    @manage()
    def init(self):
        self.token = None
        self.setup()

    def setup(self):
        pass


    @condition(action_input=['token'])
    @guard(lambda self, token: self.token is None)
    def start(self, token):
        self.token = token
        return ActionResult()

    @condition(action_output=['file'])
    @guard(lambda self: self.token is not None)
    def read_file(self):
        file = open('mirko-3.wav')
        encoded_string = base64.b64encode(file.read())

        js = json.dumps({'base64_string' : encoded_string})
        self.token = None
        return ActionResult(production=(js, ))


    action_priority = (start, read_file)
