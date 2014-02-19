hunk
====

Helps client-side Web development by mocking JSON API server.


Installation
------------

hunk can be installed via pip or easy_install:

.. code-block:: bash

    $ pip install hunk

Or:

.. code-block:: bash

    $ easy_install hunk


Usage
-----

Basics
~~~~~~

Setup data directory and files. 

- Directories under the root directory have a HTTP method name
- Directories and files have name to be resource path
- Files have conent to be response JSON

For example, see demo/simple directory:

.. code-block:: bash

    $ tree demo/simple/
    demo/simple/
    |-- get
    |   |-- members
    |   |   |-- 100.json
    |   |   |-- 200.json
    |   |   |-- 300.json
    |   |   ...
    |   +-- sounds.json
    |-- post
    |   +-- members.json
    ...

Move to the root directory and run hunk:

.. code-block:: bash

    $ cd demo/simple/
    $ hunk
     * Running on http://localhost:8080/

Now, you can access Web API with HTTP:

.. code-block:: bash

    $  curl http://localhost:8080/members/100
    {"gender": "female", "kind": "human", "name": "Dorothy"}

    $ curl http://localhost:8080/members
    [{"kind": "scarecrow", "name": "Hunk"}, ...]

    $ curl http://localhost:8080/sounds
    [{"title": "Over The Rainbow"}, ... ]

    $ curl http://localhost:8080/members -X POST
    {"result": "success"}


Controls HTTP headers and the status code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

hank can control HTTP headers and the status code. See demo/metadata directory:

.. code-block:: bash

    $ tree demo/metadata/ -a
    demo/metadata/
    +-- get
        |-- allow
        |   |-- .headers
        |   +-- record.json
        +-- forbidden
            |-- record.json
            +-- .status

Can control HTTP header with .headers file:

.. code-block:: bash

    $ cd demo/metadata/
    $ cat get/allow/.headers 
    Server: hunk!
    Allow: GET

    $ curl http://localhost:8080/allow/ -i
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 65
    Allow: GET
    Server: hunk!
    ...

And can also control HTTP status code with .status file:

.. code-block:: bash

    $ cat get/forbidden/.status 
    403

    $ curl http://localhost:8080/forbidden/ -i
    HTTP/1.0 403 FORBIDDEN
    ...


Passing through to production environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

hank can let a part of the requests to pass through to a production environment. See demo/production directory:

.. code-block:: bash

    $ tree demo/production/
    demo/production/
    +-- get
        |-- available
        |   |-- 1.json
        |   +-- 3.json
        +-- production_conf.py
        ...

production_conf.py under the root directory defines available production environment:

.. code-block:: python

    # -*- coding: utf-8 -*-


    scheme = 'http'

    hostname = 'localhost'

    port = 9000

    routes = [
        '/available/2',
        '/available/4'
    ]

According to this configuration, the responses to the request to /available/1 and /available/3 are returned from the mock server, and to /available/2 and /available/4 are returned from the production server:

.. code-block:: bash

    $ curl http://localhost:8080/available/1
    {"message": "I am from hunk server."}

    $ curl http://localhost:8080/available/2
    {"message": "I am from production server."}

    $ curl http://localhost:8080/available/3
    {"message": "I am from hunk server."}

    $ curl http://localhost:8080/available/4
    {"message": "I am from production server."}
