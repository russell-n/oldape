File Expression Watcher
=======================

A module to watch packets and bytes received on an interface.

The File-expression watchers differ from the catters and pollsters in that they:

 * repeatedly cat the file at set intervals, unlike logcatters
 * send output directly to file without making calculations (unlike proc-pollsters)



Base File Expression Watcher
----------------------------

.. uml::

   BasePollster <|-- BaseFileExpressionwatcher

.. module:: apetools.watchers.fileexpressionwatcher
.. autosummary::
   :toctree: api

   BaseFileexpressionwatcher
   BaseFileexpressionwatcher.stopped
   BaseFileexpressionwatcher.name
   BaseFileexpressionwatcher.expression_keys
   BaseFileexpressionwatcher.connection
   BaseFileexpressionwatcher.run



Battery Watcher
---------------

.. uml::

   BaseFileexpressionwatcher <|-- BatteryWatcher

.. autosummary::
   :toctree: api

   BatteryWatcher
   BatteryWatcher.header
   BatteryWatcher.expression_keys
   BatteryWatcher.expression

