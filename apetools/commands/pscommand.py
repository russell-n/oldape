
# python regular expressions
import re

#apetools
from apetools.baseclass import BaseClass
from apetools.commons.errors import CommandError
from apetools.commons import enumerations
from apetools.parsers import oatbran
from apetools.commands.basecommand import BaseProcessCommand, ProcessCommandEnum
from apetools.commands.basecommand import BaseProcessGrep, ProcessGrepEnum
operating_systems = enumerations.OperatingSystem


class PsCommand(BaseProcessCommand):
    """
    The Ps Command issues commands and watches for errors
    """
    def __init__(self, *args, **kwargs):
        """
        PsCommand Constructor

        :param:

         - `connection`: A connection to the device
         - `arguments`: the arguments to get output from ``ps``
        """
        super(PsCommand, self).__init__(*args, **kwargs)
        return

    @property
    def arguments(self):
        """
        ``ps`` arguments based on the connection.operating_system
        
        :return: argument string for the ``ps`` call        
        """
        if self._arguments is None:
            os = self.connection.operating_system
            self.logger.debug("setting the arguments for `{0}`".format(os))
            if os == operating_systems.android:
                self.logger.debug("Using the android arguments")
                self._arguments = ''
            else:
                self._arguments = "-e"
        return self._arguments
    
    @property
    def error_expression(self):
        """
        Holds the expression to match error messages

        :return: compiled regular expression to match error messages
        """
        if self._error_expression is None:
            # the only difference between the android and linux is the word `command`
            # sometimes there is a prefix referencing the shell, but this should still work
            missing = oatbran.NAMED(n=ProcessCommandEnum.missing,
                                    e=oatbran.SPACES.join([self.command+':',
                                                           '(?:command\s+)*not',
                                                           'found']))
            # watch out-- android doesn't raise an error if you pass bad arguments
            # it just doesn't work
            bad_arg = oatbran.NAMED(n=ProcessCommandEnum.bad_arg,
                                    e=oatbran.SPACES.join(["error:",
                                                           "unsupported",
                                                           'SysV',
                                                           'option']))
            self._error_expression = re.compile(missing + oatbran.OR + bad_arg)
        return self._error_expression

    def run(self):
        """
        Calls ``ps`` on the connection

        :return: output from the connections call to ps (stdout, stderr)
        """
        return self.connection.ps(self.arguments)

    @property
    def command(self):
        """
        `ps`
        """
        if self._command is None:
            self._command = 'ps'
        return self._command


# linux ps expressions
PID = oatbran.NAMED(n=ProcessGrepEnum.pid,
                           e=oatbran.NATURAL)
TTY = oatbran.GROUP("\?" + oatbran.OR + "pts/" + oatbran.NATURAL +
                    oatbran.OR + oatbran.NOT_SPACES)

TWO_DIGITS = oatbran.DIGIT + oatbran.EXACTLY.format(2)
TIME = ":".join([TWO_DIGITS] * 3)
MAC_TIME = (oatbran.DIGIT + r"{1,2}" + ':' + TWO_DIGITS + '\.' +
            TWO_DIGITS)

#PROCESS = oatbran.NAMED(n=ProcessGrepEnum.process,
#                        e="{{{process_name}}}")
PSE_LINUX = oatbran.SPACES.join([PID, TTY, TIME])
PSE_MAC = oatbran.SPACES.join([PID, TTY, MAC_TIME])

#android ps
USER = oatbran.CLASS(oatbran.ALPHA_NUM + '_') + oatbran.ONE_OR_MORE
PPID = oatbran.NATURAL
VSIZE = oatbran.NATURAL
RSS = oatbran.NATURAL
WCHAN = oatbran.ALPHA_NUMS
PC = oatbran.HEXADECIMALS
S_OR_R = "(S" + oatbran.OR + "R)"
PS_ANDROID = oatbran.SPACES.join((USER, PID, PPID, VSIZE, RSS, WCHAN, PC, S_OR_R))

#cygwin
#CYGWIN = oatbran.STRING_START + oatbran.SPACES + NAMED(n=expressions.PID_NAME,e=INTEGER)


class PsGrep(BaseProcessGrep):
    """
    The Ps command adapted to extract process IDs.
    """
    def __init__(self, *args, **kwargs):
        """
        PsGrep Constructon

        :param:
        
         - `process`: The name of the process to get (if not set pass into call())
        """
        super(PsGrep, self).__init__(*args, **kwargs)
        return
            
    @property
    def process_query(self):
        """
        The ``top`` command

        :return: PsCommand to return output from the ``top`` command.
        """
        if self._process_query is None:
            self.logger.debug("Setting the PsCommand")
            self._process_query = PsCommand(connection=self.connection)
        return self._process_query

    @property
    def expression(self):
        """
        Sets the regular expression to match output based on the connection.operating_system
        
        :return: compiled regular expression for the ps command
        """
        if self._expression is None:
            if self.connection.operating_system == OperatingSystem.android:
                self.logger.debug("Using Android Expression")
                expression = PS_ANDROID
            elif self.connection.operating_system == OperatingSystem.windows:
                #self.logger.debug("Using Cygwin Expression")
                #expression = CYGWIN
                raise CommandError("Cygwin Expression not implemented")
            elif self.connection.operating_system == OperatingSystem.mac:
                self.logger.debug("Using Mac OS 'ps' regular expression")
                expression = PSE_MAC
            else:
                #self.logger.debug("Using linux expression")
                expression = PSE_LINUX
            expression = (expression + oatbran.SPACES +
                          oatbran.NAMED(n=ProcessGrepEnum.process,
                                        e=re.escape(self.process)) +
                                        r'(\b|$)')
            self.logger.debug("Expression: {0}".format(expression))
            self._expression = re.compile(expression)
        return self._expression       

