import create_docker_base as base
import create_docker_cli as cli
import create_configtx as configtx
import create_crypto_config as crypto
import generate_artifcats as gen_art
import json
import os
import sys



## Importing JSON ##

path = sys.argv[1]
print(path)
sys.stdout.flush()

with open(path) as f:
    jsonData = json.load(f)

## Crypto Config ##
crypto.create_crypto(jsonData)

## ConfigTx ##
configtx.create_configtx(jsonData)

## Docker base ##
base.create_base(jsonData)


## Docker CLI ##
cli.create_docker_compose_cli(jsonData)

## Artifacts ##
gen_art.create_artifacts(jsonData)
