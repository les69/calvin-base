from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.utilities.calvinlogger import get_logger
import base64
import random
import os
import json

_log = get_logger(__name__)

#[TODO] rename in speaker diarization
class SpeakerIdentification(Actor):

    """
    efgpgpgmopg

    Input:
      wav : wav file
      operation: the operation to perform, either extract or add_model
      model_name: the name for the new model
    Output:
      n_people: people found
      names: dictionary of results
    """
    @manage()
    def init(self):
        self.wav = None
        self.extracted = None
        self.operation = None
        self.setup()

    def setup(self):
        self.use('calvinsys.mlearning.speaker_recognition', shorthand='rec')
        self.recognizer = self['rec']


    @condition(action_input=['operation'])
    @guard(lambda self, operation: self.operation == None and (operation == 'extract' or operation == 'add_model'))
    def set_operation(self, operation):
        self.operation = operation
        return ActionResult()

    @condition(action_input=['wav'])
    @guard(lambda self, wav: self.wav is None)
    def new_recording(self, wav):
        _log.info("Received file")
        js = json.loads(wav)
        newfile = open('temp-{0}.wav'.format(random.randint(1,100)), 'w')
        newfile.write(base64.b64decode(js['base64_string']))
        newfile.close()
        self.wav = newfile.name
        return ActionResult()

    @condition(action_input=['model_name'])
    @guard(lambda self, model_name: self.operation == 'add_model' and self.wav)
    def add_model(self, model_name):
        _log.info("Adding model {0}".format(model_name))
        self['rec'].add_voice(model_name, self.wav)
        self.operation = None
        self.wav = None
        return ActionResult()

    @condition()
    @guard(lambda self: self.operation == 'extract' and self.wav is not None and not self.extracted)
    def run_detection(self):
        _log.info("Starting extraction")
        import os
        self['rec'].extract_speakers("{0}/{1}".format(os.getcwd(),self.wav))
        self.extracted = True
        return ActionResult()

    @condition(action_output=['n_people','names'])
    @guard(lambda self: self.wav is not None and self.recognizer._in_progress == None and self.extracted)
    def return_speakers(self):
        _log.info("Extraction completed")
        res = self['rec'].get_speakers()
        _log.info("Res: {0}".format(res))
        os.remove(self.wav)
        self.wav = None
        self.operation = None
        self.extracted = None
        return ActionResult(production=(len(res.keys()), res, ))


    action_priority = (set_operation, add_model,new_recording, run_detection, return_speakers )
    requires = ['calvinsys.mlearning.speaker_recognition']