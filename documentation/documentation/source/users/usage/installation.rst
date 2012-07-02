Installing the TTR
==================

Assumptions and Prerequisites
-----------------------------

Assumptions
~~~~~~~~~~~

This document assumes that the DUT is an Android device and it has ADB setup to communicate with it via a USB cable. It further assumes that the PC that will be controlling the device is running Linux and will also be the PC that runs the `ttr` test. Since at this time **Lab126** is the intended customer for our data, the documentation will reflect a bias for their devices.

Prerequisites
~~~~~~~~~~~~~

Thus there is the assumption that:

   #. `adb` is installed and on the PATH (I put it in /usr/local/bin)
   #. The .android/adb_usb.ini file has been set up for this device
   #. The PC is running a Debian-based system.
   #. The user has super-user (`sudo`) status on the PC
   #. The device has root-access 

I won't assume that SL4A is installed, since every time there's a new build you have to re-install it, but if it is, all the better.

Downloads
---------

The downloads I'm referring to here are from the `Bitbucket Repository <https://bitbucket.org/allion_software_developers/timetorecovery/downloads>`_. The only required download is the python egg (`timetorecovertest-2012.05.24pre1-py2.7.egg <https://bitbucket.org/allion_software_developers/timetorecovery/downloads/timetorecovertest-2012.05.24pre1-py2.7.egg>`_ as of this writing) but there is also an `sl4a_setup.tbz <https://bitbucket.org/allion_software_developers/timetorecovery/downloads/timetorecovertest-2012.05.24pre1-py2.7.egg>`_ tar-file which can be used to help install the required `SL4A` packages to the DUT by side-loading them over the ADB connection.

Procedure
---------

The Basic Installation
~~~~~~~~~~~~~~~~~~~~~~

#. Make sure you have `easy_install` or `pip` (the python installers). You can install `easy_install` on Ubuntu using::

    sudo apt-get install python-setuptools

#. Change into the directory with the egg downloaded above and install it::

    sudo easy_install timetorecovertest-2012.05.24pre1-py2.7.egg

This will install the `timetorecovertest` library and create a command-line command called `ttr`.

Notes
+++++

* The actual name of the egg will depend on the day it was built.
* `pip` is the intended successor to `easy_install`. You can install it with `easy_install`::

    sudo easy_install pip

* A *pip* is the hole a made by a chick as it prepares to hatch. 

* To remove the installation get rid of `/usr/local/bin/ttr` and `/usr/local/lib/python2.7/dist-packages/timetorecovertest.egg-link`  (and check `/usr/local/lib/python2.7/dist-packages/easy_install.pth` for references to it).

Side-loading SL4A
~~~~~~~~~~~~~~~~~

If you need to install SL4A and you can launch apk's in the GUI you can install it using `the official instructions <http://code.google.com/p/android-scripting/wiki/RemoteControl>`_. If you can't install PythonForAndroid this way (as is the case for the current Kindle's) but have root access, you can download `sl4a_setup.tbz <https://bitbucket.org/allion_software_developers/timetorecovery/downloads/sl4a_setup.tbz>`_ and install it using the `amazon_install.sh` program.


#. Setup your `adb` connection to the DUT

#. Untar the file::

    tar -xjf sl4a_setup.tbz

#. Change into the folder::

    cd sl4a_setup.tbz

#. Execute the install::

    ./amazon_install.sh 
