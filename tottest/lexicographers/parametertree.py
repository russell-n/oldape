"""
A module to tranform lists of namedtuple parameters into lists of dictionaries.
"""

from collections import namedtuple

class TreeNode(object):
    """
    A Class to represent a node in a tree with arbitrary number of children
    """
    def __init__(self, cargo, children=None):
        """
        :param:

         - `cargo`: the data for this node
         - `children`: a list of TreeNodes
        """
        self.cargo = cargo
        self.children = children
        return

    def __str__(self):
        return str(self.cargo)
# end class TreeNode

class ParameterTree(object):
    """
    A class to build a tree from iterative parameters

    The main product is the `paths` attribute which can be iterated over to get the parameters for a test.
    """
    def __init__(self, parameters):
        """
        :param:

         - `parameters`: list of parameter objects with a `name` property
        """
        self.parameters = parameters
        self._tree = None
        self._paths = None
        return

    @property
    def tree(self):
        """
        builds the tree bottoms-up from the parameters
        :return: list of trees (highest nodes are parameters[0], leaves are parameters[-1])
        """
        if self._tree is None:
            parameters = self.parameters[:]
            leaves = parameters.pop()
            parameters.reverse()
            tree = [TreeNode(leaf) for leaf in leaves]
            for siblings in parameters:
                new_tree = [TreeNode(sibling, tree) for sibling in siblings]
                tree = new_tree
            self._tree = tree
        return self._tree

    @property
    def paths(self):
        """
        This is relying on a side-effect.
        
        :return: namedtuple of name:parameter dicts (paths from roots to leaves)
        """
        if self._paths is None:
            self._paths = []
            for limb in self.tree:
                path = {}
                self.traverse(limb, path)

            Paths = namedtuple("Paths", self._paths.keys())
            self._paths = Paths(*[self._paths[f] for f in Paths._fields])
        return self._paths
    
    def traverse(self, tree, path):
        """
        :param:
        
         - `tree`: A Tree object to traverse
         - `path`: a name:parametr dict to contain a particular path
         
        :postcondition:

         - path holds tree's cargo
         - if tree is a leaf, return path
         - if tree not leaf traverse children and traverse each child
         - append path returned by leaf to self._paths
        """
        path[tree.cargo.name] = tree.cargo
        if tree.children is None:
            return path
        for child in tree.children:
            new_path = path.copy()
            output = self.traverse(child, new_path)
            if output is not None:
                self._paths.append(output)
        return
# end class Parameter_Tree
