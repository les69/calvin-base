from calvin.runtime.south.plugins.machine_learning.speaker_recognition.speaker_rec import verify_model, add_model
from calvin.utilities.calvinlogger import get_logger
from calvin.runtime.south.plugins.async.twistedimpl import async, threads

_log = get_logger(__name__)


class SpeakerVerification(object):

    def __init__(self):
        self._in_progress = None
        self.result = None

    def cb_post_verify_identity(self, *args, **kwargs):
        _log.info("{0} {1}".format(args, kwargs))
        self._in_progress = None

    def cb_error_verify_identity(self, *args, **kwargs):
        _log.info("{0} {1}".format(args, kwargs))
        self._in_progress = None

    def _verify_identity(self, model_name, file_path):
        _log.info("Entering verification")
        self.result = verify_model(model_name, file_path)

    def verify_identity(self, model, file):
        _log.info("Started verification")
        self.result = None
        if not file.__contains__(".wav"):
            raise Exception("File nor supported")

        if self._in_progress is None:
            _log.info("Deferring to threead")
            self._in_progress = threads.defer_to_thread(self._verify_identity, model_name=model, file_path=file)
            _log.info("Deferring completed")
            self._in_progress.addCallback(self.cb_post_verify_identity)
            self._in_progress.addErrback(self.cb_error_verify_identity)
        else:
            _log.info("Process already running")


def register(node= None, actor= None):
    return SpeakerVerification()