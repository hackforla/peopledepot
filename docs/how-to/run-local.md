# Run backend in venv

If you have a requirement to run on your local machine or you are unable to get it to work on
Docker, do the following steps.  WARNING: If you run into issues you will get limited support.

Run these commands from the `app` directory:

1. Copy `.env.docker-example` to `.env.local`
1. Inspect `.env.local` and change values as appropriate.  The file includes instructions on how to use local `postgres` and  `sqlite` for the database. `sqlite` has no set up.  It uses a file `db.sqlite3`.  If it is not there, it automatically creates it.
1. **Mac only**: If you have a Mac, the python command may not be found and scripts will fail.  Try to run python using the "python" command from the terminal.  If you get an error that the python command is
    not found, type: `alias python="python3"`
1. Run these commands from the terminal in the project root.

```bash
cd app

# copy the env file
cp .env.docker-example .env.local

# create a virtual environment
python -m venv venv

# activate (enter) the virtual environment
source venv/bin/activate
# install dependencies
pip install -r requirements.txt

# start local server
../scripts/start-local.sh
# start server with alternate port
# DJANGO_PORT=8001 ../scripts/start-local.sh

# browse to http://localhost:8000 (or 8001) to see the app

# Ctrl-C to stop the server

# deactivate (exit) the virtual environment
# to return to the system global environment
deactivate
```

**TIP**: Look up `direnv` for a useful method to automatically enter and exit virtual environments based on the current directory.
