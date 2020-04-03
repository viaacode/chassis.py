- [Meemoo Chassis](#meemoo-chassis)
  * [Usage](#usage)
    + [Configuration](#configuration)
    + [Logging](#logging)
    + [Correlation ID's](#correlation-id-s)
  * [Tutorials](#tutorials)
    + [Prerequisites](#prerequisites)
    + [Preparing the environment](#preparing-the-environment)
    + [Preparing the environment for development](#preparing-the-environment-for-development)
    + [Tutorial 1: A trivial "Hello, World" app](#tutorial-1--a-trivial--hello--world--app)
    + [Tutorial 2: A small "Hello, World" webservice with Flask](#tutorial-2--a-small--hello--world--webservice-with-flask)
      - [Running our app with the uWSGI application server](#running-our-app-with-the-uwsgi-application-server)
    + [Tutorial 3: "Hello, World" using queues](#tutorial-3---hello--world--using-queues)
      - [The RabbitMQ broker](#the-rabbitmq-broker)
    + [Tutorial 4: Adding NGINX as a reverse proxy](#tutorial-4--adding-nginx-as-a-reverse-proxy)
    + [Tutorial 5: Putting it all together: receive a HTTP message and forward it to a queue](#tutorial-5--putting-it-all-together--receive-a-http-message-and-forward-it-to-a-queue)
    + [Tutorial 6: Application with both a HTTP Flask interface and incoming AMQP messages (TODO)](#tutorial-6--application-with-both-a-http-flask-interface-and-incoming-amqp-messages--todo-)
    + [Tutorial 7: Demonstrating correlation ID's in Celery tasks (TODO)](#tutorial-7--demonstrating-correlation-id-s-in-celery-tasks--todo-)
    + [Flask in Development mode](#flask-in-development-mode)
  * [Development](#development)
    + [Running the tests](#running-the-tests)

# Meemoo Chassis

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

1. command line arguments (*not implemented*)
2. environment variables (*not implemented*)
3. config.yml file in the project root folder
4. default values

An example config file is included in this repository, see
`config.yml.example`.

```python
>>> from viaa.configuration import ConfigParser
>>> config = ConfigParser()
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

### Correlation ID's

**TODO**

```python
>>> from viaa.observability.correlation import CorrelationID
>>> CorrelationID().correlation_id
```

## Tutorials

We will make `x` different small applications building on top of each other:

1. a trivial app that logs "Hello, World" to the console
2. a small "Hello, World" Flask-based webservice
3. "Hello, World" using queues: two connected services, a producer and a consomer, that communicate via an AMQP-queue
4. dockerize our app and put an NGINX reverse proxy in front
5. combining HTTP and AMQP

The main goal of all of these tutorials is to demonstrate the use of correlation ID's. The class that provides a correlation ID is `correlation.py`. You can import the `CorrelationID` class and get the current correlation ID via it's `correlation_id` attribute:

```python
>>> from viaa.observability.correlation import CorrelationID
>>> CorrelationID().correlation_id
```

### Prerequisites

This tutorial expects you to be familiar with Python and the basics of web
application development. We will use [Python 3.6](https://www.python.org/), [pip](https://pip.pypa.io/en/stable/installing/ "pip")
and  [virtual environments](https://virtualenv.pypa.io/en/stable/). To get set
up, see  [this guide on installing Python](https://realpython.com/installing-python/).

### Preparing the environment

First, let’s create a folder and virtual environment to isolate the code and dependencies for this project.

```shell
$ python -m venv env
$ source env/bin/activate
$ pip install viaa-chassis
```

### Preparing the environment for development

Alternatively, for development or testing purposes, it might be more convenient to git-clone the repository and set the `PYTHONPATH` environment variable to your current working directory like so (from within the `chassis.py` directory):

```shell
$ export PYTHONPATH="$PWD"
```

The main use of `PYTHONPATH` is that, when developing, we want to be able to already import from our Python-package or library before we packaged it into an installable Python package. 

See [Using PYTHONPATH](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html "Using PYTHONPATH") or [Python's official documentation on PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH "the PYTHONPATH environment variable") for more information.

Don't forget to create and activate a virtual environment as well as explained before.

### Tutorial 1: A trivial "Hello, World" app

The first app we will write is, of course, something that prints "Hello world!" to the screen. Open your editor and put the following code in `helloworld.py`:

```python
from viaa.observability import logging
from viaa.configuration import ConfigParser

config = ConfigParser()
logger = logging.get_logger(__name__, config)

if __name__ == "__main__":
    logger.info("Hello world!")
```

Execute it with:

```shell
(env) $ python helloworld.py
```

We should get a nicely JSON-formatted logging statement with "Hello world!" as the message, a correlation ID and some more contextual information.

### Tutorial 2: A small "Hello, World" webservice with Flask

First we install `flask` using pip.

```shell
(env) $ pip install flask
```

Put the following code in `app.py`:

```python
from flask import Flask

from viaa.frameworks.flask import CorrelationMiddleware
from viaa.configuration import ConfigParser
from viaa.observability import logging
from viaa.observability.correlation import CorrelationID

config = ConfigParser()
log = logging.get_logger(__name__, config=config)

app = Flask(__name__)
# Make our app correlation-id-aware
CorrelationMiddleware(app)

@app.route('/')
@app.route('/<name>')
def hello(name='World'):
    log.info('A call has been made')
    return f"<p>Hello {name}!</p><p>Your correlation ID is: <code>{CorrelationID().correlation_id}</code></p>"

if __name__ == "__main__":
    app.run()
```

Start this Flask app with:

```shell
(env) $ python app.py
```

Alternatively, you can also:

```shell
(env) $ export FLASK_APP=app.py
(env) $ flask run
```

Head over to `http://127.0.0.1:5000/` to see it in action or, in a different terminal, do:

```shell
$ curl -i http://127.0.0.1:5000/
$ curl -i -H "X-Correlation-ID: 3.14159265359" http://127.0.0.1:5000/pi
```

(The `-i` option to curl includes the response headers. The `-H` options sets a custom header.)

#### Running our app with the uWSGI application server

First, install uWSGI via `pip install uwsgi`.

The `uwsgi.ini` file:

```
[uwsgi]
module = wsgi:app

master = true
processes = 4

; We use the port 5000 which we will
; then expose on our Dockerfile
;socket = :5000
http = 0.0.0.0:5000
vacuum = true

die-on-term = true

disable-logging = false
```

The `wsgi.py` file:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

Run with:

```shell
(env) $ uwsgi -i uwsgi.ini
```

In a different terminal, test with:

```shell
$ curl -i http://127.0.0.1:5000/
$ curl -i -H "X-Correlation-ID: 3.14159265359" http://127.0.0.1:5000/pi
```

### Tutorial 3: "Hello, World" using queues

In this part of the tutorial we'll demonstrate the correlation ID's via [AMQP](https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol "AMQP")-messages. We'll write a minimal producer in `send.py` and a minimal consumer in `receive.py`. For this to work, we'll also need an AMQP-broker: we'll be using [RabbitMQ](https://www.rabbitmq.com/ "RabbitMQ").

There's a couple of ways of installing the RabbitMQ-broker. The easiest way is probably by running a Docker container.

This part of our tutorial is largely based on: [https://www.rabbitmq.com/tutorials/tutorial-one-python.html](https://www.rabbitmq.com/tutorials/tutorial-one-python.html).

The `send.py` file:

```python
from viaa.observability import logging
from viaa.observability.correlation import CorrelationID
from viaa.configuration import ConfigParser
from viaa.communication import amqp as pika

config = ConfigParser()
log = logging.get_logger(__name__, config)

if __name__ == "__main__":
    conn_params = pika.ConnectionParameters(host='localhost')
    with pika.BlockingConnection(conn_params) as connection:
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
        log.info(" [x] Sent 'Hello World!'")
```

The `receive.py` file:

```python
from viaa.observability import logging
from viaa.observability.correlation import CorrelationID
from viaa.configuration import ConfigParser
from viaa.communication import amqp as pika

config = ConfigParser()
log = logging.get_logger(__name__, config)

def callback(ch, method, properties, body):
    log.info(f"Received {body} with correlation ID {properties.correlation_id}")

if __name__ == "__main__":
    conn_params = pika.ConnectionParameters(host='localhost')
    with pika.BlockingConnection(conn_params) as connection:
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        channel.basic_consume(
            queue='hello', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
```

#### The RabbitMQ broker

Build the RabbitMQ image with:

```shell
(env) $ docker build -t chassis/rabbitmq:3.7-management -f Dockerfile.rabbitmq ./Docker
```

List the image with:

```shell
(env) $ docker images --filter=reference="chassis/*"
```

Run this container with:

```shell
(env) $ docker run -p 5672:5672 -p 15672:15672 --hostname rabbitmq.local --name chassis_rabbitmq chassis/rabbitmq:3.7-management
```

Confirm that it's running via `docker ps` and point your browser to: http://127.0.0.1:15672/ (log in with "guest/guest").

You will see that, as of yet, no queues have been defined. The `hello`-queue will appear once we send our first message (remember the call to `channel.queue_declare`).

Open up a new terminal and have the producer send a single message:

```shell
(env) $ python send.py
```

**Note**: When switching to a new terminal, don't forget to activate the virtual environment and set the `PYTHONPATH` environment variable.

You can call `python send.py` as many times as you like. In the RabbitMQ management interface, you can see that the queue has been declared and messages have arrived.

Now start the consumer with:

```shell
(env) $ python receive.py
```

### Tutorial 4: Adding NGINX as a reverse proxy

We will dockerize our Flask application from tutorial 2 and put an NGINX reverse proxy in front of it. The reverse proxy is configured to generate correlation ID's and add them to every request via the `X-Correlation-ID` header thus further demonstrating the capability of using the correlation ID when it's already present.

First, build the NGINX image with:

```shell
(env) $ docker build -t chassis/nginx -f ./Docker/Dockerfile.nginx ./Docker
```

Second, dockerize our Flask application:

```shell
(env) $ docker build -t chassis/flask-uwsgi .
```

List our new images with:

```shell
(env) $ docker images --filter=reference="chassis/*"
```

Open up your editor and put this in `docker-compose.yml`:

```yaml
# docker-compose.yml
version: '2'
services:
  flask:
    container_name: flask
    image: chassis/flask-uwsgi
    build:
      context: .
      dockerfile: Dockerfile
    expose:
      - 5000
    volumes:
      - "./:/usr/src/app"
    mem_limit: 256m
  nginx:
    container_name: nginx
    image: chassis/nginx
    build:
      context: ./Docker
      dockerfile: Dockerfile.nginx
    ports:
      - "8080:8080"
      - "5000:5000"
    mem_limit: 256m
    depends_on:
      - flask
```

Start the stack via `docker-compose`:

```shell
(env) $ docker-compose up
```

Our upstream Flask application should now **never** need to generate a correlation ID because it should always already be present in the HTTP-headers. Either, because:

1. the client-request contained an `X-Correlation-ID`-header, or,
2. because NGINX added it.

Try both cases with:

```shell
$ curl -i http://127.0.0.1:8080/
$ curl -i -H "X-Correlation-ID: 3.14159265359" http://127.0.0.1:8080/pi
```

**Note**: You can try the same cURL commands as above, only now NGINX is listening on port **8080** and forwarding the requests to our upstream Flask application (which itself doesn't expose a public port).

### Tutorial 5: Putting it all together: receive a HTTP message and forward it to a queue

Next up, we will build upon our small Flask application and extend it to forward the incoming request to a Rabbit-queue. Open up `app.py` and change it to:

```python
from flask import Flask

from viaa.frameworks.flask import CorrelationMiddleware
from viaa.configuration import ConfigParser
from viaa.observability import logging
from viaa.observability.correlation import CorrelationID
from viaa.communication import amqp as pika

config = ConfigParser()
log = logging.get_logger(__name__, config=config)

app = Flask(__name__)
# Make our app correlation-id-aware
CorrelationMiddleware(app)

conn_params = pika.ConnectionParameters(host='rabbitmq')

@app.route('/')
@app.route('/<name>')
def hello(name='World'):
    log.info('A call has been made')
    message = f"<p>Hello {name}!</p><p>Your correlation ID is: <code>{CorrelationID().correlation_id}</code></p>"
    with pika.BlockingConnection(conn_params) as connection:
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='', routing_key='hello', body=message)
        log.info(f" [x] Sent 'Hello {name}!'")
    return message + "<p>Your message was routed to Rabbit. Go check it out on <a href='http://127.0.0.1:15672/#/queues/%2F/hello' target='_blank'>http://0.0.0.0:15672/#/queues/%2F/hello</a>.</p>"

if __name__ == "__main__":
    app.run()
```

Add the RabbitMQ service to the `docker-compose.yml`-file:

```yaml
# docker-compose.yml
version: '2'
services:
  ...
  rabbitmq:
    container_name: rabbitmq
    image: chassis/rabbitmq
    build:
      context: ./Docker
      dockerfile: Dockerfile.rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    mem_limit: 256m
```

Start the stack via `docker-compose`:

```shell
(env) $ docker-compose up
```

**Note**: Make sure the RabbitMQ container from tutorial 3 isn't running anymore or you'll get an error on conflicting port numbers.

Check the output of `docker-compose ps`:

```
  Name                Command               State                                             Ports                                           
----------------------------------------------------------------------------------------------------------------------------------------------
flask      uwsgi -i uwsgi.ini               Up      5000/tcp                                                                                  
nginx      nginx -g daemon off;             Up      0.0.0.0:5000->5000/tcp, 80/tcp, 0.0.0.0:8080->8080/tcp                                    
rabbitmq   docker-entrypoint.sh rabbi ...   Up      15671/tcp, 0.0.0.0:15672->15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp
```

Now point your browser to http://127.0.0.1:8080/ or use any of the aforementioned curl-commands (on port 8080).

Since the RabbitMQ service is publicly exposed, you can also start `receive.py` to consume the messages:

```shell
(env) $ python receive.py
```

### Tutorial 6: Application with both a HTTP Flask interface and incoming AMQP messages (TODO)

**TODO**

### Tutorial 7: Demonstrating correlation ID's in Celery tasks (TODO)

**TODO**

### Flask in Development mode

```shell
(env) $ export FLASK_ENV=development
(env) $ export FLASK_APP=app.py
(env) $ flask run
```

Now, Flask tells us:

```
 * Serving Flask app "app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 198-394-047
```

Any changes to our code will now trigger a Flask reload: super convenient!

## Development

**TODO**: can be moved to `CONTRIBUTING.md`

### Running the tests

After activating your virtual environment, first set the `PYTHONPATH` to your
working directory:

```
$ export PYTHONPATH="$PWD"
```

Then run the tests with:
```
$ pytest -v
```
