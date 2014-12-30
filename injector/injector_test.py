#!/usr/bin/env python

from __future__ import absolute_import
import unittest

from injector import exceptions
from injector.injector import Injector

class InjectorTest(unittest.TestCase):
    def setUp(self):
        self.injector = Injector({
            'value1': (lambda: 1, None),
            'value2': (lambda: 'some string', None),
            'factory1': (lambda: 'factory 1 result', None),
            'factory2': (lambda val1: 'value1 is {}'.format(val1), ['value1']),
        })

    def test_has_dependency(self):
        self.assertTrue(self.injector.has_dependency('value1'))
        self.assertFalse(self.injector.has_dependency('xyz'))

    def test_get_value(self):
        self.assertEqual(1, self.injector.get_dependency('value1'))
        self.assertEqual('some string', self.injector.get_dependency('value2'))

    def test_get_factory(self):
        self.assertEqual('factory 1 result', self.injector.get_dependency('factory1'))

    def test_get_factory_with_dependencies(self):
        self.assertEqual('value1 is 1', self.injector.get_dependency('factory2'))

    def test_get_missing_dependency(self):
        with self.assertRaises(exceptions.MissingDependencyException):
            self.injector.get_dependency('missing!')

    def test_inject(self):
        def test_fn(a, b):
            return '{} {}'.format(a, b)
        result = self.injector.inject(test_fn, ['value1', 'value2'])
        self.assertEqual('1 some string', result)

if __name__ == '__main__':
    unittest.main()
