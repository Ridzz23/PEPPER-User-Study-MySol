#!/bin/bash

DIR="$(cd "$(dirname "$0")" && pwd)"

export PYTHONHOME="$DIR/pepper-install"
export PYTHONPATH="$DIR/pepper-install/lib/python3.13/site-packages"

exec "$DIR/pepper-install/bin/python3.13" "$@"