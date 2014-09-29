Data Counter
============

The Data Counter is meant for event watching. It tracks the time from its start to its first call.

Intended Sequence::

    d = DataCounter()
    d.start()
    d([data])
    d.stop()

Since it's only counting the data anything passed in to the call is ignored



Counter Datum Tuple
-------------------

.. uml::

   namedtuple <|-- CounterDatum

.. module:: apetools.commons.datacounter
.. autosummary::
   :toctree: api

   CounterDatum



The Data Counter
----------------

.. autosummary::
   :toctree: api

   DataCounter
   DataCounter.start
   DataCounter.stop

