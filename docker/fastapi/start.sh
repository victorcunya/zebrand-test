#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# alembic upgrade head
uvicorn app.interface.rest.main:app --reload --reload-dir . --host 0.0.0.0 --use-colors
