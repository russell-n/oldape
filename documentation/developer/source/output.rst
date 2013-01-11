Output
======

The Outputs used in the `timetorecovertest` library try to mimic file-like objects as much as possible.

StandardOutput
--------------

Mimics the read-only methods for file-like objects. Assumes that the output it wants is coming from a queue

.. uml::

   StandardOutput: Queue.Queue queue
   StandardOutput: Generator iterator
   StandardOutput: Boolean end_of_file
   StandardOutput: String readline(timeout=1)
   StandardOutput: List readlines()
   StandardOutput: String read()

