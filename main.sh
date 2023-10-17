#!/bin/bash

cd "$(dirname "$0")"
source ./.venv/bin/activate
source ./.env.local

export PYTHONPATH=./app:$PYTHONPATH

if [ $1 = "start_api" ]; then
    uvicorn --app-dir ./app/src api:app --reload
elif [ -e "./app/src/$1.py" ]; then
    python3 "./app/src/$1.py"
else
    echo "コマンドが不明です"
fi

deactivate