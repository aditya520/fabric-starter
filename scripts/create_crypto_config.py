import yaml
import json
import copy
import pyaml
import sys



yaml.SafeDumper.ignore_aliases = lambda *args: True

def create_crypto(jsonData):
    print("")
    print("Generating crypto-config...")
    sys.stdout.flush()

    with open("./network/template/crypto-config-template.yaml") as f:
        crypto_doc = yaml.load(f)

    peerOrgsArr = create_crypto_orgs(jsonData,crypto_doc)
    ordrArr = create_crypto_ordr(jsonData,crypto_doc)

    crypto_doc["PeerOrgs"]=peerOrgsArr
    crypto_doc["OrdererOrgs"][0]["Specs"] = ordrArr

    with open("./network/crypto-config.yaml", "w+") as f:
            pyaml.dump(crypto_doc, f, vspacing=[2, 1])


def create_crypto_orgs(jsonData, crypto_doc):
    n_user = 1 # Hardocded for now
    peerOrgsArr = []
    for org in jsonData["organizations"]["peerOrgs"]:
       peerOrgs = copy.deepcopy(crypto_doc["PeerOrgs"][0])
       
       org_name = org["name"]
       org_peer_count = org["count"]
       org_url = org["url"]

       peerOrgs["Name"] = org_name.lower().capitalize()
       peerOrgs["Domain"] = org_url
       peerOrgs["EnableNodeOUs"] = True
       peerOrgs["Template"]["Count"] = org_peer_count
       peerOrgs["Users"]["Count"] = n_user
       peerOrgsArr.append(peerOrgs)
        
    return peerOrgsArr
    
def create_crypto_ordr(jsonData, crypto_doc):
    ordrArr = []

    for ordr in jsonData["organizations"]["ordererOrg"]["url"]:
        ordrSpec = copy.deepcopy(crypto_doc["OrdererOrgs"][0]["Specs"][0])
        ordrSpec["Hostname"] = ordr.split(".")[0]
        ordrArr.append(ordrSpec)
    
    return ordrArr