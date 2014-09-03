
# python regular expressions
import re

#apetools
from apetools.baseclass import BaseClass
from apetools.commons.errors import CommandError
from apetools.parsers import oatbran
from apetools.commands.basecommand import BaseProcessCommand, BaseProcessGrep
from apetools.commands.basecommand import ProcessCommandEnum, ProcessGrepEnum


class TopCommandError(CommandError):
    """
    A command to raise if there is a problem with the top command.
    """


class TopCommand(BaseProcessCommand):
    """
    The Top Command issues commands and watches for errors
    """
    def __init__(self, *args, **kwargs):
        """
        TopCommand Constructor

        :param:

         - `connection`: A connection to the device
         - `arguments`: the arguments to get output from ``top``
        """
        super(TopCommand, self).__init__(*args, **kwargs)
        return

    @property
    def arguments(self):
        """
        the arguments for the ``top`` command
        """
        if self._arguments is None:
            self._arguments = '-l 1'
        return self._arguments

    @property
    def error_expression(self):
        """
        Holds the expression to match error messages

        :return: compiled regular expression to match error messages
        """
        if self._error_expression is None:
            missing = oatbran.NAMED(n=ProcessCommandEnum.missing,
                                    e=oatbran.SPACES.join([self.command+':',
                                                           'command',
                                                           'not',
                                                           'found']))
            bad_arg = oatbran.NAMED(n=ProcessCommandEnum.bad_arg,
                                    e=oatbran.SPACES.join([self.command + ":",
                                                           "Unrecognized",
                                                           'or',
                                                           'missing',
                                                           'option']))
            self._error_expression = re.compile(missing + oatbran.OR + bad_arg)
        return self._error_expression

    def run(self):
        """
        Calls ``top`` on the connection

        :return: output from the connections call to top (stdout, stderr)
        """
        return self.connection.top(self.arguments)

    @property
    def command(self):
        """
        `top`
        """
        if self._command is None:
            self._command = 'top'
        return self._command


class TopGrep(BaseProcessGrep):
    """
    The Top command adapted to extract process IDs.
    """
    def __init__(self, *args, **kwargs):
        """
        TopGrep Constructon

        :param:
        
         - `process`: The name of the process to get (if not set pass into call())
        """
        super(TopGrep, self).__init__(*args, **kwargs)
        return
            
    @property
    def process_query(self):
        """
        The ``top`` command

        :return: TopCommand to return output from the ``top`` command.
        """
        if self._process_query is None:
            self._process_query = TopCommand(connection=self.connection)
        return self._process_query

    @property
    def expression(self):
        """
        An expression to parse a single line of output

        :return: compiled regular expression to get PID
        """
        if self._expression is None:
            if self.process is None:
                raise TopGrepError("self.process must be set")
            self._expression = re.compile(oatbran.SPACES.join([
                oatbran.NAMED(n=ProcessGrepEnum.pid,
                              e=oatbran.INTEGER+oatbran.ONE_OR_MORE),
                              oatbran.NAMED(n=ProcessGrepEnum.process,
                                            e=self.process),
                              oatbran.REAL + "%",
                              oatbran.NOT_SPACES,
                              oatbran.INTEGER,
                              oatbran.INTEGER + "\+",
                              oatbran.INTEGER,
                              oatbran.INTEGER,
                              oatbran.INTEGER,
                              oatbran.INTEGER + '[KBMG]\+',
                              oatbran.INTEGER + '[KBMG]\+']))
        return self._expression

# end class TopGrep    


#python standard library
import unittest
from StringIO import StringIO
import random
from string import ascii_letters

# third-party
from nose.tools import raises
from mock import MagicMock


