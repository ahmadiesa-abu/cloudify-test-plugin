from .service_manager import ServiceManager


class ServiceManagerFactory(object):
    service_manager = None

    @classmethod
    def get_service_manager(cls, server, username, password, skip_verification):
        cls.service_manager = ServiceManager(server,
                                             username,
                                             password,
                                             skip_verification)
        cls.service_manager.connect()
        return cls.service_manager

    @classmethod
    def disconnect(cls):
        if cls.service_manager:
            cls.service_manager.disconnect()


import atexit
atexit.register(ServiceManagerFactory.disconnect)