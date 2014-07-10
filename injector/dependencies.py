from injector import (
    exceptions,
    graph,
    injector,
)

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
        self._check_name(name)
        self._factories[name] = (factory, dependencies)

    def _check_name(self, name):
        if not name or not isinstance(name, str):
            raise exceptions.BadNameException("Bad name: {!r}".format(name))
        if name in self._factories:
            raise exceptions.DuplicateNameException("Duplicate name: {}".format(name))

    def _make_dependency_graph(self):
        return graph.DependencyGraph({
            name: dependencies or []
            for name, (_, dependencies) in self._factories.items()
        })

    def _check_injector_state(self):
        dependency_graph = self._make_dependency_graph()
        if dependency_graph.has_missing_dependencies():
            raise exceptions.MissingDependencyException()
        if dependency_graph.has_circular_dependencies():
            raise exceptions.CircularDependencyException()

    def build_injector(self):
        """ Builds an injector instance that can be used to inject dependencies.

        Also checks for common errors (missing dependencies and circular dependencies).
        """
        self._check_injector_state()
        return injector.Injector(self._factories)
