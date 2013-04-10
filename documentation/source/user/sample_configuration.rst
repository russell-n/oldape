Sample Configuration
====================

A sample configuration file that used all of the previous sections::

   [TEST]
   operation_setup = watchlogs
   setup_test = rotate,timetorecovery,dumpdevicestate
   execute_test = iperf
   output_folder = tate_71_apg_lab126_{t}
   repeat = 2
   tag = ALLION
   recovery_time = 1 Second
   
   [SLEEP]
   time = 1 Hour

   [POWERON]
   e2000 = hostname:synaxxx,switch:5, sleep:5
   wndr3700 = hostname:synaxxx,switch:1, sleep:5
   
   [NODES]
   tate = hostname:phoridfly,login:root,operating_system:android,connection:adbshellssh,test_interface:wlan0
      
   [ROTATE]
   hostname = phoridfly
   username = root
   #password = 
   angles = 180,0:50,45,90:100,    270:10
   
   [TRAFFIC_PC]
   tpc = operating_system:linux,connection:ssh,test_interface:eth3,hostname:lancet,login:allion
   
   [WATCHLOGS]
   logcat = type:adblogcat, buffers:all
   kmsg = type:logcat,command:cat,arguments:/proc/kmsg
   battery = type:battery,name:/sys/class/power_supply/bq27541/uevent
   proc = type:procnetdev,interface:wlan0
   device = type:device
   cpu = type:cpu
   
   [IPERF]
   directions = from_dut, to_dut
   time = 10 Seconds
   protocol = tcp
   window = 256K
   length = 1470
   parallel = 4
   interval = 1
   format = b

