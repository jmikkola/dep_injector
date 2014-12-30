import collections

class DependencyGraph:
    """ A generic dependency graph, useful for checking some properties """

    def __init__(self, graph):
        """ Creates a new DependencyGraph

        :param graph: A dict mapping a dependency name to a list of zero or more things it depends on
        """
        self._graph = graph

    def has_missing_dependencies(self):
        """ Checks to see if the graph contains any references to nodes that don't exist.

        :return: True if there are missing dependencies.
        """
        for dependencies in self._graph.values():
            for dependency in dependencies:
                if dependency not in self._graph:
                    return True
        return False

    def has_circular_dependencies(self):
        """ Checks to see if the graph contains any cycles.

        :return: True if there is a cycle.
        """
        dep_counts = {
            name: len(dependencies)
            for name, dependencies in self._graph.items()
        }

        depends_on = collections.defaultdict(set)
        for name, dependencies in self._graph.items():
            for dependency in dependencies:
                depends_on[dependency].add(name)

        deps_met = collections.deque(
            name for name, dependencies in self._graph.items()
            if len(dependencies) == 0
        )

        num_removed = 0
        while deps_met:
            num_removed += 1
            done = deps_met.pop()
            for name in depends_on[done]:
                dep_counts[name] -= 1
                if dep_counts[name] == 0:
                    deps_met.append(name)

        return num_removed < len(self._graph)
