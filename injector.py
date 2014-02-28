class InjectorException(Exception):
    pass

class BadNameException(InjectorException):
    pass

class DuplicateNameException(InjectorException):
    pass

class Dependencies(object):
    def __init__(self):
        self._names_used = set()

    def _add_item(self, kind, name, value, dependencies):
        if not name or not isinstance(name, str):
            raise BadNameException("Bad name: {!r}".format(name))
        if name in self._names_used:
            raise DuplicateNameException("Duplicate name: {}".format(name))
        self._names_used.add(name)

    def register_value(self, name, value):
        """ Bind a value to a name. The Injector will always return the value as-is.
        """
        self._add_item('value', name, value, None)

    def register_factory(self, name, factory, dependencies=None):
        """ Binds a factory to a name. The injector will call the factory function once
        (if the name is ever used), and always return the value that the factory returns.

        The factory will be called with the dependencies (if any listed) as arguments.
        """
        self._add_item('factory', name, factory, dependencies)
