from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)

class SpeechToText(Actor):

    """
    Verify who is speaking in a wav file (recommended frequency 48 kHz)

    Input:
      audio : audio filepath
    Output:
      text: the text extracted from the audio
    """
    @manage()
    def init(self):
        self.audio = None
        self.setup()

    def setup(self):
        self.use('calvinsys.mlearning.speech_to_text', shorthand='speech')

    @condition(action_input=['audio'])
    @guard(lambda self, audio: self.audio is None)
    def add_file(self, audio):
        _log.info("Received file")
        self.audio = audio
        self['speech'].textify(audio)
        return ActionResult()

    @condition(action_output=['text'])
    @guard(lambda self: self.audio is not None and self['speech'].text is not None)
    def extract_text(self):
        _log.info("Extraction completed")
        res = self['speech'].text
        _log.info("Res: {0}".format(res))
        self.audio = None
        return ActionResult(production=(res, ))

    action_priority = (add_file, extract_text)
    requires = ['calvinsys.mlearning.speech_to_text']