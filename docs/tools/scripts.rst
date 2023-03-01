Convenience Scripts
===================

There's a number of scripts which makes it easier for less experienced django developers to perform common tasks. They are all located in the ``scripts/`` directory. They should be called from the project root by prepending the relative path, like this ``scripts/lint.sh``.

buildrun.sh
   cleans, builds, and runs the docker development setup

check-migrations.sh
   checks that there aren't missing migrations. Meant to be called by CI tools.

db.sh
   logs in to the database

erd.sh
   generates the entity-relation (ER) diagram

lint.sh
   runs linters against the code

logs.sh
   runs tail on the container logs

migrate.sh
   preprares and runs database migrations

precommit-check.sh
   runs lint, builds, and tests the code, to be used before committing code.

run.sh
   a master script with many options for working with the docker development setup

test.sh
   runs tests against the code
