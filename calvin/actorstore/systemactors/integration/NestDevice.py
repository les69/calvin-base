from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)


class NestDevice(Actor):
    """
    Calvin Actor which acts as a Nest Device. Possible operations (at the moment):
        -Read property
        -Write property
        ... more coming!

    Inputs:
        trigger: run the evaluation
        device: the device identifier
        operation: string representing the operation to do (get or set)
        property_name: the property to be get/set
        value: the value to be used to set the property
    Outputs:
        result: the property value
    """

    @manage()
    def init(self):
        self.operation = None
        self.trigger = None
        self.setup()

    def setup(self):
        self.use('calvinsys.integration.nest', shorthand='nest')
        self['nest'].nest._cache_ttl = 20

    def did_migrate(self):
        self.setup()

    @condition(action_input=['operation'], action_output=[])
    def set_operation(self, operation):
        self.operation = operation
        return ActionResult()

    @condition(action_input=['trigger'], action_output=[])
    @guard(lambda self, trigger: self.trigger is None)
    def trigger(self, trigger):
        self.trigger = True
        return ActionResult()

    @condition(['device', 'property_name', 'value'], [])
    @guard(lambda self, device, property_name, value: self.operation == "set" and self.trigger is True)
    def set_property(self, device, property_name, value):
        self['nest'].set_property(device, property_name, value)
        self.trigger = None
        return ActionResult()

    @condition(['device', 'property_name'], ['result'])
    @guard(lambda self, device, property_name: self.operation == "get" and self.trigger is True)
    def get_property(self, device, property_name):
        _log.info("Reading property %s from device %s" % (property_name, device))
        res = self['nest'].get_property(device, property_name)
        self.trigger = None
        return ActionResult(production=(res,))

    action_priority = (trigger, set_operation, set_property, get_property)
    requires = ['calvinsys.integration.nest']
