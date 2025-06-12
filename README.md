# Interview for Appointment Scheduling

Thank you for taking the time to work through our take home exercise.

## Running the environment

This exercise is _not_ intended to be a test of your ability to wrangle
development containers or Docker, so please contact us for help if you
have trouble getting the environment working!

With that in mind, you have a few options to get the environment
running:

### Option 1: Run using a cloud hosted Codespace

A [Github Codespace](https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces)
sets up all the dependencies in a [dev container](https://containers.dev/),
and launches VS Code in your browser.

1. `Code` -> `Codespaces` -> `New with options...`
1. Select the branch you want to use
1. Choose `Python 3, Django, Node.js LTS, React Router, and PostgreSQL`
   for `Dev container configuration`
1. `Create codespace`
1. Wait for the space to spin up, and use it in the browser version of VS Code

GitHub has [instructions for using Codespaces with your local copy of VS Code](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-github-codespaces-in-visual-studio-code),
but we have not tested these instructions yet.

### Option 2: Run on your local machine using the dev container

VS Code offers close integration with dev containers, and

You will need the following software on your machine:

* [Docker](https://www.docker.com/products/docker-desktop)
* [VS Code](https://code.visualstudio.com/) or some other VS Code derived
  editor, such as [Cursor](https://www.cursor.com/)
* [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
  for VS Code (it works with Cursor too!)

Once you have installed the necessary software, proceed as follows:

1. Start Docker if it is not already running.
1. Clone this repository on to your local machine.
1. Open your editor in the root of your local copy of this repository
1. You should see a popup with a button labeled **Reopen in Container** and
   the text:
   > Folder contains a Dev Container configuration file. Reopen folder to develop in a container (learn more).
1. Click the **Reopen in Container** button, wait for the space to boot, and
   use it in your editor
1. If you do not see the popup described in the preceding steps, click
   `View` -> `Command Palette…`, and search for
   `Dev Containers: Open Folder in Container…`
1. Navigate to the your local copy of this repository in the file picker, and
   click `Open`, wait for the space to boot, and use it in your editor

### Option 3: Run the environment manually with Docker

🚧 Running the environment manually is a work in progress. We _strongly_
encourage you to try option 1 or 2 first.

The dev container used for options 1 and 2 is a wrapper around a
[Docker Compose](https://docs.docker.com/compose/) file. If you prefer,
you can start the environment with the `docker compose` utility.

You will need the following software on your machine:

* [Docker](https://www.docker.com/products/docker-desktop)

Once you have Docker installed, proceed as follows:

1. Start Docker if it is not already running
1. Clone this repository on to your local machine
1. Remove the line:
   ```yml
       network_mode: service:db
   ```
   from the `app` servce in the
   `.devcontainer/python-django/docker-compose.yml` file
1. Add the following to the `app` service:
   ```yml
       ports:
         - "8000:8000"
         - "5173:5173"
   ```
1. Start the containers
   ```sh
   cd .devcontainer/python-django
   docker compose up -d
   ```
1. Open a shell inside the app container
   ```sh
   docker compose exec app bash
   ```

The remaining steps should be completed **inside the `app` container**.
Note that, inside the container, the repository will be mounted
under `/workspaces`.

7. Install [Python](https://www.python.org/) version 3.13
   ```sh
   apt install software-properties-common
   ```

   ```sh
   add-apt-repository ppa:deadsnakes/ppa
   ```

   ```sh
   apt-get install python3.13-full
   ```

   ```sh
   ln -s /usr/bin/python3.13 /usr/bin/python
   ```

   ```sh
   python3.13 -m ensurepip --upgrade
   ```

   ```sh
   ln -s /usr/local/bin/pip3.13 /usr/local/bin/pip
   ```


1. Install [Node.js](https://nodejs.org/) with the following commands:
   ```sh
   curl -fsSL https://deb.nodesource.com/setup_23.x -o nodesource_setup.sh
   ```

   ```sh
   bash nodesource_setup.sh
   ```

   ```sh
   apt-get install -y nodejs
   ```

1. In the repository directory inside the container, run
   ```sh
   bash python-django/install-dependencies.sh
   ```

At this point you should now have all the necessary dependencies to run the
frontend and backend for the exercise.

## Run the backend

The backend is a standard Django application, and may be run with the
standard Django `manage.py` script as follows:

```sh
cd python-django/interview_calendar/
./manage.py runserver
```

**Note:** If you chose option 3, you'll need to invoke `manage.py` like this:

```sh
./manage.py runserver 0.0.0.0:8000
```

The backend runs on port `8000`.

The backend serves some stub data at the endpoints:

- `/api/users/`
- `/api/users/1/calendar/free`

When run in a dev container, the backend will be wired up to a PostgreSQL
database. You may need to run:

```sh
./manage.py migrate
```

in order to run the migrations needed to create database tables
needed by Django.

## Run the frontend

Run it as follows:

```sh
cd python-django/interview-calendar-frontend/
npm run dev
```

The frontend runs on port `5173`.