first_line = "Processes:  49 total, 1 running, 1 stuck, 47 sleeping... 223 threads    23:00:00"
test_output = """"Processes:  49 total, 1 running, 1 stuck, 47 sleeping... 223 threads    23:00:00

Load Avg:  0.07,  0.05,  0.06    CPU usage: 50.00% user,  0.00% sys, 50.00% idle
SharedLibs: num =    0, resident =     0 code,     0 data,     0 linkedit.
MemRegions: num =     0, resident =     0 +     0 private,     0 shared.
PhysMem:   68M wired,  120M active,   15M inactive,  285M used,  218M free.
VM: 14G + 0   47836(0) pageins, 0(0) pageouts

  PID COMMAND      %CPU   TIME   #TH #PRTS #MREGS  RPRVT  RSHRD  RSIZE  VSIZE
 1153 top          0.0%  0:00.03   1    20+     0      0      0   684K+  267M+
 1152 sshd         0.0%  0:00.16   1    18+     0      0      0  1500K+  268M+
 1151 launchprox   0.0%  0:00.01   1    18+     0      0      0   408K+  266M+
  952 geod         0.0%  0:00.08   2    30+     0      0      0  1456K+  295M+
  812 SCHelper     0.0%  0:26.09   4    34+     0      0      0   952K+  277M+
  748 iperf        0.0%  0:00.47   1     9+     0      0      0   228K+  267M+
  493 mediaremot   0.0%  0:04.89   3    47+     0      0      0  1636K+  278M+
  492 MobileTime   0.0%  0:01.60  11    93+     0      0      0    21M+  347M+
  489 AppStore     0.0%  0:03.40  14   156+     0      0      0    28M+  441M+
  275 coresymbol   0.0%  0:00.02   2    21+     0      0      0   660K+  277M+
  227 Preference   0.0%  0:33.08   4   111+     0      0      0    11M+  317M+
  184 filecoordi   0.0%  0:00.02   2    27+     0      0      0  1080K+  277M+
  177 accountsd    0.0%  0:00.11   2    36+     0      0      0  1716K+  276M+
  176 MobileMail   0.0%  0:13.02   6   125+     0      0      0  7312K+  315M+
  174 tccd         0.0%  0:00.18   2    27+     0      0      0   976K+  277M+
  172 assetsd      0.0%  0:05.93   3    47+     0      0      0  3996K+  298M+
  167 xpcd         0.0%  0:00.03   3    27+     0      0      0   788K+  277M+
   96 emacsclient  0.0%  0:06.18   2    31+     0      0      0  1964K+  295M+
   98 emacs        0.0%  0:06.18   2    31+     0      0      0  1964K+  295M+
   99 lsd          0.0%  0:06.18   2    31+     0      0      0  1964K+  295M+
   97 distnoted    0.0%  0:00.08   2    34+     0      0      0  1108K+  295M+
   87 apsd         0.0%  0:23.01   5   115+     0      0      0  2548K+  296M+
   85 CommCenter   0.0%  0:06.91   5   108+     0      0      0  2800K+  280M+
   84 itunesstor   0.0%  1:32.98   5   107+     0      0      0  7204K+  301M+
   83 aggregated   0.0%  0:01.34   2    36+     0      0      0   624K+  277M+
   82 BlueTool     0.0%  0:00.06   2    25+     0      0      0   900K+  278M+
   81 networkd_p   0.0%  0:00.03   2    26+     0      0      0   656K+  277M+
   80 networkd     0.0%  0:01.95   2    61+     0      0      0  1328K+  277M+
   79 SpringBoar   0.0%  7:10.45  12   293+     0      0      0    25M+  360M+
   71 notifyd      0.0%  0:19.31   4    62+     0      0      0   848K+  278M+
   70 BTServer     0.0%  0:38.28   6    73+     0      0      0  2868K+  282M+
   65 kbd          0.0%  0:00.48   2    37+     0      0      0  3272K+  296M+
   61 backboardd   0.0%  2:07:12  12   577+     0      0      0  9884K+  406M+
   59 configd      0.0%  1:04.35   9   249+     0      0      0  2924K+  280M+
   58 AppleIDAut   0.0%  0:00.04   3    30+     0      0      0  1048K+  277M+
   56 fairplayd.   0.0%  0:06.59   2    32+     0      0      0  3400K+  285M+
   55 fseventsd    0.0%  0:03.50  18    67+     0      0      0  1308K+  284M+
   53 iaptranspo   0.0%  0:35.67   2    65+     0      0      0  1464K+  295M+
   52 imagent      0.0%  0:06.29   3    73+     0      0      0  2192K+  277M+
   50 locationd    0.0%  2:10.00   9   155+     0      0      0  5260K+  286M+
   48 mDNSRespon   0.0%  0:11.59   4    55+     0      0      0  1948K+  277M+
   46 mediaserve   0.0%  0:12.60  15   224+     0      0      0  5472K+  307M+
   42 deleted      0.0%  0:00.03   2    28+     0      0      0  1276K+  278M+
   41 backboardd   0.0%  2:07:12  12   577+     0      0      0  9884K+  406M+
   40 installd     0.0%  0:00.44   2    31+     0      0      0  1408K+  277M+
   38 lockdownd    0.0%  0:05.85   2    46+     0      0      0  1904K+  295M+
   31 powerd       0.0%  0:42.65   2    59+     0      0      0  1272K+  295M+
   29 timed        0.0%  0:05.93   3    49+     0      0      0  1908K+  295M+
   26 wifid        0.0%  7:10.17   4   106+     0      0      0  2484K+  296M+
   24 syslogd      0.0%  0:05.70   6    56+     0      0      0   852K+  279M+
   23 UserEventA   0.0% 23:15.66   9   214+     0      0      0  3468K+  300M+
    1 launchd      0.0%  1:10.80   3   330+     0      0      0  1140K+  277M+
""".split('\n')

