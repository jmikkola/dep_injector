from __future__ import absolute_import

from injector.exceptions import MissingDependencyException

class Injector(object):
    """ An injector filled with dependencies, ready to inject. """

    def __init__(self, factories):
        """ Create an Injector.

        The prefered way to create an Injector is with `Dependencies.build_injector()`.

        :param factories: A dict of the form {name: (factory fn, [dependency name])}
        """
        self._factories = factories
        self._value_cache = {}

    def has_dependency(self, name):
        """ Check if the Injector has a dependency.

        :param name: The name of the dependency
        :return: True if this provides that dependency
        """
        return name in self._factories

    def get_dependency(self, name):
        """ Get the value of a dependency.

        :param name: The name of the dependency
        :return: the value of the dependency
        """
        if not self.has_dependency(name):
            raise MissingDependencyException("Missing dependency name: {}".format(name))
        if name not in self._value_cache:
            self._value_cache[name] = self.inject(*self._factories[name])
        return self._value_cache[name]

    def inject(self, function, dependencies):
        """ Calls the function with the value of the listed dependencies.

        :param function: The function that will be called
        :param dependencies: A list of names of dependencies to inject into the function
        :return: The result of calling the function.
        """
        args = [self.get_dependency(d) for d in dependencies] if dependencies else []
        return function(*args) #pylint: disable=W0142
