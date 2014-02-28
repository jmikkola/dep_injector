#!/usr/bin/env python

import unittest

import injector

class DependenciesTest(unittest.TestCase):
    def setUp(self):
        self.injector = injector.Dependencies()

    def test_can_add_things(self):
        self.injector.register_value('my value', 123)
        self.injector.register_factory('my factory', lambda: 1)

    def test_accepts_dependency_lists(self):
        self.injector.register_factory('my factory', lambda: 1, dependencies=['my value'])

    def test_requires_names(self):
        with self.assertRaises(injector.BadNameException):
            self.injector.register_value(None, 123)
        with self.assertRaises(injector.BadNameException):
            self.injector.register_value(123, 123)
        with self.assertRaises(injector.BadNameException):
            self.injector.register_value(object(), 123)

    def test_disallows_duplicate_names(self):
        self.injector.register_value('x', 1)
        with self.assertRaises(injector.DuplicateNameException):
            self.injector.register_factory('x', lambda: 2)

if __name__ == '__main__':
    unittest.main()
