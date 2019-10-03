# VIAA Chassis

**Important: this library is currently only available on the internal VIAA PyPI, make sure to update your [pip-config](https://pip.pypa.io/en/stable/user_guide/#config-file)**


In this repository solutions for cross-cutting concerns will be gathered. This is a work in progress and it will always be...

Currently implemented:
- Configuration
- Observability
  - Logging

## Usage
Start by installing the library with `pip install viaa`, it is located on the VIAA PyPI.

### Configuration

You can use the configuration to configure the other modules in the chassis. 
You call the ConfigParser and you will get a config dictionary containing all the keys and values. 
The dictionary is filled based on following priority:

1. command line arguments (*not implemented*)
2. environment variables (*not implemented*)
3. config.yml file in the project root folder
4. default values

An example config file is included in this repository, see `config.yml.example`.

```python
from viaa.configuration import ConfigParser

config = ConfigParser()
```

### Logging

The logging interface is made to resemble the Python standard logging as close as possible. 
The biggest difference is that you can pass a config object when getting a logger instance.
**ALL** logging will go to `stdout` as a JSON string, this means that logging by external packages will be formatted aswell.
Formatting all logs as JSON makes it easier to parse the logs in other applications.

Running following example: 

```python
import logging as basic_logging
from viaa.observability import logging
from viaa.configuration import ConfigParser

example_dictionary = {"test_key": "test_value"}

config = ConfigParser()
logger = logging.get_logger(__name__, config)

basic_logger = basic_logging.getLogger()

logger.warning("Hello world!", string="extra info", dictionary=example_dictionary)
basic_logger.warning("basic log")
```

Will print: 
```
{"message": "Hello world!", "string": "extra info", "dictionary": {"test_key": "test_value"}, "logger": "__main__", "level": "warning", "timestamp": "2019-10-03T12:52:21.857624Z", "source": ".\\hello.py:<module>:12"}   
{"message": "basic log"}
```


## Tutorial

### A tiny “Hello, World” service

#### Prerequisites

This tutorial expects you to be familiar with Python and the basics of web application development. We will use  [Python 3.7](https://www.python.org/)  and  [virtual environments](https://virtualenv.pypa.io/en/stable/). To get set up, see  [this guide on installing Python](https://realpython.com/installing-python/).

#### Preparing the environment

First, let’s create a folder and virtual environment to isolate the code and dependencies for this project.

```shell
$ virtualenv ./<project-name>
$ cd ./<project-name>
$ source bin/activate
$ pip install viaa
```

Now let’s write a tiny "Hello World" service, open your editor and put the following in `helloworld.py`:

```python
from viaa.observability import logging
from viaa.configuration import ConfigParser

config = ConfigParser()
logger = logging.get_logger(__name__, config)

if __name__ == "__main__":
    logger.info("Hello world!")
```
