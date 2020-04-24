from subprocess import call
import scripts.create_docker_base as base
import json



with open('../samples/python-input.json') as f:
    jsonData = json.load(f)
    
base.create_base(jsonData)

## Docker CLI ##
call(["python", "create_docker_cli.py"])
