import pyaml
import json
import copy
import sys



def create_base(jsonData):
    
    print("")
    print("Generating docker-compose files...")
    sys.stdout.flush()
    
    peerService = create_peer_base(jsonData,7051)
    
    ordrService = create_ordr_base(jsonData)

    base = {
        "version" : "'" + str(2) + "'",
        "services": {**ordrService,**peerService}
    }
    
    with open("./network/base/docker-compose-base.yaml", "w+") as f:
        pyaml.dump(base, f, vspacing=[2, 1])


def create_ordr_base(jsonData):
    orderer_init_port = 7050
    #TODO: Parse from input json
    network_name = ["byfn"]
    
    services = {}
    
    for ordr in jsonData["organizations"]["ordererOrg"]["url"]:
       services[ordr] = {
           "extends":{
               "file": "peer-base.yaml",
               "service": "orderer-base"
           },
           "environment":[
               "ORDERER_GENERAL_LISTENPORT="+str(orderer_init_port)
           ],
           "container_name": ordr,
           "networks": network_name,
           "volumes":[
               "../channel-artifacts/genesis.block:/var/hyperledger/orderer/orderer.genesis.block",
               "../crypto-config/ordererOrganizations/everledger.com/orderers/"+ordr+"/msp:/var/hyperledger/orderer/msp",
               "../crypto-config/ordererOrganizations/everledger.com/orderers/"+ordr+"/tls/:/var/hyperledger/orderer/tls",
               ordr+":/var/hyperledger/production/orderer"
           ],
           "ports":[
               str(orderer_init_port)+":"+str(orderer_init_port)
           ]
       }
       orderer_init_port = orderer_init_port + 1000
    
    return services      

def create_peer_base(jsonData,peer_init_port):
    peer_name = "peer"

    org_final_name = []
    org_final_name_withPort = []
    org_mspID = []
    org_peer_count = []

    services = {}
    
    for i in range(0, len(jsonData["organizations"]["peerOrgs"])):
        org = jsonData["organizations"]["peerOrgs"][i]["url"]
        org_mspID.append(jsonData["organizations"]["peerOrgs"][i]["mspID"])
        org_peer_count.append(int(jsonData["organizations"]["peerOrgs"][i]["count"]))
        bootstrap_peer_count = 0
        if i != 0:
            bootstrap_peer_count = sum(org_peer_count) - org_peer_count[i]
        
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