#!/usr/bin/env python

import unittest

import injector

class InjectorTest(unittest.TestCase):
    def setUp(self):
        self.injector = injector.Injector()

    def test_can_add_things(self):
        self.injector.register_value('my value', 123)
        self.injector.register_factory('my factory', lambda: 1)
        self.injector.register_service('my service', lambda: 1)

    def test_accepts_dependency_lists(self):
        self.injector.register_value('my value', 123, dependencies=['my factory'])
        self.injector.register_factory('my factory', lambda: 1, dependencies=['my value'])
        self.injector.register_service('my service', lambda: 1, dependencies=['my value'])

    def test_requires_names(self):
        with self.assertRaises(injector.BadNameException):
            self.injector.register_value(None, 123)
        with self.assertRaises(injector.BadNameException):
            self.injector.register_value(123, 123)
        with self.assertRaises(injector.BadNameException):
            self.injector.register_value(object(), 123)

if __name__ == '__main__':
    unittest.main()
