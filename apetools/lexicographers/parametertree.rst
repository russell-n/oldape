Parameter Tree
==============

A module to tranform lists of namedtuple parameters into lists of dictionaries.

::

    Parameters = namedtuple("Parameters", "name parameters".split())
    
    



Tree Node
---------

.. module:: apetools.lexicographers.parametertree
.. autosummary::
   :toctree: api

   TreeNode
   TreeNode.__str__



Parameter Tree
--------------

.. autosummary::
   :toctree: api

   ParameterTree
   ParameterTree.tree
   ParameterTree.paths
   ParameterTree._traverse

