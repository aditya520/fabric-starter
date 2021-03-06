import create_docker_base as base
import create_docker_cli as cli
import create_configtx as configtx
import create_crypto_config as crypto
import generate_artifcats as gen_art
import network_up as net_up
import initialize_network as net_init
import start_explorer as exp
import json
import os
import sys



## Importing JSON ##

path = sys.argv[1]

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

## Docker up ##
net_up.network_up()

## Network Init ##
net_init.initNetwork(jsonData)


# Start Explorer ##
#exp.start_explorer(jsonData)

sys.exit(0)