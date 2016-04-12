from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)


class NestStructure(Actor):
    """
    Calvin Actor which acts as a Nest Structure. Possible operations (at the moment):
        -List all devices
        ... more coming!

    Inputs:
        trigger: run the evaluation

    Outputs:
        devices: the list of the devices available in the structure
    """

    @manage(['structure_name'])
    def init(self, structure_name):
        self.structure_name = structure_name
        self.trigger = None
        self.setup()

    def setup(self):
        self.use('calvinsys.integration.nest', shorthand='nest')
        #get update values each 2 seconds (it requires to renew the login, change this value carefully
        self['nest'].nest._cache_ttl = 20
        self.structure = self['nest'].get_structure_by_name(self.structure_name)

    def did_migrate(self):
        self.setup()

    @condition(action_input=['trigger'], action_output=[])
    @guard(lambda self, trigger: self.trigger is None)
    def trigger(self, trigger):
        self.trigger = True
        return ActionResult()

    @condition([], ['devices'])
    @guard(lambda self: self.structure is not None and self.trigger is True)
    def get_devices(self):
        res = self['nest'].list_devices_by_structure(self.structure_name)
        self.trigger = None
        return ActionResult(production=(res,))

    action_priority = (trigger, get_devices)
    requires = ['calvinsys.integration.nest']
