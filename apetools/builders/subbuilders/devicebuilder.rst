Device Builder
==============

This is a module to hold device builders.

   * Each builder expects a single parameter on initialization

   * Each builder has a `device` property that will return the built device



.. uml:: 

   BaseDeviceBuilder <|-- WindowsDeviceBuilder

.. module:: apetools.builders.subbuilders.devicebuilder
.. autosummary::
   :toctree: api

   WindowsDeviceBuilder
   WindowsDeviceBuilder.device



.. uml::

   BaseDeviceBuilder <|-- LinuxDeviceBuilder

.. autosummary::
   :toctree: api

   LinuxDeviceBuilder
   LinuxDeviceBuilder.device



.. uml::

   BaseDeviceBuilder <|-- AndroidDeviceBuilder

.. autosummary::
   :toctree: api

   AndroidDeviceBuilder
   AndroidDeviceBuilder.device



.. uml::

   BaseDeviceBuilder <|-- MacDeviceBuilder

.. autosummary::
   :toctree: api

   MacDeviceBuilder
   MacDeviceBuilder.device



.. uml::

   BaseDeviceBuilder <|-- IosDeviceBuilder

.. autosummary::
   :toctree: api

   IosDeviceBuilder
   IosDeviceBuilder.device
   
::

    class DeviceBuilderTypes(object):
        __slots__ = ()
        windows = "windows"
        linux = "linux"
        android = "android"
        mac = 'mac'
        osx = 'mac'
        macintosh = 'mac'
        ios = 'ios'
    # end class DeviceBuilderTypes
    
    device_builders = {DeviceBuilderTypes.windows:WindowsDeviceBuilder,
                       DeviceBuilderTypes.linux:LinuxDeviceBuilder,
                       DeviceBuilderTypes.android:AndroidDeviceBuilder,
                       DeviceBuilderTypes.mac:MacDeviceBuilder,
                       DeviceBuilderTypes.ios:IosDeviceBuilder}
    
    

