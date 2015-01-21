Popen Producer
==============

The purpose of the Popen Producer is to provide ways to read from the standard out and standard error without allowing incomplete file outputs to block the execution of the program.



PopenProducer
-------------

.. uml::

   BaseClass <|-- PopenProducer

.. module:: apetools.connections.producer
.. autosummary::
   :toctree: api

   PopenProducer
   PopenProducer.lock
   PopenProducer.counter
   PopenProducer.process
   PopenProducer.stdout
   PopenProducer.stderr
   PopenProducer.__del__



PopenFile
---------

.. uml::

   BaseThreadClass <|-- PopenFile

.. autosummary::
   :toctree: api

   PopenFile
   PopenFile.queue
   PopenFile.run
   PopenFile.start
   PopenFile.readline
   PopenFile.read
   PopenFile.close
   PopenFile.__iter__
   PopenFile.__del__
   