# end class PsGrep    


#python standard library
import unittest
from StringIO import StringIO
import random
from string import ascii_letters

# third-party
from nose.tools import raises
from mock import MagicMock
import nose
#apetools
from apetools.commons.enumerations import OperatingSystem


nexus_command_not_found = '/system/bin/sh: ps: not found'
first_ubuntu_line = "  PID TTY          TIME CMD"
getty_pids = "1068 1075 1087 1089 1095  1629".split()
ubuntu_lines = '''    1 ?        00:00:56 init
    2 ?        00:00:00 kthreadd
    3 ?        00:02:54 ksoftirqd/0
    5 ?        00:00:27 kworker/u:0
    6 ?        00:00:15 migration/0
    7 ?        00:00:03 watchdog/0
    8 ?        00:00:46 migration/1
   10 ?        00:03:25 ksoftirqd/1
   11 ?        00:00:04 watchdog/1
   12 ?        00:00:15 migration/2
   14 ?        00:02:56 ksoftirqd/2
   15 ?        00:00:04 watchdog/2
   16 ?        00:00:46 migration/3
   18 ?        00:03:29 ksoftirqd/3
   19 ?        00:00:04 watchdog/3
   20 ?        00:00:00 cpuset
   21 ?        00:00:00 khelper
   22 ?        00:00:00 kdevtmpfs
   23 ?        00:00:00 netns
   25 ?        00:00:02 sync_supers
   26 ?        00:00:00 bdi-default
   27 ?        00:00:00 kintegrityd
   28 ?        00:00:00 kblockd
   29 ?        00:00:00 ata_sff
   30 ?        00:00:00 khubd
   31 ?        00:00:00 md
   36 ?        00:00:00 khungtaskd
   37 ?        00:00:18 kswapd0
   38 ?        00:00:00 ksmd
   39 ?        00:00:00 khugepaged
   40 ?        00:00:00 fsnotify_mark
   41 ?        00:00:00 ecryptfs-kthrea
   42 ?        00:00:00 crypto
   51 ?        00:00:00 kthrotld
   52 ?        00:00:00 scsi_eh_0
   53 ?        00:00:00 scsi_eh_1
   56 ?        00:00:00 binder
   76 ?        00:00:00 deferwq
   77 ?        00:00:00 charger_manager
   78 ?        00:00:00 devfreq_wq
  295 ?        00:00:00 kdmflush
  296 ?        00:00:00 kcryptd_io
  297 ?        00:00:00 kcryptd
  310 ?        00:00:00 kdmflush
  313 ?        00:00:00 kdmflush
  335 ?        00:01:29 jbd2/dm-1-8
  336 ?        00:00:00 ext4-dio-unwrit
  355 ?        00:00:23 flush-252:1
  567 ?        00:00:00 upstart-udev-br
  569 ?        00:00:00 udevd
  664 ?        00:00:00 kpsmoused
  713 ?        00:00:00 hd-audio0
  787 ?        00:00:00 upstart-socket
  799 ?        00:00:00 kvm-irqfd-clean
  894 ?        00:00:00 aspell
  896 ?        00:02:57 sshd
  955 ?        00:00:06 dbus-daemon
  984 ?        00:00:00 modem-manager
  986 ?        00:00:00 bluetoothd
 1007 ?        00:00:10 NetworkManager
 1013 ?        00:00:15 avahi-daemon
 1016 ?        00:00:00 avahi-daemon
 1018 ?        00:00:13 polkitd
 1052 ?        00:00:03 cupsd
 1068 tty4     00:00:00 getty
 1075 tty5     00:00:00 getty
 1087 tty2     00:00:00 getty
 1089 tty3     00:00:00 getty
 1095 tty6     00:00:00 getty
 1118 ?        00:00:00 acpid
 1124 ?        00:00:00 lightdm
 1126 ?        00:00:50 whoopsie
 1131 ?        00:00:50 irqbalance
 1141 ?        00:00:01 cron
 1142 ?        00:00:00 atd
 1147 ?        00:00:00 krfcommd
 1163 tty7     03:19:43 Xorg
 1197 ?        00:00:15 accounts-daemon
 1241 ?        00:00:02 console-kit-dae
 1329 ?        00:00:04 master
 1368 ?        00:00:00 kworker/1:1
 1417 ?        00:00:00 upowerd
 1429 ?        00:22:43 nagios3
 1494 ?        00:00:31 apache2
 1548 ?        00:00:02 kworker/0:2
 1629 tty1     00:00:00 getty
 1643 ?        00:00:00 colord
 1651 ?        00:00:00 lightdm
 1706 ?        00:00:08 rtkit-daemon
 1748 ?        00:00:06 dnsmasq
 1944 ?        00:00:00 qmgr
 2055 ?        00:00:04 gnome-keyring-d
 2066 ?        00:00:16 gnome-session
 2101 ?        00:00:03 ssh-agent
 2104 ?        00:00:00 dbus-launch
 2105 ?        00:01:02 dbus-daemon
 2107 ?        00:00:00 at-spi-bus-laun
 2111 ?        00:00:01 dbus-daemon
 2114 ?        00:00:19 at-spi2-registr
 2125 ?        00:03:05 gnome-settings-
 2133 ?        00:00:03 gvfsd
 2137 ?        00:00:00 gvfsd-fuse
 2145 ?        02:41:39 compiz
 2150 ?        00:00:00 dconf-service
 2154 ?        00:00:11 nm-applet
 2156 ?        00:00:09 gnome-fallback-
 2157 ?        00:00:09 bluetooth-apple
 2158 ?        00:00:08 polkit-gnome-au
 2160 ?        00:00:52 nautilus
 2174 ?        00:00:05 gvfs-udisks2-vo
 2179 ?        00:05:50 udisksd
 2191 ?        00:39:03 pulseaudio
 2203 ?        00:00:00 gvfs-gphoto2-vo
 2205 ?        00:00:02 gconfd-2
 2209 ?        00:00:00 gvfs-afc-volume
 2215 ?        00:00:00 gconf-helper
 2218 ?        00:00:00 gvfsd-trash
 2224 ?        00:01:50 bamfdaemon
 2233 ?        00:00:00 gvfsd-metadata
 2237 ?        00:00:00 gvfsd-burn
 2241 ?        00:00:00 sh
 2242 ?        00:01:36 gtk-window-deco
 2254 ?        00:19:24 unity-panel-ser
 2256 ?        00:06:21 hud-service
 2269 ?        00:00:09 indicator-print
 2271 ?        00:00:00 indicator-appli
 2277 ?        00:00:00 indicator-sessi
 2278 ?        00:00:05 indicator-datet
 2284 ?        00:00:00 indicator-messa
 2285 ?        00:00:08 indicator-sound
 2302 ?        00:00:00 evolution-sourc
 2322 ?        00:00:03 goa-daemon
 2326 ?        00:00:00 geoclue-master
 2338 ?        00:00:00 ubuntu-geoip-pr
 2501 ?        00:26:15 screen
 2721 ?        00:00:08 telepathy-indic
 2727 ?        00:00:00 mission-control
 2733 ?        00:00:01 signon-ui
 2798 ?        00:00:54 gnome-screensav
 2799 ?        00:00:16 zeitgeist-datah
 2805 ?        00:00:01 zeitgeist-daemo
 2812 ?        00:00:01 zeitgeist-fts
 2817 ?        00:00:00 cat
 3120 ?        00:00:25 unity-applicati
 3122 ?        00:00:08 unity-files-dae
 3128 ?        00:00:18 unity-music-dae
 3130 ?        00:00:01 unity-shopping-
 3131 ?        00:00:00 unity-gwibber-d
 3132 ?        00:00:01 unity-lens-phot
 3134 ?        00:00:02 unity-lens-vide
 3222 ?        00:00:00 unity-musicstor
 3224 ?        00:00:00 unity-scope-gdo
 3258 ?        00:00:04 unity-scope-vid
 3394 ?        00:00:30 udisks-daemon
 3395 ?        00:00:00 udisks-daemon
 3415 ?        00:00:01 python
 3545 ?        00:00:00 dbus
 3568 ?        00:00:27 update-notifier
 3616 ?        00:00:00 system-service-
 4084 ?        02:53:19 spotify
 4578 ?        00:00:00 unity-webapps-s
 4689 ?        00:00:00 kworker/3:0
 5258 ?        00:00:44 deja-dup-monito
 6325 pts/12   00:00:00 bash
 7865 pts/9    00:00:00 bash
 8045 ?        00:00:00 pickup
10192 ?        00:00:05 python
10334 pts/3    00:00:00 bash
10464 pts/3    00:02:47 irssi
10512 pts/6    00:00:00 bash
10746 ?        00:00:06 kworker/2:0
10879 ?        00:00:00 kworker/3:2
11424 pts/8    00:00:00 sudo
11463 pts/8    00:00:00 sh
12121 pts/6    00:00:00 emacsclient
12653 ?        00:00:00 kworker/0:0
13410 ?        00:00:01 apache2
13625 ?        03:32:55 firefox
13749 ?        00:00:00 python3
16114 ?        00:00:00 lightdm
16403 ?        00:28:06 firefox
16981 ?        00:00:00 kworker/0:1
17324 ?        00:02:10 rsyslogd
18088 pts/14   00:00:00 bash
18419 pts/14   00:00:00 ps
18502 pts/10   00:00:00 bash
18776 pts/11   00:00:00 python
18857 ?        00:00:00 sh
18858 ?        00:05:52 gnome-terminal
18865 ?        00:00:00 gnome-pty-helpe
18866 pts/0    00:00:00 bash
21609 pts/7    00:00:01 gtypist
22016 ?        00:00:01 gvfsd-http
22066 ?        00:00:07 update-manager
22165 ?        00:42:14 emacs
22302 pts/4    00:00:07 python
22760 ?        00:00:03 apache2
22947 ?        00:00:02 kworker/u:1
23714 ?        00:00:06 kworker/1:0
24007 pts/0    00:00:00 screen
26493 pts/7    00:00:00 bash
26780 ?        00:00:00 udevd
26781 ?        00:00:00 udevd
29452 ?        00:00:00 kworker/2:1
31106 ?        00:00:03 apache2
31107 ?        00:00:03 apache2
31108 ?        00:00:03 apache2
31109 ?        00:00:03 apache2
31110 ?        00:00:03 apache2
31692 ?        00:18:25 plugin-containe'''.split('\n')

