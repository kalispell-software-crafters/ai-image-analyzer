![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/kalispell-software-crafters/ai-image-analyzer/code-linting.yml)

# AI Image Analyzer

Sample app to count target items within an image or video.

## Contents

- [Setup](#setup)
- [Setup for local code development](#setup-for-local-code-development)
  - [Makefile](#makefile)
  - [Starting up the Docker container and initializing the repository](#starting-up-the-docker-container-and-initializing-the-repository)
  - [Starting the API service](#starting-the-api-service)
  - [Starting up all the services](#starting-up-all-the-services)
- [Tests](#tests)
- [Helpful Commands](#helpful-commands)
- [VS Code Extensions](#vs-code-extensions)
- [Resources](#resources)

## Setup

Ensure you have python and pip installed.

```shell
python --version
pip --version
```

From the root directory run the following command to install the
dependencies: `pip install -r requirements.txt`

You can run the app using this command: `python -m uvicorn src.api.index:app --reload`

Once running you can navigate to `http://127.0.0.1:8000/docs` to view the
interactive API documentation.

## Setup for local code development

There are some steps that need to be done prior to being able to
properly run and develop the code in this repository.

The following is a list of steps that have to happen prior to starting to
work / test the pipelines of this repository:

### Makefile

The project comes with a `Makefile` (**not supported in Windows!**)
that can be used for executing commands that will make the interaction
with this project much smoother. Keep in mind that folders with spaces in their names may cause issues.

One can see all of the available options by:

```bash
    $: make

    Available rules:

    add-licenses              Add licenses to Python files
    all-start                 Starts both the API service and the local development service
    all-stop                  Stops both the API service and the local development service
    all-web                   Open up all web endpoints
    api-build                 Build API image
    api-start                 Start API image container
    api-stop                  Stop API image container
    api-web                   Open API in web browser
    clean                     Removes artifacts from the build stage, and other common Python artifacts.
    clean-build               Remove build artifacts
    clean-model-files         Remove files related to pre-trained models
    clean-pyc                 Removes Python file artifacts
    clean-secrets             Removes secret artifacts - Serverless
    clean-test                Remove test and coverage artifacts
    create-environment        Creates the Python environment
    create-envrc              Set up the envrc file for the project.
    delete-environment        Deletes the Python environment
    delete-envrc              Delete the local envrc file of the project
    destroy                   Remove ALL of the artifacts + Python environments
    docker-local-dev-build    Build local development image
    docker-local-dev-login    Start a shell session into the docker container
    docker-local-dev-start    Start service for local development
    docker-local-dev-stop     Stop service for local development
    docker-prune              Clean Docker images
    git-flow-install          Install git-flow
    init                      Initialize the repository for code development
    lint                      Run the 'pre-commit' linting step manually
    pip-upgrade               Upgrade the version of the 'pip' package
    pre-commit-install        Installing the pre-commit Git hook
    pre-commit-uninstall      Uninstall the pre-commit Git hook
    requirements              Install Python dependencies into the Python environment
    show-params               Show the set of input parameters
    sort-requirements         Sort the project packages requirements file
    streamlit-app-build       Build Streamlit App image
    streamlit-app-start       Start Streamlit App image container
    streamlit-app-stop        Stop Streamlit App image container
    streamlit-app-web         Open Streamlit App in web browser
    test                      Run all Python unit tests with verbose output and logs
```

> **NOTE**: If you're using `Windows`, you may have to copy and modify to some
> extents the commands that are part of the `Makefile` for some tasks.

### Starting up the Docker container and initializing the repository

In order to work on current / new features, one can use *Docker* to
start a new container and start the local development process.

To build the Docker image, one must follow the following steps:

1. Start the Docker daemon. If you're using Mac, one can use the
Docker Desktop App.
2. Go the project's directory and run the following command using the `Makefile`:
```bash
# Go the project's directory
cd /path/to/directory

# Build the Docker iamge and start a container
make docker-local-dev-start
```
3. Log into the container
```bash
# Log into the container
make docker-local-dev-login
```

4. Once you're inside the container, you'll see the following prompt:

```bash
# Log into the container
➜$: make docker-local-dev-login
direnv: error /opt/program/.envrc is blocked. Run `direnv allow` to approve its content
```
> One will see the `direnv` error because `direnv` is installed and one must
> *allow* the changes to take effect.

5. Allow for the `direnv` changes
```bash
# Accept the changes
$: direnv allow
direnv: loading /opt/program/.envrc
```

6. The last thing is to initialize the repository. This can easily be done
with the `init` command:

```bash
$: make init
```
This will do the following tasks:
- Clean Python files
- Initialize the `.envrc` file used by `direnv`.
- Delete an existing python environment for the project, if it exists.
- Creates a new environment, if applicable
- Apply `direnv allow` to allow for `direnv` modifications.
- Install package requirements via `pip`
- Install `pre-commit` for code-linting and code-checking.
- Install `git-flow`, whenever possible.

These steps allow for the user to be able to develop new feature within
Docker, which makes it easier for developers to have the exact same set of
tools available.

## Starting the API service

The project comes with an out-of-the-box solution for starting and stopping
the API endpoint via Docker.

To start the container with the API endpoint, one must run the following
command:

```bash
# Start API service
make api-start
```

This service will start a Docker container that exposes the internal port
`80` to the local host's port `8090`. Once the image has been built and
a container has started, one can go to the service's main page by using
the following command:

```bash
# Go the URL of the API endpoint
make api-web
```

> This will direct the user to the following URL:
> [http://localhost:8090/docs](http://localhost:8090/docs)

In order to *stop* the API service, one can run the following command:

```bash
# Stop the API service
make api-stop
```

As one customizes the FastAPI with new features and more, these changes
will be automatically displayed in the URL from above.

### Starting up all the services

Similar to the sections from above, one can spin up or spin down all the
services at once with the help of 2 commands, i.e. `all-start` and `all-stop`.

In order to spin up both the *api* service and that for *local development*,
one can run:

```bash
make all-start
```

This command will execute both services and one will be able to log into the
container for local development, as well to connect to the API via the
browser.

Similarly, in order to spin down all of the services, one can simply run:

```bash
make all-stop
```

This will stop both services and delete any unused Docker containers.

## Tests

Unit tests can be found under the `src` folder alongside source code.
Test files end with `_test`. The following command will run all of the tests.

```shell
python -m pytest -v -s
```

The `-v` argument is for verbose output. The `-s` argument is for turning
off the capture mode so that print statements are printed to the console.

A Makefile command also exists to run these. See `make test`.

## Helpful Commands

Here is a list of commands that may be helpful when interacting with this project.

### Docker

List all Docker containers:

```shell
docker ps -a
```

## VS Code Extensions

To help facilitate local development you can install the [Visual Studio Code Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for VS Code. This will allow you to connect to the local development Docker container and more easily develop features.

## Resources

- [direnv](https://github.com/direnv/direnv)
- [Docker](https://docs.docker.com/reference/)
- [Docker Compose](https://docs.docker.com/compose/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [git](https://git-scm.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [isort](https://pycqa.github.io/isort/index.html)
- [Makefile](https://www.gnu.org/software/make/manual/make.html)
- [Markdown](https://www.markdownguide.org/)
- [Poetry](https://python-poetry.org/)
- [pre-commit](https://pre-commit.com)
- [Pydantic](https://docs.pydantic.dev/)
- [pytest](https://docs.pytest.org/en/7.2.x/)
- [Python](https://www.python.org/)
- [tmux](https://github.com/tmux/tmux/wiki/Getting-Started)
