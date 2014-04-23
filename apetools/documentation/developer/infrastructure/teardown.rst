TearDown
========

A TearDown closes up the shop.

.. uml::

   TearDown o-- SetUp
   TearDown o-- Notifier
   TearDown: setup
   TearDown: run()
