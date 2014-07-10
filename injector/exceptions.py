class InjectorException(Exception):
    pass

class BadNameException(InjectorException):
    pass

class DuplicateNameException(InjectorException):
    pass

class MissingDependencyException(InjectorException):
    pass

class CircularDependencyException(InjectorException):
    pass
