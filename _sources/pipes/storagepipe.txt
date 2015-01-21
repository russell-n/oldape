Storage Pipe
============

A pipe to hold Storage Output.

The differernce between the 3 pipes (start, pipe, sink) is the way they handle a header line (if there is one).

If no header token is given, it tee's all input to storage and the target and ignores the header.



Storage Pipe Enum
-----------------

::

    class StoragePipeEnum(object):
        """
        A holder of constants for the StoragePipe
        """
        __slots__  = ()
        start = "start"
        pipe = "pipe"
        sink = "sink"
    # end class StoragePipeEnum
    
    



Storage Pipe
------------

.. uml::

   BaseClass <|-- StoragePipe

.. module:: apetools.pipes.storagepipe
.. autosummary::
   :toctree: api

   StoragePipe
   StoragePipe.timestamp
   StoragePipe.storage
   StoragePipe.pipe_start
   StoragePipe.pipe_sink
   StoragePipe.pipe
   StoragePipe.open_start
   StoragePipe.open_sink
   StoragePipe.open
   StoragePipe.extend_path
   StoragePipe.set_emit
   StoragePipe.unset_emit

