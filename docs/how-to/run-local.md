If you have a requirement to run on your local machine or you are unable to get it to work on
Docker, do the following steps.  WARNING: If you run into issues you will get limited support.

Run these commands from the app directory:
1. From the terminal:
```
cd app
cp .env.local-example .env.local
```
2. Inspect .env.local and change values as appropriate.
3. From the terminal in the app directory, run:
```
source ../scripts/start-local.sh
```
