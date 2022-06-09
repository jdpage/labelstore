# labelstore

A silly little API for storing labels with unique ids. A `/random` endpoint means it can
be used as a massively-multiplayer ephemeral fortune database, I suppose. If you wanted
such a thing.

Only works under the Flask development server, due to storing data in a global variable.
Not suitable for production. Not suitable for children under 3. May contain chemicals
known to cause the state of California. 


## How to run

With [poetry](https://python-poetry.org/) installed, can be run in a virtualenv using
the following commands:

```sh
$ poetry install
$ export FLASK_APP=labelstore:app
$ export FLASK_ENV=development
$ poetry run pytest  # optional: run tests
$ poetry run flask run
```

With [podman](https://podman.io/) or Docker installed, a container can be built and run
in a container using the following commands:

```sh
$ podman build -t labelstore:latest .
$ podman run --rm -it -p 5000:5000 labelstore:latest
```
