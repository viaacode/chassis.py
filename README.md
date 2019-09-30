# VIAA Chassis

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
$ pip install viaa-chassis
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
