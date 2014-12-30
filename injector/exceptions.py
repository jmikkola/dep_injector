class InjectorException(Exception):
    """ Base class for exceptions raised by the injector """
    pass

class BadNameException(InjectorException):
    """ Raised when an invalid name is used """
    pass

class DuplicateNameException(InjectorException):
    """ Raised when a duplicate name is used """
    pass

class MissingDependencyException(InjectorException):
    """ Raised when a requested dependency is not found """
    pass

class CircularDependencyException(InjectorException):
    """ Raised when the dependencies defined are circular """
    pass
