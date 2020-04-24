import yaml
import json
from marshmallow import pprint
import copy

yaml.SafeDumper.ignore_aliases = lambda *args: True

def create_crypto(jsonData):

    with open("./docker-files/boilerplate_files/crypto-config-boilerplate.yaml") as f:
        crypto_doc = yaml.load(f)


    n_user = 1 # Hardocded for now


    peerOrgsArr = []
    ordrArr = []
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

    for ordr in jsonData["organizations"]["ordererOrg"]["url"]:
        ordrSpec = copy.deepcopy(crypto_doc["OrdererOrgs"][0]["Specs"][0])
        ordrSpec["Hostname"] = ordr.split(".")[0]
        ordrArr.append(ordrSpec)


    crypto_doc["PeerOrgs"]=peerOrgsArr

    crypto_doc["OrdererOrgs"][0]["Specs"] = ordrArr

    with open("./crypto-config/final_files/crypto-config.yaml", "w+") as f:
            yaml.safe_dump(crypto_doc, f)

