
import os
import sys
import pyaml
import json
import yaml


def create_docker_compose_cli(jsonData):
    ###### HardCoded Values ######
    # n_orgs = args[1]
    # n_peer_org = args[2]
    peer_name = "peer"
    # TODO: Update to take value from json 
    network_name = ["byfn"]

    with open("./network/template/docker-compose-cli-template.yaml") as f:
        list_doc = yaml.load(f)

    #### Networks ####
    list_doc["version"] = "'" + str(2) + "'"

    networks = dict.fromkeys(network_name,)
    list_doc["networks"] = networks

    #### Volumes ####

    ## Orderer Volume ##
    org_final_name = []
    for orderer in jsonData["organizations"]["ordererOrg"]["url"]:
        org_final_name.append(orderer)

    ### ORG Volumes ###
    for i in range(0, len(jsonData["organizations"]["peerOrgs"])):
        org = jsonData["organizations"]["peerOrgs"][i]["url"]
        for peer in range(0, int(jsonData["organizations"]["peerOrgs"][i]["count"])):
            orgName = peer_name + str(peer) + "." + org
            org_final_name.append(orgName)


    volumes = dict.fromkeys(org_final_name,)
    list_doc["volumes"] = volumes

    #### Services ####

    services = {}

    for org in org_final_name:
        if not org in services:
            services[org] = {}
        if not "extends" in services[org]:
            services[org]["extends"] = {}

        if not "service" in services[org]["extends"]:
            services[org]["extends"]["service"] = {}
        if not "file" in services[org]["extends"]:
            services[org]["extends"]["file"] = {}

        if not "container_name" in services[org]:
            services[org]["container_name"] = {}
        if not "networks" in services[org]:
            services[org]["networks"] = {}

        services[org]["extends"]["service"] = org
        services[org]["extends"]["file"] = "base/docker-compose-base.yaml"
        services[org]["container_name"] = org
        services[org]["networks"] = network_name

    list_doc["services"].update(services)


    #### Services CLI ####


    for i in range (0, len(list_doc["services"]["cli"]["environment"])):
        env = list_doc["services"]["cli"]["environment"][i]
        if list_doc["services"]["cli"]["environment"][i].find("org1") != -1:
            env = env.replace("org1",jsonData["organizations"]["peerOrgs"][0]["name"])
        if list_doc["services"]["cli"]["environment"][i].find("Org1MSP") != -1:
            env = env.replace("Org1MSP",jsonData["organizations"]["peerOrgs"][0]["mspID"])
            
        list_doc["services"]["cli"]["environment"][i] = env

            

    list_doc["services"]["cli"]["depends_on"] = org_final_name
    list_doc["services"]["cli"]["networks"] = network_name
    # print (list_doc["services"])


    with open("./network/docker-compose-cli.yaml", "w+") as f:
        pyaml.dump(list_doc, f, vspacing=[2, 1])

    # print (list_doc)
