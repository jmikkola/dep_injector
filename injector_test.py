#!/usr/bin/env python3

import unittest

import injector

class DependenciesTest(unittest.TestCase):
    def setUp(self):
        self.dependencies = injector.Dependencies()

    def test_can_add_things(self):
        self.dependencies.register_value('my value', 123)
        self.dependencies.register_factory('my factory', lambda: 1)

    def test_accepts_dependency_lists(self):
        self.dependencies.register_factory(
            'my factory', lambda: 1, dependencies=['my value']
        )

    def test_requires_names(self):
        with self.assertRaises(injector.BadNameException):
            self.dependencies.register_value(None, 123)
        with self.assertRaises(injector.BadNameException):
            self.dependencies.register_value(123, 123)
        with self.assertRaises(injector.BadNameException):
            self.dependencies.register_value(object(), 123)

    def test_disallows_duplicate_names(self):
        self.dependencies.register_value('x', 1)
        with self.assertRaises(injector.DuplicateNameException):
            self.dependencies.register_factory('x', lambda: 2)

    def test_builds_injector(self):
        self.dependencies.register_value('x1', 1)
        inj = self.dependencies.build_injector()

        self.assertEqual(inj.get_dependency('x1'), 1)

    def test_catches_missing_dependency(self):
        self.dependencies.register_factory('f1', lambda f2: 1, dependencies=['f2'])

        with self.assertRaises(injector.MissingDependencyException):
            self.dependencies.build_injector()

    def test_catches_circular_dependency(self):
        self.dependencies.register_factory('f1', lambda f2: 1, dependencies=['f2'])
        self.dependencies.register_factory('f2', lambda f3: 2, dependencies=['f3'])
        self.dependencies.register_factory('f3', lambda f1: 3, dependencies=['f1'])

        with self.assertRaises(injector.CircularDependencyException):
            self.dependencies.build_injector()

class InjectorTest(unittest.TestCase):
    def setUp(self):
        self.injector = injector.Injector({})

if __name__ == '__main__':
    unittest.main()
