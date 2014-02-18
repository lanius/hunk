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

Setup data directory and files. 

- Directories under the root have a HTTP method name
- Directories and files have name to be resource path
- Files have conent to be response JSON

For example:

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
