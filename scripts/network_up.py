import sys
import os
import time



## Docker up

def network_up():
    
    os.system("docker-compose -f network/docker-compose-cli.yaml up -d")

    time.sleep(15)
    print("")
    print("Created network")
    print("")
    sys.stdout.flush()

