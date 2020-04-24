import yaml
import json

with open('../samples/python-input.json') as f:
    jsonData = json.load(f)

yaml.SafeDumper.ignore_aliases = lambda *args: True

orderer_init_port = 7050
peer_init_port = 7051

with open("../docker-files/boilerplate_files/docker-compose-base-boilerplate.yaml") as f:
    base_doc = yaml.load(f)

# print (base_doc)

# Let's make base doc for peers #### (Wish me luck)

peer_name = "peer"
# TODO: Update to take value from json
network_name = ["byfn"]

org_final_name = []
org_final_name_withPort = []
org_mspID = []
org_peer_count = []

services = base_doc["services"]

for i in range(0, len(jsonData["organizations"]["peerOrgs"])):
    org = jsonData["organizations"]["peerOrgs"][i]["url"]
    org_mspID.append(jsonData["organizations"]["peerOrgs"][i]["mspID"])
    org_peer_count.append(int(jsonData["organizations"]["peerOrgs"][0]["count"]))

    for peer in range(0, int(jsonData["organizations"]["peerOrgs"][0]["count"])):
        orgName = peer_name + str(peer) + "." + org
        orgNameWithPort = orgName + ":" + str(peer_init_port)
        org_final_name.append(orgName)
        org_final_name_withPort.append(orgNameWithPort)
        
        if not orgName in services:
            services[orgName] = {}
        if not "container_name" in services[orgName]:
            services[orgName]["container_name"] = orgName
        if not "extends" in services[orgName]:
            services[orgName]["extends"] = {}
            if not "file" in services[orgName]["extends"]:
                services[orgName]["extends"]["file"] = "peer-base.yaml"
            if not "service" in services[orgName]["extends"]:
                services[orgName]["extends"]["service"] = "peer-base"
        if not "environment" in services[orgName]:
            services[orgName]["environment"] = [
            "CORE_PEER_ID=" + orgName, "CORE_PEER_ADDRESS=" + orgNameWithPort, "CORE_PEER_LISTENADDRESS=0.0.0.0:" + str(peer_init_port),
            "CORE_PEER_CHAINCODEADDRESS=" + orgName + ":" + str(peer_init_port + 1), "CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:" + str(peer_init_port + 1),
            "CORE_PEER_GOSSIP_BOOTSTRAP=" + orgNameWithPort, "CORE_PEER_GOSSIP_EXTERNALENDPOINT=" + orgNameWithPort,"CORE_PEER_LOCALMSPID=" + org_mspID[i]
        ]
        if not "volumes" in services[orgName]:
            services[orgName]["volumes"] = [
            "/var/run/:/host/var/run/",
            "../crypto-config/peerOrganizations/" + org + "/peers/" + orgName + "/msp:/etc/hyperledger/fabric/msp",
            "../crypto-config/peerOrganizations/" + org + "/peers/" + orgName + "/tls:/etc/hyperledger/fabric/tls",
            orgName + ":/var/hyperledger/production"
            ]
        if not "ports" in services[orgName]:
            services[orgName]["ports"] = [str(peer_init_port) + ":" + str(peer_init_port)]

        peer_init_port = peer_init_port + 1000


# TODO: Algorithm for PEER_GOSSIP_BOOTSTRAP

base_doc["services"].update(services)

with open("../docker-files/final_files/base/docker-compose-base.yaml", "w") as f:
    yaml.safe_dump(base_doc, f)
