Output
======

The `Output` classes are attempts to create *duck-typed* read-only file-like objects.

.. _standardoutputuml:

StandardOutput
--------------

The `StandardOutput` is a read-only file-like object.

.. uml::

   StandardOutput: Queue queue
   StandardOutput: GeneratorType iterator
   StandardOutput: GeneratorType __iter__()
   StandardOutput: StringType readline(FloatType timeout)
   StandardOutput: ListType readlines()
   StandardOutput: StringType read()

.. _validatingoutputuml:

ValidatingOutput
----------------

The `ValidatingOutput` is similar to the `StandardOutput` (and is intended to take `StandardOutput` as an argument to the constructor) but also requires a validatin-method which it uses to check lines of output.

.. uml::

   ValidatingOutput: GeneratorType lines
   ValidatingOutput: MethodType validate
   ValidatingOutput: Queue queue
   ValidatingOutput: GeneratorType iterator
   ValidatingOutput: GeneratorType __iter__()
   ValidatingOutput: StringType readline(FloatType timeout)
   ValidatingOutput: ListType readlines()
   ValidatingOutput: StringType read()

