Threads
=======

.. _threaduml:

Thread
------

The Thread class is a subclass of threading.Thread that implements the convenience constructor suggested by Alan Downey in the `Little Book of Semaphores`. It really just sets it to daemonic and calls `start()` automatically.

.. uml::

   Thread --|> threading.Thread
   Thread: MethodType t