ubuntu_process_names = [name.strip() for name in """init           
kthreadd       
ksoftirqd/0    
kworker/u:0    
migration/0    
watchdog/0     
migration/1    
ksoftirqd/1    
watchdog/1     
migration/2    
ksoftirqd/2    
watchdog/2     
migration/3    
ksoftirqd/3    
watchdog/3     
cpuset         
khelper        
kdevtmpfs      
netns          
sync_supers    
bdi-default    
kintegrityd    
kblockd        
ata_sff        
khubd          
md             
khungtaskd     
kswapd0        
ksmd           
khugepaged     
fsnotify_mark  
ecryptfs-kthrea
crypto         
kthrotld       
scsi_eh_0      
scsi_eh_1      
binder         
deferwq        
charger_manager
devfreq_wq     
kdmflush       
kcryptd_io     
kcryptd        
kdmflush       
kdmflush       
jbd2/dm-1-8    
ext4-dio-unwrit
flush-252:1    
upstart-udev-br
udevd          
kpsmoused      
hd-audio0      
upstart-socket
kvm-irqfd-clean
aspell         
sshd           
dbus-daemon    
modem-manager  
bluetoothd     
NetworkManager 
avahi-daemon   
avahi-daemon   
polkitd        
cupsd          
getty          
getty          
getty          
getty          
getty          
acpid          
lightdm        
whoopsie       
irqbalance     
cron           
atd            
krfcommd       
Xorg           
accounts-daemon
console-kit-dae
master         
kworker/1:1    
upowerd        
nagios3        
apache2        
kworker/0:2    
getty          
colord         
lightdm        
rtkit-daemon   
dnsmasq        
qmgr           
gnome-keyring-d
gnome-session  
ssh-agent      
dbus-launch    
dbus-daemon    
at-spi-bus-laun
dbus-daemon    
at-spi2-registr
gnome-settings-
gvfsd          
gvfsd-fuse     
compiz         
dconf-service  
nm-applet      
gnome-fallback-
bluetooth-apple
polkit-gnome-au
nautilus       
gvfs-udisks2-vo
udisksd        
pulseaudio     
gvfs-gphoto2-vo
gconfd-2       
gvfs-afc-volume
gconf-helper   
gvfsd-trash    
bamfdaemon     
gvfsd-metadata 
gvfsd-burn     
sh             
gtk-window-deco
unity-panel-ser
hud-service    
indicator-print
indicator-appli
indicator-sessi
indicator-datet
indicator-messa
indicator-sound
evolution-sourc
goa-daemon     
geoclue-master 
ubuntu-geoip-pr
screen         
telepathy-indic
mission-control
signon-ui      
gnome-screensav
zeitgeist-datah
zeitgeist-daemo
zeitgeist-fts  
cat            
unity-applicati
unity-files-dae
unity-music-dae
unity-shopping-
unity-gwibber-d
unity-lens-phot
unity-lens-vide
unity-musicstor
unity-scope-gdo
unity-scope-vid
udisks-daemon  
udisks-daemon  
python         
dbus           
update-notifier
system-service-
spotify        
unity-webapps-s
kworker/3:0    
deja-dup-monito
bash           
bash           
pickup         
python         
bash           
irssi          
bash           
kworker/2:0    
kworker/3:2    
sudo           
sh             
emacsclient    
kworker/0:0    
apache2        
firefox        
python3        
lightdm        
firefox        
kworker/0:1    
rsyslogd       
bash           
ps             
bash           
python         
sh             
gnome-terminal 
gnome-pty-helpe
bash           
gtypist        
gvfsd-http     
update-manager 
emacs          
python         
apache2        
kworker/u:1    
kworker/1:0    
screen         
bash           
udevd          
udevd          
kworker/2:1    
apache2        
apache2        
apache2        
apache2        
apache2        
plugin-containe""".split('\n')]

