import os
import sys
import yaml
import json
import copy
import pyaml

print("")
print("Generating configtx...")
sys.stdout.flush()


actorDict = {
        "Type": "",
        "Rule": "",
    }

orgDict = {
    "Name": "",
    "ID": "",
    "MSPDir": "",
    "Policies": {
        "Readers": copy.deepcopy(actorDict),
        "Writers": copy.deepcopy(actorDict),
        "Admins": copy.deepcopy(actorDict),
        "Endorsement": copy.deepcopy(actorDict)
    },
    "AnchorPeers": [
        {
            "Host": "",
            "Port": ""
        }
    ]
}

ordrDict = {
    "Host": "",
    "Port": "",
    "ClientTLSCert":"",
    "ServerTLSCert":""
}


def add_quote(a):
    return '"{0}"'.format(a)

def create_configtx(jsonData):
    yaml.SafeDumper.ignore_aliases = lambda *args: True

    with open("./network/template/configtx-template.yaml") as f:
        list_doc = yaml.load(f)

    orgArray = create_org_config(jsonData, 7051)

    list_doc["Profiles"]["TwoOrgsChannel"]["Application"]["Organizations"] = orgArray
    list_doc["Profiles"]["SampleMultiNodeEtcdRaft"]["Consortiums"]["SampleConsortium"]["Organizations"] = orgArray

    list_doc["Orderer"]["Addresses"] = [jsonData["organizations"]["ordererOrg"]["url"][0] + ":7050"]

    ordrArr, ordrDetailsArr = create_ordr_config(jsonData)

    list_doc["Profiles"]["SampleMultiNodeEtcdRaft"]["Orderer"]["EtcdRaft"]["Consenters"] = ordrDetailsArr
    list_doc["Profiles"]["SampleMultiNodeEtcdRaft"]["Orderer"]["Addresses"] = ordrArr
    
    ## Temperory fix
    with open("./network/configtx.yaml", "w+") as f:
        pyaml.dump(list_doc, f, vspacing=[2, 1])


def create_org_config(jsonData, aPPort):
    orgArray = []
    
    for org in jsonData["organizations"]["peerOrgs"]:
        orgDetails = copy.deepcopy(orgDict)

        adminRole = org["mspID"] + ".admin"
        peerRole = org["mspID"] + ".peer"
        clientRole = org["mspID"] + ".client"
        
        orgDetails["Name"] = org["mspID"]
        orgDetails["ID"] = org["mspID"]
        orgDetails["MSPDir"] = "crypto-config/peerOrganizations/"+org["url"] + "/msp"

        orgDetails["Policies"]["Readers"]["Type"] = "Signature"
        orgDetails["Policies"]["Readers"]["Rule"] = "OR(" + add_quote(adminRole) + ", " + add_quote(peerRole) + ", " + add_quote(clientRole) + " )"

        orgDetails["Policies"]["Writers"]["Type"] = "Signature"
        orgDetails["Policies"]["Writers"]["Rule"] = "OR(" + add_quote(adminRole) + ", " + add_quote(clientRole) + " )"

        orgDetails["Policies"]["Admins"]["Type"] = "Signature"
        orgDetails["Policies"]["Admins"]["Rule"] = "OR(" + add_quote(adminRole) + " )"

        orgDetails["Policies"]["Endorsement"]["Type"] = "Signature"
        orgDetails["Policies"]["Endorsement"]["Rule"] = "OR(" + add_quote(peerRole) + " )"

        orgDetails["AnchorPeers"][0]["Host"] = "peer0." + org["url"]
        orgDetails["AnchorPeers"][0]["Port"] = aPPort

        aPPort = aPPort + 2000

        orgArray.append(orgDetails)
        del orgDetails
    
    return orgArray

def create_ordr_config(jsonData):
    ordrPort = 7050
    ordrArr=[]
    ordrDetailsArr =[]
    
    for ordr in jsonData["organizations"]["ordererOrg"]["url"]:
        address = ordr+":"+ str(ordrPort)
        ordrArr.append(address)
        ordrDetails = copy.deepcopy(ordrDict)
        ordrDetails["Host"] = ordr
        ordrDetails["Port"] = ordrPort
        ordrDetails["ClientTLSCert"] = "crypto-config/ordererOrganizations/example.com/orderers/" + ordr + "/tls/server.crt"
        ordrDetails["ServerTLSCert"] = "crypto-config/ordererOrganizations/example.com/orderers/" + ordr + "/tls/server.crt"
        ordrDetailsArr.append(ordrDetails)
        ordrPort = ordrPort + 1000
    
    return ordrArr, ordrDetailsArr