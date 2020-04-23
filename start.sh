#!/usr/bin/env bash
export GO111MODULE=on
ERR="$(go build -o app ./cmd/... 2>&1)"

[  -z "$ERR" ] && ./app --port=9000 || echo ERROR: "${ERR}"; exit 1