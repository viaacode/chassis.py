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
Logging will go to `stdout` as a JSON string.

Running following example: 

```python
from viaa.observability import logging
from viaa.configuration import ConfigParser

config = ConfigParser()
logger = logging.get_logger(__name__, config)

logger.info("Hello world!", random_keyword="Vroom vroom...)
```

Will print: 
`{"message": "Hello world!", "source": ".\\test.py:<module>:6", "logger": "__main__", "level": "info", "timestamp": "2019-10-02T08:19:48.784897Z", "extra": {"random_keyword": "Vroom vroom..."}}`


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
