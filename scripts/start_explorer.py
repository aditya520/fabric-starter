import os
import sys
import json



def start_explorer(jsonData):
    
    path = "./explorer/connection-profile/first-network.json"
    with open(path) as f:
        config = json.load(f)
        

    # os.system("CRYPTOS_PATH= \"./network/crypto-config\"")
    # os.system("admin_key_path=\"peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore\"")
    # os.system("private_key=\"/tmp/crypto/${admin_key_path}/$(ls ${CRYPTOS_PATH}/${admin_key_path})")

    # os.system("cat $config | jq -r --arg private_key \"$private_key\" '.organizations.Org1MSP.adminPrivateKey.path = $private_key' > tmp && mv tmp $config")

    # __delete_shared

    os.system("docker-compose -f ./explorer/docker-compose.yaml up --force-recreate -d || exit 1")

    # echoc "Blockchain Explorer default user is admin/adminpw" light yellow
    # echoc "Grafana default user is admin/admin" light yellow