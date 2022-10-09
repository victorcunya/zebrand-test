#!/bin/bash

alembic -c $(pwd)/alembic.ini "$@"
