from voiceid.db import GMMVoiceDB
from voiceid.sr import Voiceid
from calvin.runtime.south.plugins.async.twistedimpl import async, threads
from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)

db_name = 'voices/models'


class SpeakerRecognition(object):

    def __init__(self):
        self._in_progress = None
        self.db = GMMVoiceDB(db_name)
        self.voice = None

    def cb_post_add_voice(self, *args, **kwargs):
        #_log.info("{0} {1}".format(args, kwargs))
        self._in_progress = None

    def cb_error_add_voice(self, *args, **kwargs):
        #_log.info("{0} {1}".format(args, kwargs))
        self._in_progress = None

    def _add_voice(self, model_name, file):
        self.db.add_model(file, model_name)

    def add_voice(self, model_name, file):

        if file.__contains__('.wav'):
            file.replace('.wav','')
        self._in_progress = threads.defer_to_thread(10, self._add_voice, model_name =model_name, file=file)
        self._in_progress.addCallback(self.cb_post_add_voice)
        self._in_progress.addErrback(self.cb_error_add_voice)

    def _post_extract(self, *args, **kwargs):
        #_log.info("{0} {1}".format(args, kwargs))
        self._in_progress = None

    def _error_extract(self, *args, **kwargs):
        #_log.info("{0} {1}".format(args, kwargs))
        self._in_progress = None

    def _extract_speakers(self):
        self.voice.extract_speakers()

    def extract_speakers(self, file):
        self.voice = Voiceid(self.db, file)
        _log.info("Voice created {0}".format(self.voice))

        self._in_progress = threads.defer_to_thread(10, self._extract_speakers)
        self._in_progress.addCallback(self._post_extract)
        self._in_progress.addErrback(self._error_extract)

    def get_speakers(self):
        return self.voice.get_speakers_map()


def register(node= None, actor= None):
    return SpeakerRecognition()
