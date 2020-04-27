import json
import os
import sys
import pyaml
import yaml
import time
import copy
import create_configtx as configtx
import create_crypto_config as crypto
import create_docker_base as dockerBase

def createConfigtx(jsonData,inputJson):
    peerCount = 0
    for org in inputJson["organizations"]["peerOrgs"]:
        peerCount = peerCount + org["count"]
        
    port = (peerCount)*1000 + 7051

    orgArr = configtx.create_org_config(jsonData,port)

    configtxObj = {
        "Organizations": orgArr
    }

    with open("./network/newOrg/"+jsonData["organizations"]["peerOrgs"][0]["name"]+"/configtx.yaml", "w+") as f:
        pyaml.dump(configtxObj, f, vspacing=[2, 1])
        
    return port


def createCryptoConfig(jsonData, inputJson):
    with open("./network/template/crypto-config-template.yaml") as f:
        crypto_doc = yaml.load(f)
    
    peerOrgsArr = crypto.create_crypto_orgs(jsonData,crypto_doc)
    
    cryptoObj = {
        "PeerOrgs": peerOrgsArr
    }
    
    with open("./network/newOrg/"+jsonData["organizations"]["peerOrgs"][0]["name"]+"/crypto-config.yaml", "w+") as f:
           pyaml.dump(cryptoObj, f, vspacing=[2, 1])


def createDockerCompose(jsonData, port):
    
    peerService = dockerBase.create_peer_base(jsonData,port)
    peerArr = []
    for i in range(0, jsonData["organizations"]["peerOrgs"][0]["count"]):
        peer = "peer" + str(i) + "." + jsonData["organizations"]["peerOrgs"][0]["url"]
        peerArr.append(peer)
        peerService[peer]["extends"]["file"] = "../../base/peer-base.yaml"
        peerService[peer]["networks"]={}
        peerService[peer]["networks"]=["byfn"]

        for i in range (0, len(peerService[peer]["volumes"])):
            if (peerService[peer]["volumes"][i].find("crypto-config") != -1):
                peerService[peer]["volumes"][i]="../"+peerService[peer]["volumes"][i]
    
    
    base = {
        "version" : "'" + str(2) + "'",
        "volumes": dict.fromkeys(peerArr,),
        "networks": dict.fromkeys(["byfn"],),
        "services": {**peerService}
    }
    
    with open("./network/newOrg/"+jsonData["organizations"]["peerOrgs"][0]["name"]+"/docker-compose.yaml", "w+") as f:
        pyaml.dump(base, f, vspacing=[2, 1])
    

def generateArtifactsAndConfig(name,mspID):
    print("")
    print("Generating artifacts for "+name+"...")
    print("")
    sys.stdout.flush()

    command = "./bin/cryptogen generate --config=./network/newOrg/" + name +"/crypto-config.yaml --output=./network/newOrg/"+name+"/crypto-config"
    
    os.system(command)
    
    command = "./bin/configtxgen -printOrg " + mspID + " > ./network/newOrg/" + name +"/"+ name +".json -configPath ./network/newOrg/" + name
    
    os.system(command)


def prepChannelUpdate(name,mspID,channelName):
    
    print("")
    print("Updating channel to add "+name+"...")
    print("")
    sys.stdout.flush()
    
    command = "docker exec cli peer channel fetch config config_block.pb -o orderer0.everledger.com:7050 -c " + channelName + " --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/everledger.com/orderers/orderer0.everledger.com/msp/tlscacerts/tlsca.everledger.com-cert.pem || exit 1"
    
    os.system(command)
    
    command = "docker exec cli /bin/bash -c 'configtxlator proto_decode --input config_block.pb --type common.Block | jq .data.data[0].payload.data.config > ./channel-artifacts/config.json' || exit 1"
    
    os.system(command)
    
    jqinput = "\".[0] * {\"channel_group\":{\"groups\":{\"Application\":{\"groups\": {\"" + mspID + "\":.[1]}}}}}\""
    command = "docker exec cli /bin/bash -c 'jq -s "+ jqinput +" ./channel-artifacts/config.json ./newOrg/" + name +"/"+ name +".json > ./channel-artifacts/modified_config.json'"
   
    os.system(command)
    
    command = "docker exec cli configtxlator proto_encode --input ./channel-artifacts/config.json --type common.Config --output config.pb"

    os.system(command)
    
    command = "docker exec cli configtxlator proto_encode --input ./channel-artifacts/modified_config.json --type common.Config --output modified_config.pb"
    
    os.system(command)
    
    command = "docker exec cli configtxlator compute_update --channel_id " + channelName + " --original config.pb --updated modified_config.pb --output update.pb"
    
    os.system(command)
     
    command = "docker exec cli /bin/bash -c 'configtxlator proto_decode --input update.pb --type common.ConfigUpdate | jq . > org_update.json'" 
    
    os.system(command)
    
    command = "docker exec cli /bin/bash -c 'echo \"{\\\"payload\\\":{\\\"header\\\":{\\\"channel_header\\\":{\\\"channel_id\\\":\\\""+ channelName + "\\\", \\\"type\\\":2}},\\\"data\\\":{\\\"config_update\\\":\"$(cat org_update.json)\"}}}\" > org_update_in_envelope.json'"
       
    os.system(command)
    
    command = "docker exec cli configtxlator proto_encode --input org_update_in_envelope.json --type common.Envelope --output org_update_in_envelope.pb"
    
    os.system(command)

    