sshd_line = ' 1152 sshd         0.0%  0:00.16   1    18+     0      0      0  1500K+  268M+'
sshd_process = '1152'
sshd_name = 'sshd'

process_output = """1153 top          2.2%  3:00.03   1    20+     0      0      0   684K+  267M+
 1152 sshd         0.0%  0:00.16   1    18+     0      0      0  1500K+  268M+
 1151 launchprox   0.0%  0:00.01   1    18+     0      0      0   408K+  266M+
  952 geod         0.0%  0:00.08   2    30+     0      0      0  1456K+  295M+
  812 SCHelper     0.0%  0:26.09   4    34+     0      0      0   952K+  277M+
  748 iperf        0.0%  0:00.47   1     9+     0      0      0   228K+  267M+
  493 mediaremot   0.0%  0:04.89   3    47+     0      0      0  1636K+  278M+
  492 MobileTime   0.0%  0:01.60  11    93+     0      0      0    21M+  347M+
  489 AppStore     0.0%  0:03.40  14   156+     0      0      0    28M+  441M+
  275 coresymbol   0.0%  0:00.02   2    21+     0      0      0   660K+  277M+
  227 Preference   0.0%  0:33.08   4   111+     0      0      0    11M+  317M+
  184 filecoordi   0.0%  0:00.02   2    27+     0      0      0  1080K+  277M+
  177 accountsd    0.0%  0:00.11   2    36+     0      0      0  1716K+  276M+
  176 MobileMail   0.0%  0:13.02   6   125+     0      0      0  7312K+  315M+
  174 tccd         0.0%  0:00.18   2    27+     0      0      0   976K+  277M+
  172 assetsd      0.0%  0:05.93   3    47+     0      0      0  3996K+  298M+
  167 xpcd         0.0%  0:00.03   3    27+     0      0      0   788K+  277M+
   96 emacsclient  0.0%  0:06.18   2    31+     0      0      0  1964K+  295M+
   98 emacs        0.0%  0:06.18   2    31+     0      0      0  1964K+  295M+
   99 lsd          0.0%  0:06.18   2    31+     0      0      0  1964K+  295M+
   97 distnoted    0.0%  0:00.08   2    34+     0      0      0  1108K+  295M+
   87 apsd         0.0%  0:23.01   5   115+     0      0      0  2548K+  296M+
   85 CommCenter   0.0%  0:06.91   5   108+     0      0      0  2800K+  280M+
   84 itunesstor   0.0%  1:32.98   5   107+     0      0      0  7204K+  301M+
   83 aggregated   0.0%  0:01.34   2    36+     0      0      0   624K+  277M+
   82 BlueTool     0.0%  0:00.06   2    25+     0      0      0   900K+  278M+
   81 networkd_p   0.0%  0:00.03   2    26+     0      0      0   656K+  277M+
   80 networkd     0.0%  0:01.95   2    61+     0      0      0  1328K+  277M+
   79 SpringBoar   0.0%  7:10.45  12   293+     0      0      0    25M+  360M+
   71 notifyd      0.0%  0:19.31   4    62+     0      0      0   848K+  278M+
   70 BTServer     0.0%  0:38.28   6    73+     0      0      0  2868K+  282M+
   65 kbd          0.0%  0:00.48   2    37+     0      0      0  3272K+  296M+
   61 backboardd   0.0%  2:07:12  12   577+     0      0      0  9884K+  406M+
   59 configd      0.0%  1:04.35   9   249+     0      0      0  2924K+  280M+
   58 AppleIDAut   0.0%  0:00.04   3    30+     0      0      0  1048K+  277M+
   56 fairplayd.   0.0%  0:06.59   2    32+     0      0      0  3400K+  285M+
   55 fseventsd    0.0%  0:03.50  18    67+     0      0      0  1308K+  284M+
   53 iaptranspo   0.0%  0:35.67   2    65+     0      0      0  1464K+  295M+
   52 imagent      0.0%  0:06.29   3    73+     0      0      0  2192K+  277M+
   50 locationd    0.0%  2:10.00   9   155+     0      0      0  5260K+  286M+
   48 mDNSRespon   0.0%  0:11.59   4    55+     0      0      0  1948K+  277M+
   46 mediaserve   0.0%  0:12.60  15   224+     0      0      0  5472K+  307M+
   42 deleted      0.0%  0:00.03   2    28+     0      0      0  1276K+  278M+
   41 backboardd   0.0%  2:07:12  12   577+     0      0      0  9884K+  406M+
   40 installd     0.0%  0:00.44   2    31+     0      0      0  1408K+  277M+
   38 lockdownd    0.0%  0:05.85   2    46+     0      0      0  1904K+  295M+
   31 powerd       0.0%  0:42.65   2    59+     0      0      0  1272K+  295M+
   29 timed        0.0%  0:05.93   3    49+     0      0      0  1908K+  295M+
   26 wifid        0.0%  7:10.17   4   106+     0      0      0  2484K+  296M+
   24 syslogd      0.0%  0:05.70   6    56+     0      0      0   852K+  279M+
   23 UserEventA   0.0% 23:15.66   9   214+     0      0      0  3468K+  300M+
    1 launchd      0.0%  1:10.80   3   330+     0      0      0  1140K+  277M+""".split('\n')

