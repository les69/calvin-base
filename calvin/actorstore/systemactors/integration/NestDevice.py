from calvin.actor.actor import Actor, ActionResult, manage, condition, guard
from calvin.utilities.calvinlogger import get_logger
import time

_log = get_logger(__name__)


class NestDevice(Actor):
    """
    Calvin Actor which acts as a Nest Device. Possible operations (at the moment):
        -Read property
        -Write property
        ... more coming!

    Inputs:
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
        self.time_start = None
        self.started = None
        self.setup()

    def setup(self):
        self.use('calvinsys.integration.nest_async', shorthand='nest')
        self.nest = self['nest']


    def did_migrate(self):
        self.setup()

    @condition(action_input=['operation'], action_output=[])
    def set_operation(self, operation):
        self.operation = operation
        return ActionResult()

    @condition(['device', 'property_name', 'value'], [])
    @guard(lambda self, device, property_name, value: self.nest._in_progress is None and self.operation == "set")
    def set_property(self, device, property_name, value):
        self['nest'].set_property(device, property_name, value)
        self.operation = None
        return ActionResult()

    @condition(['device', 'property_name'], [])
    @guard(lambda self, device, property_name: self.operation == "get" and self.started is None)
    def get_property(self, device, property_name):
        _log.info("Reading property %s from device %s" % (property_name, device))
        self['nest'].get_property(device, property_name)
        self.operation = None
        self.started = True
        return ActionResult()

    @condition(action_output=['result'])
    @guard(lambda self, device, property_name: self['nest']._in_progress is None and self.operation == "get" and self.data is not None)
    def return_value(self):
        res = self['nest'].data
        return ActionResult(production=(res,))





    action_priority = (set_operation, set_property, get_property)
    requires = ['calvinsys.integration.nest']
