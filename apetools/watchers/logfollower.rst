The Log Follower
================
.. currentmodule:: apetools.watchers.logfollower
The `LogFollower` executes a `tail -f` on a file and sends the output to a file. The motivation for it comes from the fact that I want to capture `syslog`, `kern.log`, etc. output. It is implemented as an extension of the `LogWatcher` but all it really does is over-ride the `execute` method so that it uses `tail` instead of `cat`.

.. uml::

   LogFollower -|> LogWatcher
   LogFollower : (output, error) execute()

.. autosummary::
   :toctree: api

   LogFollower

