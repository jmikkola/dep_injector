#!/usr/bin/env python3

from __future__ import absolute_import
import unittest

from injector.graph import DependencyGraph

class MissingDependenciesTest(unittest.TestCase):
    def _assert_result_for_graph_is(self, result, graph):
        dependency_graph = DependencyGraph(graph)
        self.assertEqual(result, dependency_graph.has_missing_dependencies())

    def _assert_missing_dependencies(self, graph):
        self._assert_result_for_graph_is(True, graph)

    def _assert_no_missing_dependencies(self, graph):
        self._assert_result_for_graph_is(False, graph)

    def test_approves_empty_graph(self):
        self._assert_no_missing_dependencies({})

    def test_approves_when_dependencies_met(self):
        self._assert_no_missing_dependencies({
            'a': ['b', 'c'],
            'b': ['c'],
            'c': [],
        })

    def test_rejects_when_missing_dependencies(self):
        self._assert_missing_dependencies({
            'a': ['b', 'c'],
            'b': ['c'],
        })

class CircularDependenciesTest(unittest.TestCase):
    def _assert_result_for_graph_is(self, result, graph):
        dependency_graph = DependencyGraph(graph)
        self.assertEqual(result, dependency_graph.has_circular_dependencies())

    def test_no_cycles_in_emtpy_graph(self):
        self._assert_result_for_graph_is(False, {})

    def test_no_cycles_in_good_graph(self):
        self._assert_result_for_graph_is(False, {
            'a': ['b', 'c'],
            'b': ['c'],
            'c': [],
        })

    def test_finds_cycles(self):
        self._assert_result_for_graph_is(True, {
            'a': ['b', 'c'],
            'b': ['c'],
            'c': ['d'],
            'd': ['b'],
        })

if __name__ == '__main__':
    unittest.main()
