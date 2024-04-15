# uv

We're using `uv` as a faster replacement to `pip` and `pip-tools`. See the [official documentation on getting started](https://github.com/astral-sh/uv#getting-started).

## How we use it

We're using `uv` to compile and install python dependencies, which replaces the functionalities of `pip` and `pip-tools`. `uv` can also create and maintain a virtual environment but we're not using it for now. In fact, we're suppressing it with the `--system` option during `uv pip install`.

`uv` is already part of the `docker` image, so there's no need to install it on the host. It does require prepending the docker-compose information to run, for example: `docker-compose exec web uv pip compile requirements.in -o requirements.txt`. We'll omit the `docker-compose exec web` portion from now on in this document.

`requirements.in` is the requirements file and `uv pip compile` generates `requirement.txt`, with pinned versions, similar to lock files in other languages.

## Usage

### Upgrade depencencies

We shouldn't run this on every build, but we should do this manually every month/quarter or so.

```bash
# docker-compose exec web
uv pip compile requirements.in -o requirements.txt --no-header --upgrade
```

Or run the script

```bash
./scripts/update-dependencies.sh
```

#### pip compile options

Disable header in the generated file
: `--no-header` This solves the problem unnecessary code churn caused by changing headers

Upgrade all dependencies
: `--upgrade`

Generate pip-8 style hashes
: `--generate-hashes` Hashes improve security but are not verified by `uv` at the moment. It is planned. Switch back to `pip` for installation if we need to verify hashes.

Disable annotation of where dependencies come from
: `--no-annotate` This makes the generated file shorter but less informative

See [pip-compile docs](https://pip-tools.readthedocs.io/en/stable/cli/pip-compile/) for more options and explanation

### Install dependencies

This is used in the `Dockerfile` to install python dependencies.

```bash
uv pip install --system -r requirements.txt
```

#### pip install options

Install to global
: `--system` bypass the virtual environment requirement

See [pip install docs](https://pip.pypa.io/en/stable/cli/pip_install/) for more options and explanation

## Explanations

### Global install

We're using the `--system` option in the `Dockerfile` to bypass the virtual environment requirement for `uv`. This is because the docker image is already a virtual environment separate from the host.

### Version pinning

We're leaving most dependencies unpinned in `requirements.in` so that `pip compile` will pin the newest compatible versions in `requirements.txt`. The only manually pinned dependency is `django~=4.2.0`. The `x.2.x` versions have long term support, and we're using `4`, since `4.2` is the latest LTS available.
