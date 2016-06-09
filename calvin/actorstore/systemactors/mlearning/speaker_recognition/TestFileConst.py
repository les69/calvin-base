from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.utilities.calvinlogger import get_logger
import base64
import json
_log = get_logger(__name__)


class TestFileConst(Actor):

    """
    Get contents of URL

    Input:
      token : token
    Output:
      file: path to file
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
    def file_string(self):
        file_path = "/Users/les/Virtualenvs/calvin/calvin-base/mirko-4.wav"
        self.token = None
        return ActionResult(production=(file_path, ))



    action_priority = (start, file_string)
