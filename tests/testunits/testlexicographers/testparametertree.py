from unittest import TestCase
from collections import namedtuple

from apetools.lexicographers.parametertree import ParameterTree


cargo = namedtuple("cargo", "name parameters".split())
a0 = cargo("a", ["a0"])
b0 = cargo("b", ["b0"])
b1 = cargo("b", ["b1"])
c0 = cargo("c", ["c0"])
c1 = cargo("c", ["c1"])

parameters = [cargo("a", [a0]), cargo("b", [b0, b1]), cargo("c",[c0, c1])]
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
                if key != "total_count":
                    self.assertEqual(paths[index][key], getattr(getattr(path, key), "parameters"))
        return
# end class TestParameterTree
    
if __name__ == "__main__":
    import pudb; pudb.set_trace()
    t = ParameterTree(parameters)
    for index,path in enumerate(t.paths):
        for key in path._fields:
            print(paths[index][key], getattr(path, key))
