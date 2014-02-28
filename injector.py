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
    """ Checks to see if the graph contains any references to nodes that don't exist.

    dependency_graph - a graph of the form {name: [children names]}

    Returns True if there are missing dependencies.
    """
    for dependencies in dependency_graph.values():
        for dependency in dependencies:
            if dependency not in dependency_graph:
                return True
    return False

def has_circular_dependencies(dependency_graph):
    """ Checks to see if the graph contains any cycles.

    dependency_graph - a graph of the form {name: [children names]}

    Returns True if there is a cycle.
    """
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
    """ A factory for setting up and building an Injector instance.  """
    def __init__(self):
        self._factories = dict()

    def _add_item(self, kind, name, value, dependencies):
        self._names_used.add(name)

    def register_value(self, name, value):
        """ Bind a value to a name. The Injector will always return the value as-is.  """
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
        """ Builds an injector instance that can be used to inject dependencies.

        Also checks for common errors (missing dependencies and circular dependencies).
        """
        graph = self._make_dependency_graph()
        if has_missing_dependencies(graph):
            raise MissingDependencyException()
        if has_circular_dependencies(graph):
            raise CircularDependencyException()
        return Injector(self._factories)

class Injector(object):
    def __init__(self, factories):
        """ Create an Injector.

        The prefered way to create an Injector is with `Dependencies.build_injector()`.
        """
        self._factories = factories
        self._value_cache = {}

    def has_dependency(self, name):
        """ Check if the Injector has a dependency """
        return name in self._factories

    def get_dependency(self, name):
        """ Get the value of a dependency.

        name - The name of the requested dependency

        Returns the value of the dependency
        """
        if not self.has_dependency(name):
            raise MissingDependencyException("Missing dependency name: {}".format(name))
        if name not in self._value_cache:
            self._value_cache[name] = self.inject(*self._factories[name])
        return self._value_cache[name]

    def inject(self, fn, dependencies):
        """ Calls the function with the value of the listed dependencies

        fn           - function that will be called
        dependencies - list of names of dependencies to inject

        Returns the result of calling the function.
        """
        args = map(self.get_dependency, dependencies) if dependencies else []
        return fn(*args)