ubuntu_process_list = [name.strip() for name in '''1
    2
    3
    5
    6
    7
    8
   10
   11
   12
   14
   15
   16
   18
   19
   20
   21
   22
   23
   25
   26
   27
   28
   29
   30
   31
   36
   37
   38
   39
   40
   41
   42
   51
   52
   53
   56
   76
   77
   78
  295
  296
  297
  310
  313
  335
  336
  355
  567
  569
  664
  713
  787
  799
  894
  896
  955
  984
  986
 1007
 1013
 1016
 1018
 1052
 1068
 1075
 1087
 1089
 1095
 1118
 1124
 1126
 1131
 1141
 1142
 1147
 1163
 1197
 1241
 1329
 1368
 1417
 1429
 1494
 1548
 1629
 1643
 1651
 1706
 1748
 1944
 2055
 2066
 2101
 2104
 2105
 2107
 2111
 2114
 2125
 2133
 2137
 2145
 2150
 2154
 2156
 2157
 2158
 2160
 2174
 2179
 2191
 2203
 2205
 2209
 2215
 2218
 2224
 2233
 2237
 2241
 2242
 2254
 2256
 2269
 2271
 2277
 2278
 2284
 2285
 2302
 2322
 2326
 2338
 2501
 2721
 2727
 2733
 2798
 2799
 2805
 2812
 2817
 3120
 3122
 3128
 3130
 3131
 3132
 3134
 3222
 3224
 3258
 3394
 3395
 3415
 3545
 3568
 3616
 4084
 4578
 4689
 5258
 6325
 7865
 8045
10192
10334
10464
10512
10746
10879
11424
11463
12121
12653
13410
13625
13749
16114
16403
16981
17324
18088
18419
18502
18776
18857
18858
18865
18866
21609
22016
22066
22165
22302
22760
22947
23714
24007
26493
26780
26781
29452
31106
31107
31108
31109
31110
31692'''.split('\n')]

