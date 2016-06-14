from calvin.calvinsys.integration.nest import LogInException, NotFoundException
from calvin.runtime.north.plugins.nest import Nest
from calvin.utilities.calvinlogger import get_logger
from calvin.runtime.south.plugins.async.twistedimpl import  threads

_log = get_logger(__name__)


class NestIntegrationAsync(object):

    def __init__(self, node, actor):
        self.nest = None
        self._node = node
        self._actore = actor
        self.isLogged = None
        self.data = None
        self._in_progress = None

        try:
            credentials = self._node.attributes.get_private("/web/nest.com")
        except Exception as e:
            _log.error("Credentials not accessible. Error message %s" % e.message)
            credentials = None

        if credentials:
            self._in_progress = threads.defer_to_thread(self.login,credentials['username'], credentials['password'])
            self._in_progress.addCallback(self._post_login)
            self._in_progress.addErrback(self._err_login)

        else:
            _log.warning("Expected credentials /private/web/nest.com not found")
            self.nest = None

    def _post_login(self,*args, **kwargs):
        self._in_progress = None
        (res,) = args
        self.isLogged = res

        if self.isLogged:
            _log.info("Successfully logged in into Nest.com")
            #get update values each 2 seconds (it requires to renew the login, change this value carefully
            self.nest._cache_ttl = 20
        else:
            _log.info("Authentication failed. Check username and password")

    def _err_login(self, *args, **kwargs):
         _log.error("%r %r" % (args, kwargs))
         self._in_progress = None
         self.isLogged = False

    def login(self, username, password):
        """
        Authentication to the Nest service
        Args:
            username:
            password:

        Returns: False if authentication fails, True otherwise

        """
        login_success = False
        try:
            self.nest = Nest(username, password)
            self.check_login()
            login_success = True

        except Exception, ex:
            _log.error(ex.message)
        return login_success

    def check_login(self):

        """
        Checks if the user credentials are correct. Using this library is necessary to execute a query
        to get any authentication results
        Returns:

        """
        if self.nest is None:
            raise LogInException("Log in before attempting any operation!")
        try:
            self.nest.structures
        except Exception:
            raise LogInException("Wrong credentials! Check username and password")

    def err_callback(self, *args, **kwargs):
        self._in_progress = None

    def post_callback(self, *args, **kwargs):
        self._in_progress = None


    def _lift_structures(self):
        self.check_login()
        self.data = self.nest.structures

    def list_structures(self):

        if not self._in_progress:
            self.data = None
            self._in_progress = threads.defer_to_thread(self._lift_structures)
            self._in_progress.addErrback(self.err_callback)
            self._in_progress.addCallback(self.post_callback())

        else:
            _log.info("Task is already busy")

    def _list_devices(self):

        self.check_login()
        complete_list = [self.nest.devices, self.nest.protectdevices, self.nest.cameradevices]
        self.data = reduce(lambda first,second: first + second, complete_list)

    def list_devices(self):
        if not self._in_progress:
            self.data = None
            self._in_progress = threads.defer_to_thread(self._list_devices)
            self._in_progress.addErrback(self.err_callback)
            self._in_progress.addCallback(self.post_callback())
        else:
            _log.info("Task is already busy")

    def _list_devices_by_structure(self, structure_name):

        """
        Lists the devices in the given structure
        Args:
            structure_name:

        Returns: the list of devices related to that structure

        """
        self.check_login()
        structure = self.get_structure_by_name(structure_name)

        if structure is None:
            raise NotFoundException("Structure with %s name does not exist" % structure_name)
        complete_list = [structure.devices, structure.protectdevices, structure.cameradevices]
        self.data = reduce(lambda first,second: first + second, complete_list)

    def list_devices_by_structure(self, structure_name):
        if not self._in_progress:
            self.data = None
            self._in_progress = threads.defer_to_thread(self._list_devices_by_structure, structure_name = structure_name)
            self._in_progress.addErrback(self.err_callback)
            self._in_progress.addCallback(self.post_callback())
        else:
            _log.info("Task is already busy")


    def _get_structure_by_name(self, structure_name):

        """
        Args:
            structure_name: the name of the selected structure

        Returns: a list with all the structures which matches that name

        """
        self.check_login()
        res = filter(lambda item: item.name == structure_name, self.nest.structures)
        self.data = next(iter(res), None)

    def get_structure_by_name(self, structure_name):
        if not self._in_progress:
            self.data = None
            self._in_progress = threads.defer_to_thread(self._get_structure_by_name, structure_name = structure_name)
            self._in_progress.addErrback(self.err_callback)
            self._in_progress.addCallback(self.post_callback())
        else:
            _log.info("Task is already busy")

    def _get_device_by_name(self,deviceID):

        """
        Lookup with a device given its name
        Args:
            deviceID: the device name

        Returns: the managed object linked to the name or None if it doesn't exist

        """
        self.check_login()
        res = filter(lambda device: device.name == deviceID, self.nest.devices)
        self.data = next(iter(res), None)

    def get_device_by_name(self, deviceID):
        if not self._in_progress:
            self.data = None
            self._in_progress = threads.defer_to_thread(self._get_device_by_name, deviceID = deviceID)
            self._in_progress.addErrback(self.err_callback)
            self._in_progress.addCallback(self.post_callback())
        else:
            _log.info("Task is already busy")

    def _get_property(self, deviceID, property_name):

        """
        read property device given property and device names
        Args:
            deviceID:
            property_name:

        Returns: the value of that property or raise an exception otherwise

        """
        self.check_login()
        device = self.get_device_by_name(deviceID)

        if device is None:
            raise NotFoundException("Device with %s name does not exist!" % deviceID)
        self.data = device.__getattribute__(property_name)

    def get_property(self, deviceID, property_name):
        if not self._in_progress:
            self.data = None
            self._in_progress = threads.defer_to_thread(self._get_property, deviceID = deviceID, property_name = property_name)
            self._in_progress.addErrback(self.err_callback)
            self._in_progress.addCallback(self.post_callback())
        else:
            _log.info("Task is already busy")


    def _set_property(self, deviceID, property_name, value):
        """
        Set the property of a device given its identifier

        Args:
            deviceID: device identifier
            property_name: the property name to set
            value: the value for the property to be set

        Returns:
            True if the operation succeeds
            NotFoundException if the device name is not found
            AttributeError if the property doesn't exists
        """
        self.check_login()
        device = self.get_device_by_name(deviceID)

        if device is None:
            raise NotFoundException("Device with %s name does not exist!" % deviceID)
        device.__setattr__(property_name, value)
        self.data = True

    def set_property(self, deviceID, property_name, value):
        if not self._in_progress:
            self.data = None
            self._in_progress = threads.defer_to_thread(self._set_property, deviceID = deviceID, proprety_name = property_name, value = value)
            self._in_progress.addErrback(self.err_callback)
            self._in_progress.addCallback(self.post_callback())
        else:
            _log.info("Task is already busy")


def register(node, actor):
    return NestIntegrationAsync(node,actor)






