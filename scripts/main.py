from subprocess import call
import create_docker_base as base
import create_docker_cli as cli
import create_configtx as configtx
import create_crypto_config as crypto
import json



## Importing JSON ##
with open('../samples/python-input.json') as f:
    jsonData = json.load(f)



## Crypto Config ##
crypto.create_crypto(jsonData)

## ConfigTx ##
configtx.create_configtx(jsonData)

## Docker base ##
base.create_base(jsonData)


## Docker CLI ##
cli.create_docker_compose_cli(jsonData)

