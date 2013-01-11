A /proc/net/dev Pollster for the TPC
====================================

*Can the network counters for the Traffic PC's test interface be collected in parallel to that of the node's*

Work
----

* Added a check in the watchers builder that adds a ProcnetdevPollster for the TPC if it sees that it is building a ProcnetdevPollster

* Added a check in the nodes' builder to raise an error if there is no test interface given

* Changed the ProcnetdevPollsterBuilder to take the interface name from the device being passed in

Observations
------------

The actual implementation was relatively painless, but it took a while to figure out what to do -- the use of the builders is still not clear -- and I allowed too many empty values in the configuration file, a lot of things fail silently.

Extensions
----------

* For cases where the parameter is crucial but may fail silently (e.g. things passed in to create a regular expression) make an explicit type-check before using.

* Troubleshoot the missing headers for watcher-files