android_output = """USER     PID   PPID  VSIZE  RSS     WCHAN    PC         NAME
root      1     0     276    264   80168c10 0000eccc S /init
root      2     0     0      0     800f3e24 00000000 S kthreadd
root      3     2     0      0     800e030c 00000000 S ksoftirqd/0
root      4     2     0      0     800f0434 00000000 S events/0
root      5     2     0      0     800f0434 00000000 S khelper
root      6     2     0      0     800fad2c 00000000 S async/mgr
root      7     2     0      0     800f0434 00000000 S suspend
root      8     2     0      0     80116bac 00000000 S irq/155-pm8058-
root      9     2     0      0     80142948 00000000 S sync_supers
root      10    2     0      0     801433ac 00000000 S bdi-default
root      11    2     0      0     800f0434 00000000 S kblockd/0
root      12    2     0      0     800f0434 00000000 S ksuspend_usbd
root      13    2     0      0     803134d4 00000000 S khubd
root      14    2     0      0     800f0434 00000000 S kmmcd
root      15    2     0      0     800f0434 00000000 S bluetooth
root      16    2     0      0     800f0434 00000000 S rpciod/0
root      17    2     0      0     800f0434 00000000 S modem_notifier
root      18    2     0      0     800f0434 00000000 S qmi
root      19    2     0      0     800f0434 00000000 S nmea
root      20    2     0      0     800f0434 00000000 S rpcrouter
root      21    2     0      0     8005b8d0 00000000 D rpcrotuer_smd_x
root      22    2     0      0     800f0434 00000000 S dalrpc_rcv_DAL0
root      23    2     0      0     8005fa84 00000000 S krpcserversd
root      24    2     0      0     8005dc34 00000000 D krmt_storagecln
root      25    2     0      0     80061314 00000000 D krmt_storagecln
root      26    2     0      0     8013a8dc 00000000 S kswapd0
root      27    2     0      0     800f0434 00000000 S aio/0
root      28    2     0      0     800f0434 00000000 S nfsiod
root      29    2     0      0     800f0434 00000000 S crypto/0
root      39    2     0      0     800f0434 00000000 S mdp_dma_wq
root      40    2     0      0     800f0434 00000000 S mdp_vsync_wq
root      41    2     0      0     800f0434 00000000 S mdp_pipe_ctrl_w
root      42    2     0      0     800f0434 00000000 S vidc_worker_que
root      43    2     0      0     800f0434 00000000 S vidc_timer_wq
root      44    2     0      0     800f0434 00000000 S diag_wq
root      45    2     0      0     800f0434 00000000 S scsi_tgtd/0
root      46    2     0      0     802ebb74 00000000 S mtdblockd
root      53    2     0      0     800f0434 00000000 S k_otg
root      54    2     0      0     803479e0 00000000 S usb_mass_storag
root      55    2     0      0     800f0434 00000000 S k_gserial
root      56    2     0      0     800f0434 00000000 S k_rmnet_work
root      57    2     0      0     800f0434 00000000 S headset_hook
root      58    2     0      0     800f0434 00000000 S fwupdate_wq
root      59    2     0      0     8005dc34 00000000 D krtcclntd
root      60    2     0      0     80061314 00000000 D krtcclntcbd
root      61    2     0      0     80399940 00000000 D mt9p111_flashle
root      62    2     0      0     8005dc34 00000000 D kbatteryclntd
root      63    2     0      0     80061314 00000000 D kbatteryclntcbd
root      64    2     0      0     800f0434 00000000 S kstriped
root      65    2     0      0     800f0434 00000000 S kondemand/0
root      66    2     0      0     800f0434 00000000 S kconservative/0
root      67    2     0      0     80116bac 00000000 S irq/270-msm-sdc
root      68    2     0      0     800f0434 00000000 S switch_gpio
root      69    2     0      0     800f0434 00000000 S usbhid_resumer
root      70    2     0      0     800f0434 00000000 S binder
root      71    2     0      0     805087c8 00000000 S krfcommd
root      72    2     0      0     8006b76c 00000000 D voice
root      73    2     0      0     800b5af4 00000000 S acdb_cb_thread
root      74    2     0      0     8005dc34 00000000 D khsclntd
root      75    2     0      0     803ce22c 00000000 S mmcqd
root      76    2     0      0     803ce22c 00000000 S mmcqd
root      77    2     0      0     801ca904 00000000 S kjournald
root      80    2     0      0     80178c20 00000000 S flush-179:0
root      81    2     0      0     801ca904 00000000 S kjournald
root      82    2     0      0     801ca904 00000000 S kjournald
root      83    2     0      0     801ca904 00000000 S kjournald
root      86    2     0      0     801ca904 00000000 S kjournald
system    88    1     700    252   803e14b4 6fd0dbbc S /system/bin/servicemanager
root      89    1     3636   408   ffffffff 6fd0e22c S /system/bin/vold
root      90    1     3960   608   ffffffff 6fd0e22c S /system/bin/netd
radio     92    1     8044   480   ffffffff 6fd0dce4 S /system/bin/qmuxd
radio     93    1     17996  2412  ffffffff ffff0520 S /system/bin/rild
root      95    1     146784 16620 80168c10 6fd0dce4 S zygote
media     96    1     34840  4296  ffffffff 6fd0dbbc S /system/bin/mediaserver
bluetooth 97    1     1164   332   80168c10 ffff0520 S /system/bin/dbus-daemon
root      98    1     704    276   804adb6c 6fd0d91c S /system/bin/installd
system    99    1     784    276   804108c8 6fd0e54c S /system/bin/fm_server
system    100   1     772    232   804108c8 6fd0e54c S /system/bin/runit
compass   101   1     712    264   80355d74 6fd0d91c S /system/bin/geomagneticd
compass   102   1     2744   272   ffffffff 6fd0eb8c S /system/bin/orientationd
compass   103   1     2744   276   ffffffff 6fd0eb8c S /system/bin/proximityd
compass   104   1     2748   292   ffffffff 6fd0eb8c S /system/bin/lightd
keystore  105   1     1512   236   804108c8 6fd0e54c S /system/bin/keystore
system    106   1     560    228   8010e8b4 6fd0d91c S /system/bin/logfile
root      108   1     2020   452   ffffffff 6fd0d91c S /system/bin/port-bridge
root      109   1     5348   676   ffffffff 6fd0eb8c S /system/bin/netmgrd
root      112   1     5808   268   ffffffff 6fd0dbbc S /system/bin/rmt_storage
root      113   1     4672   708   ffffffff 6fd0dbbc S /system/bin/hdmid
system    172   95    373280 42484 ffffffff 6fd0dbbc S system_server
app_91    264   95    221836 23160 ffffffff 6fd0eb8c S org.pocketworkstation.pckeyboard
radio     272   95    235036 24896 ffffffff 6fd0eb8c S com.android.phone
system    273   95    202460 14148 ffffffff 6fd0eb8c S com.fihtdc.batteryprotect
app_79    277   95    259180 36696 ffffffff 6fd0eb8c S com.android.launcher
system    281   95    207336 18228 ffffffff 6fd0eb8c S com.android.settings
app_19    310   95    236472 23296 ffffffff 6fd0eb8c S com.google.process.gapps
root      378   2     0      0     802c35f0 00000000 S loop1
system    380   1     636    232   80161874 6fd0d91c S /system/bin/sh
root      410   2     0      0     7f014060 00000000 S WD_Thread
root      411   2     0      0     803cc708 00000000 S ksdioirqd/mmc1
root      412   2     0      0     7f014858 00000000 S MC_Thread
root      413   2     0      0     7f014388 00000000 S TX_Thread
log       421   1     572    276   802895f0 6fd0d91c S /system/bin/logwrapper
wifi      422   421   2084   832   80168c10 6fd0dce4 S /system/bin/wpa_supplicant
app_88    430   95    214876 28036 ffffffff 6fd0eb8c S com.google.android.apps.listen
app_47    464   95    204016 16064 ffffffff 6fd0eb8c S android.process.media
root      505   2     0      0     802c35f0 00000000 S loop0
root      507   2     0      0     800f0434 00000000 S kdmflush
root      519   2     0      0     800f0434 00000000 S kcryptd_io
root      520   2     0      0     800f0434 00000000 S kcryptd
system    536   1     3604   764   ffffffff 6fd0e22c S /system/bin/icdr-auto
app_32    541   95    206572 17340 ffffffff 6fd0eb8c S android.process.acore
root      547   2     0      0     802c35f0 00000000 S loop2
root      550   2     0      0     800f0434 00000000 S kdmflush
root      551   2     0      0     800f0434 00000000 S kcryptd_io
root      552   2     0      0     800f0434 00000000 S kcryptd
root      640   2     0      0     802c35f0 00000000 S loop3
root      641   2     0      0     800f0434 00000000 S kdmflush
root      642   2     0      0     800f0434 00000000 S kcryptd_io
root      643   2     0      0     800f0434 00000000 S kcryptd
root      658   2     0      0     802c35f0 00000000 S loop4
root      659   2     0      0     800f0434 00000000 S kdmflush
root      660   2     0      0     800f0434 00000000 S kcryptd_io
root      661   2     0      0     800f0434 00000000 S kcryptd
root      665   2     0      0     802c35f0 00000000 S loop5
root      667   2     0      0     800f0434 00000000 S kdmflush
root      668   2     0      0     800f0434 00000000 S kcryptd_io
root      669   2     0      0     800f0434 00000000 S kcryptd
root      694   2     0      0     802c35f0 00000000 S loop6
root      695   2     0      0     800f0434 00000000 S kdmflush
root      696   2     0      0     800f0434 00000000 S kcryptd_io
root      697   2     0      0     800f0434 00000000 S kcryptd
root      715   2     0      0     802c35f0 00000000 S loop7
root      716   2     0      0     800f0434 00000000 S kdmflush
root      717   2     0      0     800f0434 00000000 S kcryptd_io
root      718   2     0      0     800f0434 00000000 S kcryptd
root      729   2     0      0     802c35f0 00000000 S loop8
root      730   2     0      0     800f0434 00000000 S kdmflush
root      731   2     0      0     800f0434 00000000 S kcryptd_io
root      732   2     0      0     800f0434 00000000 S kcryptd
root      733   2     0      0     802c35f0 00000000 S loop9
root      734   2     0      0     800f0434 00000000 S kdmflush
root      735   2     0      0     800f0434 00000000 S kcryptd_io
root      736   2     0      0     800f0434 00000000 S kcryptd
root      761   2     0      0     802c35f0 00000000 S loop10
root      762   2     0      0     800f0434 00000000 S kdmflush
root      763   2     0      0     800f0434 00000000 S kcryptd_io
root      764   2     0      0     800f0434 00000000 S kcryptd
root      793   2     0      0     802c35f0 00000000 S loop11
root      794   2     0      0     800f0434 00000000 S kdmflush
root      795   2     0      0     800f0434 00000000 S kcryptd_io
root      796   2     0      0     800f0434 00000000 S kcryptd
root      827   2     0      0     802c35f0 00000000 S loop12
root      830   2     0      0     800f0434 00000000 S kdmflush
root      831   2     0      0     800f0434 00000000 S kcryptd_io
root      832   2     0      0     800f0434 00000000 S kcryptd
root      834   2     0      0     802c35f0 00000000 S loop13
root      843   2     0      0     800f0434 00000000 S kdmflush
root      845   2     0      0     800f0434 00000000 S kcryptd_io
root      847   2     0      0     800f0434 00000000 S kcryptd
root      853   2     0      0     802c35f0 00000000 S loop14
root      857   2     0      0     800f0434 00000000 S kdmflush
root      859   2     0      0     800f0434 00000000 S kcryptd_io
root      860   2     0      0     800f0434 00000000 S kcryptd
root      878   2     0      0     802c35f0 00000000 S loop15
root      880   2     0      0     800f0434 00000000 S kdmflush
root      883   2     0      0     800f0434 00000000 S kcryptd_io
root      886   2     0      0     800f0434 00000000 S kcryptd
root      934   1     4344   204   ffffffff 000081e4 S emacsclient
root      935   1     4344   204   ffffffff 000081e4 S emacs
root      936   1     4344   204   ffffffff 000081e4 S /sbin/adbd
app_88    1462  95    258340 17052 ffffffff 6fd0eb8c S com.google.android.apps.listen:remote
root      1555  1     564    232   804108c8 6fd0e54c S /system/bin/debuggerd
app_76    1568  95    257376 18728 ffffffff 6fd0eb8c S com.google.android.apps.maps
app_102   1977  95    203256 16388 ffffffff 6fd0eb8c S com.googlecode.mindbell:remote
app_108   2349  95    203384 15984 ffffffff 6fd0eb8c S jp.gr.java_conf.wire_dev.UnKeyLockerService
system    2419  380   780    280   8010ff88 6fd0d91c S cat
app_80    2429  95    217660 20068 ffffffff 6fd0eb8c S net.artifix.pomodroido.free
app_19    3533  95    216128 17456 ffffffff 6fd0eb8c S com.google.android.gcm
app_70    3960  95    206252 16832 ffffffff 6fd0eb8c S com.android.providers.calendar
app_105   5190  95    219824 22112 ffffffff 6fd0eb8c S com.adylitica.android.DoItTomorrow
app_111   5343  95    244104 27132 ffffffff 6fd0eb8c S com.evernote
app_68    5359  95    243748 23112 ffffffff 6fd0eb8c S com.android.vending
app_76    5396  95    233592 25360 ffffffff 6fd0eb8c S com.google.android.apps.maps:GoogleLocationService
app_76    5411  95    223980 22636 ffffffff 6fd0eb8c S com.google.android.apps.maps:FriendService
app_76    5418  95    226228 24392 ffffffff 6fd0eb8c S com.google.android.apps.maps:LocationFriendService
app_118   5429  95    203108 14056 ffffffff 6fd0eb8c S com.robbieone.plum
app_107   5648  95    207148 16020 ffffffff 6fd0eb8c S com.caynax.hourlychime
dhcp      5724  1     744    384   80168c10 6fd0e9fc S /system/bin/dhcpcd
app_29    5752  95    205392 15348 ffffffff 6fd0eb8c S com.google.android.apps.uploader
app_112   5762  95    202988 15116 ffffffff 6fd0eb8c S ru.org.amip.ClockSync
app_74    5772  95    208904 19828 ffffffff 6fd0eb8c S com.android.email
app_99    5793  95    221152 22160 ffffffff 6fd0eb8c S com.wunderground.android.weather
root      5914  936   632    324   800dd0f0 6fd0e82c S /system/bin/sh
root      5916  5914  784    340   00000000 6fd0d91c R ps
app_64    14450 95    222352 22536 ffffffff 6fd0eb8c S com.google.android.gm
app_81    14458 95    215644 17360 ffffffff 6fd0eb8c S com.google.android.apps.unveil
app_115   22449 95    219336 21816 ffffffff 6fd0eb8c S im.doit.pro""".split('\n')
android_line = "app_115   22449 95    219336 21816 ffffffff 6fd0eb8c S im.doit.pro"
android_process = 'im.doit.pro'
android_pid = '22449'


