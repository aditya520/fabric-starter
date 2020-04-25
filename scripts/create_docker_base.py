import yaml
import json
import copy

yaml.SafeDumper.ignore_aliases = lambda *args: True

def create_base(jsonData):
    #orderer_init_port = 7050
    

    with open("./docker-files/boilerplate_files/docker-compose-base-boilerplate.yaml") as f:
        base_doc = yaml.load(f)

    services = create_peer_base(base_doc, jsonData)
    base_doc["services"].update(services)

    with open("./docker-files/final_files/base/docker-compose-base.yaml", "w+") as f:
        yaml.safe_dump(base_doc, f)



def create_peer_base(base_doc, jsonData):
    peer_name = "peer"
    peer_init_port = 7051

    org_final_name = []
    org_final_name_withPort = []
    org_mspID = []
    org_peer_count = []

    services = copy.deepcopy(base_doc["services"])
    
    for i in range(0, len(jsonData["organizations"]["peerOrgs"])):
        org = jsonData["organizations"]["peerOrgs"][i]["url"]
        org_mspID.append(jsonData["organizations"]["peerOrgs"][i]["mspID"])
        org_peer_count.append(int(jsonData["organizations"]["peerOrgs"][i]["count"]))
        print("orgPeerCount: ",org_peer_count)
        bootstrap_peer_count = 0
        if i != 0:
            bootstrap_peer_count = sum(org_peer_count) - org_peer_count[i]
        
        print("Bootstrap: ",bootstrap_peer_count)


        for peer in range(0, int(jsonData["organizations"]["peerOrgs"][i]["count"])):
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
                if peer == 0:
                    services[orgName]["environment"] = [
                    "CORE_PEER_ID=" + orgName, "CORE_PEER_ADDRESS=" + orgNameWithPort, "CORE_PEER_LISTENADDRESS=0.0.0.0:" + str(peer_init_port),
                    "CORE_PEER_CHAINCODEADDRESS=" + orgName + ":" + str(peer_init_port + 1), "CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:" + str(peer_init_port + 1),
                    "CORE_PEER_GOSSIP_BOOTSTRAP=" + "peer1." + jsonData["organizations"]["peerOrgs"][i]["url"] + ":" + str(peer_init_port + 1000), "CORE_PEER_GOSSIP_EXTERNALENDPOINT=" + orgNameWithPort,"CORE_PEER_LOCALMSPID=" + org_mspID[i]]
                else:
                    print("IN with ",i, " org")
                    print("Bootstrapped: ",org_final_name_withPort[bootstrap_peer_count])
                    services[orgName]["environment"] = [
                    "CORE_PEER_ID=" + orgName, "CORE_PEER_ADDRESS=" + orgNameWithPort, "CORE_PEER_LISTENADDRESS=0.0.0.0:" + str(peer_init_port),
                    "CORE_PEER_CHAINCODEADDRESS=" + orgName + ":" + str(peer_init_port + 1), "CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:" + str(peer_init_port + 1),
                    "CORE_PEER_GOSSIP_BOOTSTRAP=" + org_final_name_withPort[bootstrap_peer_count], "CORE_PEER_GOSSIP_EXTERNALENDPOINT=" + orgNameWithPort,"CORE_PEER_LOCALMSPID=" + org_mspID[i]
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

    return services