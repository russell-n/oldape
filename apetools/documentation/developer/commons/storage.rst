Storage Output
==============

The `StorageOuput` acts somewhat like a writeable file while maintaining a memory of the result folder path and opened filename.

.. uml::

   StorageOuput: String path
   StorageOuput: StorageOutput open(String filename, [extension])
   StorageOuput: write(String line)
   StorageOuput: writeline(String line)
   StorageOuput: writelines(Iterator lines)

Although it is an object in and of itself, it doesn't have an open file until the `open` method is called. Since the `open` method returns a cloned `StorageOutput`, you can use it to open new StorageOutput outputs or to write to the opened file.
