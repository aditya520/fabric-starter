import os
import sys
import yaml
import json


args = sys.argv


###### JSON File ######

with open('../samples/python-input.json') as f:
  jsonData = json.load(f)




###### HardCoded Values ######
# n_orgs = args[1]
# n_peer_org = args[2]
peer_name = "peer"
network_name = ["byfn"]

# yaml.Dumper.ignore_aliases = lambda *args : True
yaml.SafeDumper.ignore_aliases = lambda *args : True


# class D(dict):
#     def __missing__(self, key):
#         self[key] = D()
#         return self[key]


with open("../docker-files/boilerplate_files/docker-compose-cli-boilerplate.yaml") as f:
     list_doc = yaml.load(f)

#### Networks ####

networks = dict.fromkeys(network_name,)
list_doc["networks"] = networks

#### Volumes ####

## Orderer Volume ##
org_final_name = []
for orderer in jsonData["organizations"]["ordererOrg"]["url"]:
     org_final_name.append(orderer)

### ORG Volumes ###
for i in range(0,len(jsonData["organizations"]["peerOrgs"])):
     org = jsonData["organizations"]["peerOrgs"][i]["url"]
     for peer in range(0,int(jsonData["organizations"]["peerOrgs"][0]["count"])):
          orgName = peer_name + str(peer) + "." + org
          org_final_name.append(orgName)


volumes = dict.fromkeys(org_final_name,)
list_doc["volumes"] = volumes

#### Services ####
# print (list_doc["services"])

services = {}


for org in org_final_name:
     if not org in services: services[org]={}
     if not "extends" in services[org]: services[org]["extends"]={}

     if not "service" in services[org]["extends"]: services[org]["extends"]["service"]={}
     if not "file" in services[org]["extends"]: services[org]["extends"]["file"]={}

     if not "container_name" in services[org]: services[org]["container_name"]={}
     if not "networks" in services[org]: services[org]["networks"]={}

     services[org]["extends"]["service"] = org
     services[org]["extends"]["file"] = "base/docker-compose-base.yaml"
     services[org]["container_name"] = org
     services[org]["networks"] = network_name

list_doc["services"].update(services)
# print (list_doc["services"])



#### Services CLI ####


list_doc["services"]["cli"]["depends_on"] = org_final_name
list_doc["services"]["cli"]["networks"] = network_name
# print (list_doc["services"])


with open("../docker-files/final_files/docker-compose-cli.yaml", "w") as f:
    yaml.safe_dump(list_doc, f)





# print (list_doc)


