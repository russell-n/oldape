# Copyright 2012 Russell Nakamura
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
A module to watch packets and bytes received on an interface.

The File-expression watchers differ from the catters and pollsters in that they:

 * repeatedly cat the file at set intervals, unlike logcatters
 * send output directly to file without making calculations (unlike proc-pollsters)
"""
#python standard library
from abc import ABCMeta, abstractproperty
from time import time, sleep
from collections import defaultdict


#apetools
from basepollster import BasePollster
from apetools.commons.errors import ConfigurationError
from apetools.parsers import oatbran

NOT_AVAILABLE = 'NA'


class BaseFileexpressionwatcher(BasePollster):
    """
    A class to repeatedly cat a file and output a csv-line. Unlike regular pollster, does no calculation
    """
    __metaclass__ = ABCMeta
    def __init__(self, *args, **kwargs):
        """
        :param:

        - `output`: A writeable file-like object
        - `interface`: The name of the interface to watch
        - `interval`: seconds between samples
        - `connection`: the connection to the device to watch
        - `name`: the name of the file to watch
        - `expression`: A regular expression with groups to match the output
        """
        super(BaseFileexpressionwatcher, self).__init__(*args, **kwargs)
        self._logger = None
        self._connection = None
        self._expression_keys = None
        self._stopped = None
        self._header = None
        return

    @property
    def stopped(self):
        """
        :rtype: Boolean
        :return: True if self.stop is set.
        """
        if self.event is not None:
            return self.event.is_set()
        return False


    @property
    def name(self):
        """
        :return: the path to the file to cat
        """
        return self._name

    @name.setter
    def name(self, new_name):
        """
        :param:

         - `new_name`: path of the file to cat

        :raise: ConfigurationError if the new_name is none
        """
        if new_name is None:
            raise ConfigurationError("FileExpression watcher requires the name parameter")
        return

    @abstractproperty
    def expression_keys(self):
        """
        :return: list of group-keys to order the output
        """
        return self._expression_keys

    @property
    def connection(self):
        """
        :return: the node connection
        """
        if self._connection is None:
            self._connection = self.device.connection
        return self._connection

    def run(self):
        """
        Repeatedly cats file self.name and saves matching output
        """
        if self.use_header:
            self.output.writeline(self.header)
       
        while not self.stopped:                
            start = time()
            data = defaultdict(lambda:NOT_AVAILABLE)
            output, error = self.connection.cat(self.name)
            for line in output:
                match = self.regex.search(line)
                if match:                    
                    match = match.groupdict()
                    for key, value in match.iteritems():
                        if value is not None:
                            data[key] = value
            data_out = ",".join([data[key] for key in self.expression_keys])
            self.output.write("{0},{1}\n".format(self.timestamp.now, data_out))
            try:
                sleep(self.interval - (time() - start))
            except IOError:
                self.logger.debug("cat {0} took more than one second".format(self.name))
        return
# end class BaseFileexpressionWatcher

class BatteryWatcher(BaseFileexpressionwatcher):
    """
    Watches the battery data from a proc file
    """
    def __init__(self, *args, **kwargs):
        super(BatteryWatcher, self).__init__(*args, **kwargs)
        return

    @property
    def header(self):
        """
        :return: the header to use in files
        """
        if self._header is None:
            self._header = "status,voltage,current,temp,charge,health,capacity"
        return self._header

    @property
    def expression_keys(self):
        """
        :return: list of group-dict keys in order 
        """
        if self._expression_keys is None:
            self._expression_keys = self.header.split(',')
        return self._expression_keys

    @property
    def expression(self):
        """
        :return: regular expression to match the output
        """
        if self._expression is None:
            status = oatbran.GROUP("STATUS=" + oatbran.NAMED(n='status', e=oatbran.LETTERS))
            voltage = oatbran.GROUP("VOLTAGE_NOW=" + oatbran.NAMED(n="voltage", e= oatbran.INTEGER))
            current = oatbran.GROUP("CURRENT_NOW=" + oatbran.NAMED(n='current', e=oatbran.INTEGER))
            temp = oatbran.GROUP("TEMP="+ oatbran.NAMED(n='temp', e=oatbran.INTEGER))
            charge = oatbran.GROUP("CHARGE_NOW=" + oatbran.NAMED(n='charge', e=oatbran.INTEGER))
            health = oatbran.GROUP("HEALTH=" + oatbran.NAMED(n='health', e=oatbran.LETTERS))
            capacity = oatbran.GROUP("CAPACITY=" + oatbran.NAMED(n='capacity', e=oatbran.INTEGER))
            self._expression = oatbran.OR.join([status, voltage, current, temp, charge, health,
                                                capacity])
        return self._expression
#end class BatteryWatcher       
