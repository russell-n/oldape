
from apetools.commons.reporter import Reporter


class ReportBuilder(object):
    """
    A Report builder builds an instance of a Reporter
    """
    def __init__(self, parameters, storage):
        """
        :param:

         - `parameters`: parameters needed to build a reporter
         - `storage`: a file opener
        """
        self.parameters = parameters
        self.storage = storage
        self._instance = None
        return

    @property
    def instance(self):
        """
        :return: instance of Reporter
        """
        if self._instance is None:
            self._instance = Reporter(header=self.parameters.header,
                                      filename=self.parameters.filename,
                                      storage = self.storage,
                                      delimiter=self.parameters.delimiter,
                                      missing= self.parameters.missing)
        return self._instance
# end class ReportBuilder
