class InjectorException(Exception):
    pass

class BadNameException(InjectorException):
    pass

class DuplicateNameException(InjectorException):
    pass

class MissingDependencyException(InjectorException):
    pass

def has_missing_dependencies(dependency_graph):
    for dependencies in dependency_graph.values():
        for dependency in dependencies:
            if dependency not in dependency_graph:
                return True
    return False

class Dependencies(object):
    def __init__(self):
        self._factories = dict()

    def _add_item(self, kind, name, value, dependencies):
        self._names_used.add(name)

    def register_value(self, name, value):
        """ Bind a value to a name. The Injector will always return the value as-is.
        """
        self.register_factory(name, lambda: value)

    def register_factory(self, name, factory, dependencies=None):
        """ Binds a factory to a name. The injector will call the factory function once
        (if the name is ever used), and always return the value that the factory returns.

        The factory will be called with the dependencies (if any listed) as arguments.
        """
        if not name or not isinstance(name, str):
            raise BadNameException("Bad name: {!r}".format(name))
        if name in self._factories:
            raise DuplicateNameException("Duplicate name: {}".format(name))

        self._factories[name] = (factory, dependencies)

    def _make_dependency_graph(self):
        return {
            name: dependencies or []
            for name, (_, dependencies) in self._factories.items()
        }

    def build_injector(self):
        graph = self._make_dependency_graph()
        if has_missing_dependencies(graph):
            raise MissingDependencyException()
        return Injector(self._factories)

class Injector(object):
    def __init__(self, factories):
        self._factories = factories
        self._value_cache = {}

    def get_dependency(self, name):
        if name not in self._factories:
            raise MissingDependencyException("Missing dependency name: {}".format(name))
        (factory, dependencies) = self._factories[name]
        args = []
        return factory(*args)
