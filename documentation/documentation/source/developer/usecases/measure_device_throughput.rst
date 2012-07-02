Measure Device Throughput Test Case
===================================

.. uml::

   scale .75 

   APE --> (Measure Device Throughput)
   (Measure Device Throughput) --> (Perform Measurement) : <<include>>
   (Measure Device Throughput) --> (Configure System) : <<include>>
   (Measure Device Throughput) --> (Watch) : <<include>>

   (Perform Measurement) --> (Control Device) : <<include>>
   (Configure System) --> (Configure Device) : <<include>>
   (Configure System) --> (Configure Measurement) : <<include>>   
   (Configure System) --> (Configure Environment) : <<include>>
   (Watch) <|---- (Watch Device) : <<extend>>
   (Watch) <|---- (Watch Environment) : <<extend>>

   (Control Device) <|-- (Control Android) : <<extend>>
   (Control Device) <|-- (Control Linux) : <<extend>>

   (Configure Device) <|-- (Configure WiFi) : <<extend>>
   (Configure Device) <|-- (Push Button) : <<extend>>

   (Configure Measurement) <|-- (Fix Parameters) : <<extend>>
   (Configure Measurement) <|-- (Vary Parameters) : <<extend>>
   (Configure Measurement) <|-- (Randomize Parameters) : <<extend>>

   (Configure Environment) <|-- (Switch Power) : <<extend>>
   (Configure Environment) <|-- (Attenuate Signal) : <<extend>>
   (Configure Environment) <|-- (Configure AP) : <<extend>>

   (Control Android) --> (Connect ADB) : <<include>>
   (Control Linux) --> (Connect) : <<include>>

   (Configure WiFi) --> (Control Device) : <<include>>

   (Connect ADB) --> (Connect) : <<include>>

   (Connect) <|-- (Connect Locally) : <<extend>>
   (Connect) <|-- (Connect SSH) : <<extend>>
   (Connect) <|-- (Connect Serial) :<<extend>>
   (Connect) <|-- (Connect Telnet) : <<extend>>

   (Watch Device) <|-- (Watch RSSI) : <<extend>>
   (Watch Device) <|-- (Watch Noise) : <<extend>>
   (Watch Device) <|-- (Watch Logs) : <<extend>>
   (Watch Device) <|-- (Watch Resources) : <<extend>>   
   (Watch Device) --> (Control Device) : <<include>>   
   
   (Watch Logs) <|-- (Watch KMSG) : <<extend>>
   (Watch Logs) <|-- (Watch Logcat) : <<extend>>

   (Watch Resources) <|-- (Watch Power) : <<extends>>
   (Watch Resources) <|-- (Watch CPU) : <<extends>>
   (Watch Resources) <|-- (Watch Process) : <<extends>>
   (Watch Resources) <|-- (Watch Memory) : <<extends>>
