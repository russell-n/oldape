The Storage Output
==================

.. currentmodule:: apetools.commons.storageoutput

This module holds (a) class(es) to send lines to files.



.. _storage-output:

The Storage Output
------------------

The `StorageOutput` is a class to maintain path information so that users of it can focus on file-names only.

.. autosummary::
   :toctree: api

   StorageOutput

.. uml::

   StorageOutput -|> BaseClass
   StorageOutput : __init__(output_folder, timestamp_format)
   StorageOutput : path
   StorageOutput : extend_path(subdirectory)
   StorageOutput : get_filename(filename, subdir, mode)
   StorageOutput : open(filename, subdir, mode)
   StorageOutput : write(line)
   StorageOutput : writeline(line)
   StorageOutput : writelines(lines)
   StorageOutput : copy(source, subdir)
   StorageOutput : move(source, subdir)


Example::

   storage = StorageOutput("data")
   out_file = storage.open('trial_1.txt')
   for line in data:
       out_file.write(line)

   storage.copy('config.ini', 'configs')
   storage.move('operation.log', 'logs')
   out_name = storage.get_filename('test.iperf', 'raw_iperf')
   sftp.get('test.iperf', out_name)
   
       