class TestPs(unittest.TestCase):
    def setUp(self):        
        self.logger = MagicMock()
        self.connection = MagicMock()
        self.ps = PsCommand(connection=self.connection)
        self.ps._logger = self.logger
        return
    
    def test_constructor(self):
        """
        Does the constructor have the expected signature?
        """
        connection=MagicMock()
        ps = PsCommand(connection=connection)
        self.assertEqual(ps.connection, connection)
        return

    @raises(CommandError)
    def test_wrong_command(self):
        """
        Does the PsCommand raise a CommandError if ``ps`` isn't installed?
        """
        self.ps.check_errors('ps: command not found')
        return

    @raises(CommandError)
    def test_wrong_command_nexus(self):
        """
        Does the wrong-command expression match a nexus 7 error message?
        """
        self.ps.check_errors('/system/bin/sh: ps: not found')
        return

    @raises(CommandError)
    def test_bad_argument(self):
        """
        Does PsCommand raise a CommandError if a bad command is given?
        """
        line = 'error: unsupported SysV option'
        self.ps.check_errors(line)
        return


    def test_bad_argument_android(self):
        """
        Does PsCommand raise a CommandError if a bad command is given on an Android (no)"
        """
        line = 'USER     PID   PPID  VSIZE  RSS     WCHAN    PC         NAME'
        self.ps.check_errors(line)
        return

    @raises(CommandError)
    def test_standard_error(self):
        """
        Does an error from standard error get passed to the checker?
        """
        self.connection.ps.return_value = [''], ['ps: command not found']
        for line in self.ps():
            pass
        return

    def test_no_processes_found(self):
        """
        Is a warning raised if no processes are found?
        """
        self.connection.ps.return_value = ['USER     PID   PPID  VSIZE  RSS     WCHAN    PC         NAME'], ['']
        self.connection.operating_system = OperatingSystem.android
        for line in self.ps():
            pass
        self.logger.warning.assert_called_with("No processes found, check `ps `")
        self.logger.debug.assert_called_with('USER     PID   PPID  VSIZE  RSS     WCHAN    PC         NAME')
        return


