from unittest import TestCase
from collections import namedtuple

from tottest.lexicographers.parametertree import ParameterTree


cargo = namedtuple("cargo", "name data".split())
a0 = cargo("a", "a0")
b0 = cargo("b", "b0")
b1 = cargo("b", "b1")
c0 = cargo("c", "c0")
c1 = cargo("c", "c1")

parameters = [[a0], [b0, b1], [c0, c1]]
paths = [{"a":a0, "b":b0, "c":c0},
         {"a":a0, "b":b0, "c":c1},
         {"a":a0, "b":b1, "c":c0},
         {"a":a0, "b":b1, "c":c1}]


class TestParameterTree(TestCase):
    def setUp(self):
        self.tree = ParameterTree(parameters)
        return

    def test_paths(self):
        for index,path in enumerate(self.tree.paths):
            for key in path._fields:
                self.assertEqual(paths[index][key], getattr(path, key))
        return
# end class TestParameterTree
