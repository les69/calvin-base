import nest

from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)

class LogInException(Exception):

    """
    Just a simple custom exception for the class below
    """
    def __init__(self, message):
        self.message = message

class NotFoundException(Exception):

    """
    Just a simple custom exception for the class below
    """
    def __init__(self, message):
        self.message = message


class NestIntegration(object):

    def __init__(self):
        self.nest = None

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
            self.nest = nest.Nest(username, password)
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


    def list_structures(self):

        """
        Lists all structures owned by the current user
        Returns: a list of structures

        """
        self.check_login()
        return self.nest.structures

    def get_structure_by_name(self, structure_name):

        """
        Args:
            structure_name: the name of the selected structure

        Returns: a list with all the structures which matches that name

        """
        self.check_login()
        return filter(lambda item: item.name == structure_name, self.nest.structures)

    def get_device_by_name(self,deviceID):

        """
        Lookup with a device given its name
        Args:
            deviceID: the device name

        Returns: the managed object linked to the name or None if it doesn't exist

        """
        self.check_login()
        res = filter(lambda device: device.name == deviceID, self.nest.devices)
        return next(iter(res), None)

    def get_property(self,deviceID, proprety_name):

        """
        read property device given property and device names
        Args:
            deviceID:
            proprety_name:

        Returns: the value of that property or raise an exception otherwise

        """
        self.check_login()
        device = self.get_device_by_name(deviceID)

        try:
            if device is None:
                raise NotFoundException("Device name does not exist!")
            return device.__getattribute__(proprety_name)
        except Exception, ex:
            _log.error(ex.message)






