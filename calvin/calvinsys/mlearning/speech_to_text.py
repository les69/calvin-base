from calvin.utilities.calvinlogger import get_logger
from calvin.runtime.south.plugins.async.twistedimpl import async, threads
import speech_recognition as sr
_log = get_logger(__name__)

class SpeechToText(object):

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.in_progress = None
        self.text = None

    def cb_post_textify(self, *args, **kwargs):
        _log.info("{0} {1}".format(args, kwargs))
        self.in_progress = None

    def cb_error_textify(self, *args, **kwargs):
        _log.info("{0} {1}".format(args, kwargs))
        self.in_progress = None

    def _textify(self, audio):

        with sr.AudioFile(audio) as source:
            audio_obj = self.recognizer.record(source)
        self.text = self.recognizer.recognize_google(audio_obj)

    def textify(self, file):
        if self.in_progress is not None:
            _log.error("Process is already running")
            return
        self.text = None
        self.in_progress = threads.defer_to_thread(self._textify, audio = file)
        self.in_progress.addCallback(self.cb_post_textify)
        self.in_progress.addErrback((self.cb_error_textify))

def register(node= None, actor= None):
    return SpeechToText()