# Meemoo Chassis.py

**Important: this library is currently only available on the internal Meemoo
PyPI, make sure to update your
[pip-config](https://pip.pypa.io/en/stable/user_guide/#config-file)**


In this repository solutions for cross-cutting concerns will be gathered. This
is a work in progress and it will always be...

Currently implemented:
- Configuration
- Observability
  - Logging
  - Correlation

## Usage

Start by installing the library with `pip install viaa-chassis`, it is located
on the Meemoo PyPI.

### Configuration

You can use the configuration to configure the other modules in the chassis.
You call the `ConfigParser` and you will get a config dictionary containing all
the keys and values. The dictionary is filled based on following priority:

1. command line arguments (*not yet implemented*)
2. environment variables
3. config.yml file in the project root folder
4. default values

The configuration parser expects a default configuration file named
`config.yml` to be present in the project root folder. If this file is not
present, it will fall back to sane defaults for the services Chassis.py itself
exposes. This file minimally has one top-level section named `viaa` which is
used to configure Chassis.py. More sections may be added for application
specific configuration.

If no configuration exists in the project root folder, Chassis.py will
configure itself with sane defaults. For application specific configuration,
the `config.yml` file is needed, of course.

An example config file, `config.yml.example`, is included in this repository:

```yaml
viaa:
  logging:
    level: WARNING
app:
  log_path: !ENV "/var/${LOG_PATH}"
  passwd: !ENV ${PASSWD}
  service:
    host: api.example.com
```

In this example you can see how it is possible to interpolate values in your
configuration via environment variables. Configuration values in which
environment variables need to be expanded, have to start with the tag `!ENV`.
The environment variable keys use the standard curly braces bash syntax:
`${ENV_VAR}`.

When the corresponding environment variables are not declared, the ConfigParser
will raise a `KeyError` telling you wich environment variable is missing.

More examples can be found under `tests/resources/`.

#### Usage

```python
from viaa.configuration import ConfigParser
config = ConfigParser()
```

### Logging

The logging interface is made to resemble the Python standard logging as close
as possible.  The biggest difference is that you can pass a config object when
getting a logger instance.  **ALL** logging will go to `stdout` as a JSON
string, this means that logging by external packages will be formatted aswell.
Formatting all logs as JSON makes it easier to parse the logs in other
applications.

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

### A tiny "Hello, World" service

#### Prerequisites

This tutorial expects you to be familiar with Python and the basics of web
application development. We will use [Python 3.7](https://www.python.org/)
and  [virtual environments](https://virtualenv.pypa.io/en/stable/). To get set
up, see  [this guide on installing
Python](https://realpython.com/installing-python/).

#### Preparing the environment

First, let’s create a folder and virtual environment to isolate the code and
dependencies for this project.

```shell
$ python -m venv env
$ source env/bin/activate
$ pip install viaa-chassis
```

Now let’s write a tiny "Hello World" service, open your editor and put the
following in `helloworld.py`:

```python
from viaa.observability import logging
from viaa.configuration import ConfigParser

config = ConfigParser()
logger = logging.get_logger(__name__, config)

if __name__ == "__main__":
    logger.info("Hello world!")
```

### A small "Hello, World" webservice

Optional: make a new virtual environment and activate it.

First we install `flask` and `viaa-chassis` using pip. (Note: viaa-chassis is
only available on the Meemoo PyPI)

```shell
$ pip install flask
$ pip install viaa-chassis
```

Put the following code in `app.py`:

```python
from flask import Flask
from viaa.configuration import ConfigParser
from viaa.observability import logging

app = Flask(__name__)

config = ConfigParser()
logger = logging.get_logger(__name__, config=config)

@app.route('/')
def hello():
    logger.info('A call has been made')
    return 'Hello world!'

if __name__ == "__main__":
    app.run()
```

If you run this with `$ python app.py` and visit `http://127.0.0.1:5000/` you
should see following output:

```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
{"message": " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)"}
{"message": "A call has been made", "logger": "__main__", "level": "info", "timestamp": "2019-10-17T09:57:16.336332Z", "source": ".\\app.py:hello:12"}
{"message": "127.0.0.1 - - [17/Oct/2019 11:57:16] \"GET / HTTP/1.1\" 200 -"}
{"message": "127.0.0.1 - - [17/Oct/2019 11:57:16] \"GET /favicon.ico HTTP/1.1\" 404 -"}
```