class TestPsGrep(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.test_process = 'spotify'
        self.test_pid = '4084'
        self.grep = PsGrep(connection=self.connection, process=self.test_process)
        return

    def test_call(self):
        """
        Does the `__call__` return all the matching PIDs?
        """
        self.connection.ps.return_value = (ubuntu_lines, [''])
        
        for count, pid in enumerate(self.grep('getty')):
            self.assertEqual(getty_pids[count], pid)
        self.assertEqual(count+1, len(getty_pids))
        return

    def test_constructor(self):
        """
        Does the constructor have the expected signature?
        """
        process = ''.join([random.choice(ascii_letters) for letter in range(random.randrange(10))])
        connection=MagicMock()
        grep = PsGrep(connection=connection, process=process, field=ProcessGrepEnum.process)
        self.assertEqual(grep.connection, connection)
        self.assertEqual(grep.process, process)
        self.assertEqual(grep.field, ProcessGrepEnum.process)
        return

    def test_unmatched(self):
        """
        Does the expression not match lines similar to the process-lines?
        """
        self.assertIsNone(self.grep.expression.search(first_ubuntu_line))
        return


    def test_call_parameter(self):
        """
        Does passing in the name of the process override the process passed in on construction?
        """
        found = False
        self.grep.connection.ps.return_value = (ubuntu_lines, StringIO(''))
        for pid in self.grep('emacs'):
            self.assertEqual(pid, '22165')
            found = True
        self.assertTrue(found)
        return

    def test_expression(self):
        """
        Does the expression match the output lines correctly?
        """
        for index, line in enumerate(ubuntu_lines):
            self.grep._expression = None
            self.grep.process = ubuntu_process_names[index]
            match = self.grep.expression.search(line)
            self.assertIsNotNone(match, msg="Line: `{0}` did not match process {1} with expression '{2}'".format(line,
                                                                                           self.grep.process,
                                                                                           self.grep.expression.pattern))
            pid_map = match.groupdict()
            self.assertEqual(ubuntu_process_list[index], pid_map[ProcessGrepEnum.pid],
                             msg="expected: {0}, actual {1}".format(ubuntu_process_list[index],
                                                                    pid_map[ProcessGrepEnum.pid]))
        return

    def test_name_field(self):
        """
        If the process-name-field is set, will it yield the names instead of PID?
        """
        found = False
        self.grep.connection.ps.return_value = (ubuntu_lines, [''])
        self.grep.field = ProcessGrepEnum.process
        for pid in self.grep(self.test_process):
            self.assertEqual(pid, self.test_process,
                             msg="Expected: {0}, Actual: {1}".format(self.test_process,
                                                                     pid))
            found = True
        self.assertTrue(found)
        return

    def test_change_connection(self):
        """
        Does the PsCommand get a new connection if you change the PsGrep's connection?
        """
        self.assertEqual(self.grep.connection, self.connection,
                         msg="setUp connection not setting up")
        self.assertEqual(self.grep.process_query.connection, self.connection,
                         msg='setUp connection not passed to ps')
        connection_2 = MagicMock()
        self.grep.connection = connection_2
        self.assertEqual(self.grep.connection, connection_2,
                         msg="grep connection not set")
        self.assertEqual(self.grep.process_query.connection,
                         connection_2)
        return
    def test_android_output(self):
        """
        Does it work with android output?
        """
        self.connection.ps.return_value = android_output, [""]
        self.connection.operating_system = operating_systems.android
        self.grep.connection = self.connection
        called = False
        for pid in self.grep('emacs'):
            self.assertEqual(pid, '935')
            called = True
        self.assertTrue(called)
        return

    def test_android_expression(self):
        """
        Can the expression get the PID?
        """
        self.connection.operating_system = operating_systems.android
        self.grep.connection = self.connection
        self.grep.process = android_process
        match = self.grep.expression.search(android_line)
        self.assertIsNotNone(match,
                             msg="Didn't match '{0}'".format(android_line))
        return

    def test_arguments(self):
        """
        Do the arguments change when the connection changes?
        """
        # linux by default
        self.connection.operating_system = OperatingSystem.linux
        self.grep.connection = self.connection
        self.assertEqual('-e', self.grep.process_query.arguments)

        #try android
        self.connection.operating_system = OperatingSystem.android
        self.grep.connection = self.connection
        self.assertEqual('', self.grep.process_query.arguments)
        return
