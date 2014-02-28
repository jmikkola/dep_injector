import collections

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

def has_missing_dependencies(dependency_graph):
    for dependencies in dependency_graph.values():
        for dependency in dependencies:
            if dependency not in dependency_graph:
                return True
    return False

def has_circular_dependencies(dependency_graph):
    dep_counts = {
        name: len(dependencies)
        for name, dependencies in dependency_graph.items()
    }

    depends_on = collections.defaultdict(set)
    for name, dependencies in dependency_graph.items():
        for dependency in dependencies:
            depends_on[dependency].add(name)

    deps_met = collections.deque(
        name for name, dependencies in dependency_graph.items()
        if len(dependencies) == 0
    )

    num_removed = 0
    while deps_met:
        num_removed += 1
        done = deps_met.pop()
        for name in depends_on[done]:
            dep_counts[name] -= 1
            if dep_counts[name] == 0:
                deps_met.add(name)

    return num_removed < len(dependency_graph)

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
        if has_circular_dependencies(graph):
            raise CircularDependencyException()
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
