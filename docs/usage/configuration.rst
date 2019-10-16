Configuration
=============

Using the ``configuration`` module the chassis can be configured,
but it can also be used for application-specific configuration.

When you make a new instance of the ``ConfigParser`` it will contain
a property ``config`` that contains all the configuration.

The dictionary is filled based on following priority:

#. command line arguments (*not implemented*)
#. environment variables (*not implemented*)
#. config.yml file in the project root folder
#. default values


.. code-block:: python

    from viaa.configuration import ConfigParser

    config = ConfigParser()


Example of a ``config.yml`` file.

.. code-block:: yaml

    viaa:
      logging:
        level: 40
    application:
      throttle_time: 10

API
---

.. automodule:: viaa.configuration
    :members:
