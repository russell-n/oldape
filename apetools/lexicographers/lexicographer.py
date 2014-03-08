"""
A module to hold a translator of configurations to configuration map.

The Lexicographers used to check configurations and do conversions,
but more has been pushed to the builders and ConfigurationMap
"""
# apetools Libraries
from apetools.baseclass import BaseClass
from apetools.commons.generators import ShallowFind
from apetools.commons import errors
import configurationmap 

class Lexicographer(BaseClass):
    """
    A Lexicographer yields configuration Maps.
    """
    def __init__(self, glob, *args, **kwargs):
        """
        :param:

         - `glob`: a file glob to match the config file.
        """
        super(Lexicographer, self).__init__(*args, **kwargs)
        self.logger.debug("Lexicographer using glob: {0}".format(glob))
        self.glob = glob
        self._maps = None
        self._filenames = None
        self._finder = None
        return

    @property
    def filenames(self):
        """
        Generates filenames that match self.glob.
        This is made a parameter so other classes can retrieve the list.
        
        :yield: next name
        """
        found = False
        for file_name in self.finder:
            found = True            
            yield file_name
        if not found:
            raise errors.ArgumentError(("Your glob for the config file ('{0}') doesn't match any file in"
                                        " directory {1}"
                                        " which contains ({2})").format(self.finder.glob,
                                                                    self.finder.path,
                                                                    self.finder.filenames))
        return

    @property
    def finder(self):
        """
        :return: shallow-find filename generator
        """
        if self._finder is None:
            self._finder = ShallowFind(glob=self.glob)
        return self._finder
    
    def __iter__(self):
        """
        :yield: TestParameters namedtuple
        """
        for name in self.filenames:
            yield configurationmap.ConfigurationMap(name)
        return 

# end class Lexicographer

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    l = Lexicographer("tot.ini")
    
    for parameter in l.parameters:
        print parameter.iperf
