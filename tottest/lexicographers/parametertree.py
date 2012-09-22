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
        :return: list of namedtuples
        """
        if self._paths is None:
            # create the paths with a series of tree-traversals
            self._paths = []
            for limb in self.tree:
                path = {}
                self._traverse(limb, path, self._paths)

            # convert self._paths from dicts to namedtuples
            paths = []
            for path in self._paths:
                Paths = namedtuple("Paths", path.keys())
                paths.append(Paths(*[path[f] for f in Paths._fields]))
            self._paths = paths
        return self._paths
    
    def _traverse(self, tree, path, paths):
        """
        A depth-first traversal
        
        :param:
        
         - `tree`: A Tree object to traverse
         - `path`: a name:parameter dict to contain a particular path
         - `paths`: The list to store all the paths
         
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
            output = self._traverse(child, new_path, paths)
            if output is not None:
                paths.append(output)
        return
# end class Parameter_Tree
