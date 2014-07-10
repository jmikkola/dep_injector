from injector.exceptions import MissingDependencyException

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