process_list="""1153
1152
1151
952
812
748
493
492
489
275
227
184
177
176
174
172
167
96
98
99
97
87
85
84
83
82
81
80
79
71
70
65
61
59
58
56
55
53
52
50
48
46
42
41
40
38
31
29
26
24
23
1""".split('\n')

process_names=[name.strip() for name in"""top
sshd         
launchprox   
geod         
SCHelper     
iperf        
mediaremot   
MobileTime   
AppStore     
coresymbol   
Preference   
filecoordi   
accountsd    
MobileMail   
tccd         
assetsd      
xpcd
emacsclient
emacs
lsd          
distnoted    
apsd         
CommCenter   
itunesstor   
aggregated   
BlueTool     
networkd_p   
networkd     
SpringBoar   
notifyd      
BTServer     
kbd          
backboardd   
configd      
AppleIDAut   
fairplayd.   
fseventsd    
iaptranspo   
imagent      
locationd    
mDNSRespon   
mediaserve   
deleted      
backboardd   
installd     
lockdownd    
powerd       
timed        
wifid        
syslogd      
UserEventA   
launchd
""".split('\n')]



test_line = '   61 backboardd   0.0%  2:07:12  12   577+     0      0      0  9884K+  406M+'
test_pid = '61'
test_process = 'backboardd'
test_pid_2 = '41'
expected_pid = {test_pid:test_pid,
                test_pid_2:test_pid_2}

