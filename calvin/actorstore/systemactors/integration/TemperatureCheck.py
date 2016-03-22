from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.runtime.north.plugins.coders.integration.nest_integration import NestIntegration
import time
import json as js
from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)

def absolute_filename(filename):
    """Test helper - get absolute name of file
    @TODO: Possibly not the best way of doing this
    """
    import os.path
    return os.path.join(os.path.dirname(__file__), filename)


class TemperatureCheck(Actor):

    """
    After first token, pass on token once every 'delay' seconds.
    Inputs:
        device: the device name
    Outputs:
        alert: alert message if temperature is too high
    """

    @manage()
    def init(self):
        self.delay = 5
        _log.info("Operation started")
        self.device = None
        self.use('calvinsys.events.timer', shorthand='timer')
        self.nest = NestIntegration()
        self.temperature = None
        self.alarm = False
        self.isLogged = False
        self.setup()

    def read_credentials(self, filename):
        json_content =open(absolute_filename(filename)).read()
        json = js.loads(json_content)
        return (json['user'], json['pass'])

    def setup(self):
        (user, password) = self.read_credentials('config')
        self.isLogged = self.nest.login(user, password)
        if self.isLogged:
            self.nest.nest._cache_ttl = 20 #Force refresh after few seconds
            _log.info("Log in successful")
        self.timer = self['timer'].repeat(self.delay)

    def will_migrate(self):
        self.timer.cancel()

    def did_migrate(self):
        self.setup()


    @condition(['device'], [])
    def set_device(self, device):
        self.device = device
        return ActionResult()

    @condition([], [])
    @guard(lambda self: self.isLogged and self.device and not self.alarm)
    def wait_and_read(self):
        self.temperature = self.nest.get_property(self.device, 'temperature')

        if self.temperature > 25:
            self.alarm = True
            _log.info("Alarm set")
        else:
            _log.info("Temperature ok")

        time.sleep(self.delay)
        return ActionResult()

    @condition([], ['alert'])
    @guard(lambda self: self.isLogged and self.alarm)
    def send_alarm(self):
        self.alarm = False
        _log.info("Alarm message sent")

        return ActionResult(production=("temperature too high",))

    action_priority = (set_device, wait_and_read, send_alarm)