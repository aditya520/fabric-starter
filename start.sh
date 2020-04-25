#!/usr/bin/env bash
export GO111MODULE=on
export PYTHONWARNINGS="ignore"

if ! [ -d "./bin" ]; then
    echo "Binaries dont exist..."
    echo "Pulling latest binaries"
    curl -o binaries.sh -sL https://bit.ly/2ysbOFE
    chmod a+x binaries.sh
    ./binaries.sh -s -d
    rm -rf binaries.sh
    rm -rf ./config
fi


rm -rf ./network/crypto-config
rm -rf ./network/channel-artifacts/*

ERR="$(go build -o app ./cmd/... 2>&1)"

[  -z "$ERR" ] && ./app --port=9000 || echo ERROR: "${ERR}"; exit 1