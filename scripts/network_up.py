import sys
import os
import time



## Docker up
os.system("docker-compose -f network/docker-compose-cli.yaml up -d")

time.sleep(15)

