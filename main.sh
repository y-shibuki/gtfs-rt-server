#!/bin/bash

cd "$(dirname "$0")"
source ./.venv/bin/activate
source ./.env.local

if [ -e "./app/src/$1.py" ]; then
    python3 "./app/src/$1.py"
else
    echo "コマンドが不明です"
fi

deactivate