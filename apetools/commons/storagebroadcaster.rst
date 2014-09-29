Storage Broadcaster
===================

The Storage Broadcaster maintains a file object and broadcasts to a list of targets.



The Storage Broadcaster
-----------------------

.. uml::

   BaseClass <|-- StorageBroadcaster

.. module:: apetools.commons.storagebroadcaster
.. autosummary::
   :toctree: api

   StorageBroadcaster
   StorageBroadcaster.targets
   StorageBroadcaster.folder
   StorageBroadcaster.check_folder
   StorageBroadcaster.open
   StorageBroadcaster.write
   StorageBroadcaster.add
   StorageBroadcaster.__call__
   StorageBroadcaster.close
   StorageBroadcaster.__del__



The Call File
-------------

.. autosummary::
   :tocree: api

   CallFile
   CallFile.open_file
   CallFile.send
   CallFile.__call__
   CallFile.write
   CallFile.close
   CallFile.__del__

