from unittest import TestCase
from collections import namedtuple
from tottest.lexicographers.parametergenerator import ParameterGenerator

Parameter = namedtuple("Parameter", "name parameters".split())

node_names = "able baker".split()
a,b= node_names
nodes = [Parameter(name, parameter) for parameter,name in enumerate(node_names)]

ap_names = "chester delta elephant".split()
c, d , e = ap_names
aps = [Parameter(name, parameter) for parameter, name in enumerate(ap_names)]

test_directions = "far gumbo".split()
f, g = test_directions
tests = [Parameter(name, parameter) for parameter,name in enumerate(test_directions)]

parameters = [Parameter("nodes", nodes), Parameter("aps", aps), Parameter("tests", tests)]

names = ("nodes", "aps", "tests")
parameter_values = [[a,c,f], [a,c,g],
         [a,d,f], [a,d,g],
         [a,e,f], [a,e,g],
         [b,c,f], [b,c,g],
         [b,d,f], [b,d,g],
         [b,e,f], [b,e,g],]

class TestParameterGenerator(TestCase):
    def setUp(self):
        self.parameters = ParameterGenerator(parameters)
        return

    def test_parameters(self):
        for i, parameter in enumerate(self.parameters):
            for p in parameter:
                print parameter
                if hasattr(p, "name"):
                    self.assertIn(p.name, names)
        return
# end class TestParameterGenerator

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    pg = ParameterGenerator(parameters)
    for i,p in enumerate(pg):
        for j,q in enumerate(p):
            print names[i][j], q.name

