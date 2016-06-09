from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.utilities.calvinlogger import get_logger
import base64
import random
import os
import json

_log = get_logger(__name__)

#[TODO] implement model insertion
class SpeakerVerification(Actor):

    """
    Verify who is speaking in a wav file (recommended frequency 48 kHz)

    Input:
      wav : wav file
      model: the person to look for
      operation: the operation to perform (add or identify a model)
    Output:
      likelihood: the likelihood for the model match (only for identify), otherwise the result of the adding operation
      match: yes or no
    """
    @manage()
    def init(self):
        self.wav = None
        self.extracted = None
        self.model = None
        self.setup()

    def setup(self):
        self.use('calvinsys.mlearning.speaker_verification', shorthand='rec')
        self.recognizer = self['rec']

    @condition(action_input=['wav'])
    @guard(lambda self, wav: self.wav is None and self.model is None)
    def new_recording(self, wav):
        _log.info("Received file")
        js = json.loads(wav)
        newfile = open('temp-{0}.wav'.format(random.randint(1,100)), 'w')
        newfile.write(base64.b64decode(js['base64_string']))
        newfile.close()
        self.wav = newfile.name
        return ActionResult()

    @condition(action_input=['operation'])
    def set_operation(self,operation):
        self.operation = operation
        return ActionResult()

    @condition(action_input=['model'])
    @guard(lambda self, model: self.wav is not None and not self.extracted)
    def run_identification(self, model):
        _log.info("Starting extraction")
        self.model = model
        self['rec'].verify_identity(model,"{0}/{1}".format(os.getcwd(),self.wav))
        self.extracted = True
        return ActionResult()

    @condition(action_output=['match','likelihood'])
    @guard(lambda self: self.wav is not None and self['rec']._in_progress == None and self.extracted)
    def identification(self):
        _log.info("Extraction completed")
        res = self['rec'].result
        _log.info("Res: {0}".format(res))
        os.remove(self.wav)
        self.wav = None
        self.extracted = None
        return ActionResult(production=(res['match'], res['likelihood'], ))


    action_priority = (new_recording, run_identification, identification )
    requires = ['calvinsys.mlearning.speaker_recognition']