def updateChannel(orgs, channelName):
    port = 7051
    for org in orgs:
        mspEnv = "CORE_PEER_LOCALMSPID="+org["mspID"]
        mspConfigEnv = "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+org["url"]+"/users/Admin@"+org["url"]+"/msp"
        addEnv = "CORE_PEER_ADDRESS="+org["url"] + ":" + str(port)
        tlsEnv = "CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+org["url"]+"/peers/peer0."+org["url"]+"/tls/ca.crt"
        
        env = mspEnv + " " + mspConfigEnv + " " + addEnv + " " + tlsEnv + " "

        command = "docker exec cli /bin/bash -c '"+ env +"peer channel signconfigtx -f org_update_in_envelope.pb'"
                
        os.system(command)
        
        port = port + (org["count"] * 1000)
      
    command = "docker exec cli peer channel update -f org_update_in_envelope.pb -c " + channelName +" -o orderer0.everledger.com:7050 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/everledger.com/orderers/orderer0.everledger.com/msp/tlscacerts/tlsca.everledger.com-cert.pem"
    os.system(command)



def joinChannel(jsonData, channelName, port):
    
    for i in range(0, jsonData["organizations"]["peerOrgs"][0]["count"]):
        mspEnv = "CORE_PEER_LOCALMSPID="+jsonData["organizations"]["peerOrgs"][0]["mspID"]
        mspConfigEnv = "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+jsonData["organizations"]["peerOrgs"][0]["url"]+"/users/Admin@"+jsonData["organizations"]["peerOrgs"][0]["url"]+"/msp"
        addEnv = "CORE_PEER_ADDRESS=peer"+ str(i)+ "." +jsonData["organizations"]["peerOrgs"][0]["url"] + ":" + str(port)
        tlsEnv = "CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+jsonData["organizations"]["peerOrgs"][0]["url"]+"/peers/peer"+str(i)+"."+jsonData["organizations"]["peerOrgs"][0]["url"]+"/tls/ca.crt"
        
        env = mspEnv + " " + mspConfigEnv + " " + addEnv + " " + tlsEnv + " "
        
        if i == 0:
            command = "docker exec cli /bin/bash -c '"+ env +"peer channel fetch 0 channel.block -o orderer0.everledger.com:7050 -c "+ channelName +" --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/everledger.com/orderers/orderer0.everledger.com/msp/tlscacerts/tlsca.everledger.com-cert.pem'"
            os.system(command)
        
        
        command = "docker exec cli /bin/bash -c '"+ env + "peer channel join -b channel.block'"
        os.system(command)
        
        port = port + 1000
        
    print("")
    print("Joined "+channelName)
    print("")
    sys.stdout.flush()


def startOrg(jsonData):
    
    print("")
    print("Starting "+jsonData["organizations"]["peerOrgs"][0]["name"]+" containers")
    print("")
    sys.stdout.flush()
    
    command = "cp -R ./network/newOrg/"+jsonData["organizations"]["peerOrgs"][0]["name"]+"/crypto-config/peerOrganizations/* ./network/crypto-config/peerOrganizations"
    os.system(command)
    
    command = "docker-compose -f ./network/newOrg/"+jsonData["organizations"]["peerOrgs"][0]["name"]+"/docker-compose.yaml up -d"
    
    os.system(command)
    
    time.sleep(3)



# START MAIN
path = sys.argv[1]

with open(path) as f:
    jsonData = json.load(f)

with open("./fixtures/"+jsonData["name"]+".json") as f:
    inputJson = json.load(f)
    
peerOrgs = copy.deepcopy(inputJson["organizations"]["peerOrgs"])
peerOrgs.append(jsonData["organizations"]["peerOrgs"][0])
    
os.mkdir("./network/newOrg/"+jsonData["organizations"]["peerOrgs"][0]["name"])

port = createConfigtx(jsonData,inputJson)
createCryptoConfig(jsonData, inputJson)
createDockerCompose(jsonData, port)

name = jsonData["organizations"]["peerOrgs"][0]["name"]
mspID = jsonData["organizations"]["peerOrgs"][0]["mspID"]
channelName = jsonData["channelName"]

generateArtifactsAndConfig(name,mspID)
prepChannelUpdate(name,mspID,channelName)

orgs = inputJson["organizations"]["peerOrgs"]

updateChannel(orgs, channelName)

startOrg(jsonData)
joinChannel(jsonData, channelName, port)

inputJson["organizations"]["peerOrgs"] = peerOrgs
with open("./fixtures/"+jsonData["name"]+".json", "w+") as f:
    json.dump(inputJson, f, ensure_ascii=False, indent=4)
