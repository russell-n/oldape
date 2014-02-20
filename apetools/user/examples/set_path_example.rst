Read-Only Device, Non-Interactive PATH Not Complete
===================================================

Unique Features
---------------

Devices that meet the following conditions should find this example applicable:

   * Device is read-only (or you lack permissions to move, link, or edit files)

   * Commands needed aren't on the PATH

Example Assumptions
-------------------

To make the example concrete, we'll assume that the device has an ssh-connection, is linux-based, and is missing the following directories on its PATH:

   * /sbin

   * /opt/wlanmanager/thirdparty/bin

We'll also assume that the wifi interface is called `wln0`, and that the syslog is at `/var/viewer/messages.log`.

