Log Watcher
============

The `LogWatcher` watches the logs.

**Note:** on at least one device (*Airpad*) watching the log caused there to be *kmsg* messages noting that ADB was watching the log (an infinite stream of `adb_read` and `adb_write`).

.. uml::

   LogWatcher: StandardOutput output
   LogWatcher: Connection Connection
   LogWatcher: String path
   LogWatcher: run()
   LogWatcher: start()

