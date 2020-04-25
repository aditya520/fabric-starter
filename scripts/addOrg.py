import json
import os
import sys
import pyaml
import yaml
import create_configtx as configtx
import create_crypto_config as crypto

def createConfigtx(jsonData,inputJson):
    peerCount = 0
    for org in inputJson["organizations"]["peerOrgs"]:
        peerCount = peerCount + org["count"]
        
    port = (peerCount)*1000 + 7051

    orgArr = configtx.create_org_config(jsonData,port)

    configtxObj = {
        "Organizations": orgArr
    }

    with open("./network/newOrg/"+jsonData["organizations"]["peerOrgs"][0]["name"]+"configtx.yaml", "w+") as f:
        pyaml.dump(configtxObj, f, vspacing=[2, 1])


def createCryptoConfig(jsonData, inputJson):
    with open("./network/template/crypto-config-template.yaml") as f:
        crypto_doc = yaml.load(f)
    
    peerOrgsArr = crypto.create_crypto_orgs(jsonData,crypto_doc)
    
    cryptoObj = {
        "PeerOrgs": peerOrgsArr
    }
    
    with open("./network/newOrg/"+jsonData["organizations"]["peerOrgs"][0]["name"]+"crypto-config.yaml", "w+") as f:
           pyaml.dump(cryptoObj, f, vspacing=[2, 1])

path = sys.argv[1]
print(path)
sys.stdout.flush()

with open(path) as f:
    jsonData = json.load(f)

with open("./fixtures/"+jsonData["name"]+".json") as f:
    inputJson = json.load(f)
    
createConfigtx(jsonData,inputJson)
createCryptoConfig(jsonData, inputJson)
