If you have a requirement to run on your local machine or you are unable to get it to work on
Docker, do the following steps.  WARNING: If you run into issues you will get limited support.

Run these commands from the root directory:

1. Copy .env.docker-example to .env.local
1. Inspect .env.local and change values as appropriate.  The file includes instructions on how to use sqlite for the database.\
    sqlite has no set up.  It uses a file db.sqlite3.  If it is not there, it automatically creates it.
1. **Mac only**: If you have a Mac, the python command may not be found and scripts will fail.  Try to run python using the "python" command from the terminal.  If you get an error that the python command is
    not found, type: `alias python="python3"`
1. Run these commands from the terminal in the root.

```
cd django_root
source ../scripts/source start-local.sh
```