class TestTop(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.connection = MagicMock()
        self.top = TopCommand(connection=self.connection)
        self.top._logger = self.logger
        return
    
    def test_constructor(self):
        """
        Does the constructor have the expected signature?
        """
        connection=MagicMock()
        top = TopCommand(connection=connection)
        self.assertEqual(top.connection, connection)
        return

    @raises(CommandError)
    def test_wrong_command(self):
        """
        Does the TopCommand raise a TopCommandError if top isn't installed?
        """
        self.top.check_errors('-sh: top: command not found')
        return

    @raises(CommandError)
    def test_bad_argument(self):
        """
        Does TopCommand raise a TopCommandError if a bad command is given?
        """
        line = 'top: Unrecognized or missing option q'
        match = self.top.error_expression.search(line)
        error_map = match.groupdict()
        self.top.check_errors(line)
        return

    @raises(CommandError)
    def test_standard_error(self):
        """
        Does an error from standard error get passed to the checker?
        """
        self.connection.top.return_value = [''], ['-sh: top: command not found']
        for line in self.top():
            pass
        return


class TestTopGrep(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()        
        self.grep = TopGrep(connection=self.connection, process=test_process)
        return

    def test_call(self):
        """
        Does the `__call__` return all the matching PIDs?
        """
        self.connection.top.return_value = (test_output, [''])
        
        for count, pid in enumerate(self.grep(test_process)):
            self.assertEqual(expected_pid[pid], pid)
        self.assertEqual(count+1, len(expected_pid))
        return

    def test_constructor(self):
        """
        Does the constructor have the expected signature?
        """
        process = ''.join([random.choice(ascii_letters) for letter in range(random.randrange(10))])
        connection=MagicMock()
        grep = TopGrep(connection=connection, process=process, field=ProcessGrepEnum.process)
        self.assertEqual(grep.connection, connection)
        self.assertEqual(grep.process, process)
        self.assertEqual(grep.field, ProcessGrepEnum.process)
        return

    def test_unmatched(self):
        """
        Does the expression not match lines similar to the process-lines?
        """
        self.assertIsNone(self.grep.expression.search(first_line))
        return


    def test_call_parameter(self):
        """
        Does passing in the name of the process override the process passed in on construction?
        """
        found = False
        self.grep.connection.top.return_value = (process_output, StringIO(''))
        for pid in self.grep('sshd'):
            self.assertEqual(pid, sshd_process)
            found = True
        self.assertTrue(found)
        return

    def test_expression(self):
        """
        Does the expression match the output lines correctly?
        """
        for index, line in enumerate(process_output):
            self.grep._expression = None
            self.grep.process = process_names[index]
            match = self.grep.expression.search(line)
            self.assertIsNotNone(match, msg="Line: `{0}` did not match".format(line))
            pid_map = match.groupdict()
            self.assertEqual(process_list[index], pid_map[ProcessGrepEnum.pid],
                             msg="expected: {0}, actual {1}".format(process_list[index],
                                                                    pid_map[ProcessGrepEnum.pid]))
        return

    def test_name_field(self):
        """
        If the process-name-field is set, will it yield the names instead of PID?
        """
        found = False
        self.grep.connection.top.return_value = (process_output, [''])
        self.grep.field = ProcessGrepEnum.process
        for pid in self.grep('sshd'):
            self.assertEqual(pid, sshd_name)
            found = True
        self.assertTrue(found)
        return

    def test_change_connection(self):
        """
        Does the TopCommand get a new connection if you change the TopGrep's connection?
        """
        self.assertEqual(self.grep.connection, self.connection,
                         msg="setUp connection not setting up")
        self.assertEqual(self.grep.process_query.connection,
                         self.connection,
                         msg='setUp connection not passed to top')
        connection_2 = MagicMock()
        self.grep.connection = connection_2
        self.assertEqual(self.grep.connection, connection_2,
                         msg="grep connection not set")
        self.assertEqual(self.grep.process_query.connection,
                         connection_2)
        return

    def test_substring(self):
        """
        Does it only match complete strings, not substrings of other processes?
        """
        self.connection.top.return_value = test_output, [""]
        called = False
        for pid in self.grep('emacs'):
            self.assertEqual(pid, '98')
            called = True
        self.assertTrue(called)
