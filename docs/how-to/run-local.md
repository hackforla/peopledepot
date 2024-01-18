If you have a requirement to run on your local machine or you are unable to get it to work on 
Docker, do the following steps.  WARNING: If you run into issues you will get limited support.

Run these commands from the root directory:
1. Copy .env.local-example to .env.local
2. Inspect .env.local and change values as appropriate.
3. Run these commands from the terminal in the root.
```
cd django_root
source ../scripts/source start-local.sh
```
