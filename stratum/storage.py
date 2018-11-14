from builtins import str
from builtins import object

class Storage(object):

    def __init__(self):
        self.__services = {}
        self.session = None

    def get(self, service_type, vendor, default_object):
        self.__services.setdefault(service_type, {})
        self.__services[service_type].setdefault(vendor, default_object)
        return self.__services[service_type][vendor]

    def __repr__(self):
        return str(self.__services)
