import sys
import os
import time
import subprocess

## ENV files ##

CHAINCODE_UTIL_CONTAINER="cli"
ORDERER_ADDRESS="orderer0.everledger.com:7050"
CHANNELS_CONFIG_PATH="/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts"
TLS_CA_FILE = "/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/everledger.com/orderers/orderer0.everledger.com/msp/tlscacerts/tlsca.everledger.com-cert.pem"


###Create channel ##
##TODO: Join all peers to org and in
##TODO: Multi channel support ##
def initNetwork(jsonData):
    
    CHANNEL_NAME = jsonData["channel"][0]["name"]
    
    # Create Channel #
    print("")
    print("Create channel...")
    print("")
    sys.stdout.flush()
    os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer channel create -o "+ORDERER_ADDRESS+" -c "+CHANNEL_NAME+" -f "+CHANNELS_CONFIG_PATH+"/channel.tx --tls --cafile "+TLS_CA_FILE)


    # Join Channel ##
    print("")
    print("Join Channel...")
    print("")
    sys.stdout.flush()
    
    port = 7051  
    for i in range(0, len(jsonData["organizations"]["peerOrgs"])):
        org = jsonData["organizations"]["peerOrgs"][i]
        mspEnv = "CORE_PEER_LOCALMSPID="+org["mspID"]
        mspConfigEnv = "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+org["url"]+"/users/Admin@"+org["url"]+"/msp"
        addEnv = "CORE_PEER_ADDRESS=peer0."+org["url"] + ":" + str(port)
        tlsEnv = "CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+org["url"]+"/peers/peer0."+org["url"]+"/tls/ca.crt"
        env = mspEnv + " " + mspConfigEnv + " " + addEnv + " " + tlsEnv + " "
        
        print("ENV for ",org["name"])
        print(env)
        print("")
        
        command = "docker exec cli /bin/bash -c '"+env+"peer channel join -b "+CHANNEL_NAME+".block'"
        os.system(command)
        command = "docker exec cli /bin/bash -c '"+env+"peer channel update -o "+ORDERER_ADDRESS+" -c "+CHANNEL_NAME+" -f ./channel-artifacts/"+ org["mspID"] +"anchors.tx --tls --cafile " + TLS_CA_FILE + "'"
        os.system(command)
        port = port + (org["count"]*1000)
    

    # chaincode Dependecies ##
    print("")
    print("chaincode Dependecies...")
    print("")
    sys.stdout.flush()
    
    os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'cd /opt/gopath/src/github.com/hyperledger/fabric-samples/chaincode/abstore/go && export GO111MODULE=on && go mod vendor && cd -'")

    # Package Chaincode ##
    print("")
    print("Package Chaincode...")
    print("")
    sys.stdout.flush()
    
    os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode package mycc.tar.gz --path github.com/hyperledger/fabric-samples/chaincode/abstore/go/ --lang golang --label mycc_1")

    # Installing Chaincode First Org##
    print("")
    print("Installing Chaincode First Org...")
    print("")
    sys.stdout.flush()
    
    os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode install mycc.tar.gz")

    # # Querying Chaincode
    print("")
    print("Querying Chaincode...")
    print("")
    sys.stdout.flush()
    
    PACKAGE_ID_OUTPUT=subprocess.check_output("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode queryinstalled 2>&1 | awk -F \"[, ]+\" '/Label: /{print $3}'",shell=True)
    PACKAGE_ID = str(PACKAGE_ID_OUTPUT,'utf-8').rstrip()
    os.environ["PACKAGE_ID"] = PACKAGE_ID
    print(PACKAGE_ID)
    
    # ## Installing Chaincode  Other org##
    print("")
    print("Installing Chaincode on Other Orgs...")
    print("")
    sys.stdout.flush()
    
    port = 7051 + (jsonData["organizations"]["peerOrgs"][0]["count"]*1000)
    for i in range(1, len(jsonData["organizations"]["peerOrgs"])):
        org = jsonData["organizations"]["peerOrgs"][i]
        mspEnv = "CORE_PEER_LOCALMSPID="+org["mspID"]
        mspConfigEnv = "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+org["url"]+"/users/Admin@"+org["url"]+"/msp"
        addEnv = "CORE_PEER_ADDRESS=peer0."+org["url"] + ":" + str(port)
        tlsEnv = "CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+org["url"]+"/peers/peer0."+org["url"]+"/tls/ca.crt"
        env = mspEnv + " " + mspConfigEnv + " " + addEnv + " " + tlsEnv + " "
        command = "docker exec cli /bin/bash -c '" + env +"peer lifecycle chaincode install mycc.tar.gz'"
        os.system(command)
        port = port + (org["count"]*1000)


    # ## Approve Chaincode ##
    print("")
    print("Approve Chaincode for All Orgs..")
    print("")
    sys.stdout.flush()
    
    port = 7051
    for i in range(0, len(jsonData["organizations"]["peerOrgs"])):
        org = jsonData["organizations"]["peerOrgs"][i]
        mspEnv = "CORE_PEER_LOCALMSPID="+org["mspID"]
        mspConfigEnv = "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+org["url"]+"/users/Admin@"+org["url"]+"/msp"
        addEnv = "CORE_PEER_ADDRESS=peer0."+org["url"] + ":" + str(port)
        tlsEnv = "CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/"+org["url"]+"/peers/peer0."+org["url"]+"/tls/ca.crt"
        env = mspEnv + " " + mspConfigEnv + " " + addEnv + " " + tlsEnv + " "
        command = "docker exec cli /bin/bash -c '" + env + "peer lifecycle chaincode approveformyorg --channelID "+CHANNEL_NAME+" --name mycc --version 1.0 --init-required --package-id " + PACKAGE_ID + " --sequence 1 --tls true --cafile " + TLS_CA_FILE + "'" 
        os.system(command)
        port = port + (org["count"]*1000)


    ## Check commit Readiness
    print("")
    print("Check commit Readiness...")
    print("")
    sys.stdout.flush()
    
    os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode checkcommitreadiness --channelID "+CHANNEL_NAME+" --name mycc --version 1.0 --init-required --sequence 1 --tls true --cafile "+TLS_CA_FILE+" --output json")

    ## Commit the chaincode
    print("")
    print("Commit the chaincode...")
    print("")
    sys.stdout.flush()
    
    commandSuffix = ""
    port = 7051
    for i in range(0, len(jsonData["organizations"]["peerOrgs"])):
        org = jsonData["organizations"]["peerOrgs"][i]
        commandSuffix = commandSuffix + " --peerAddresses peer0."+org["url"]+":" + str(port) + " --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/" + org["url"] + "/peers/peer0." + org["url"] + "/tls/ca.crt"
        port = port + (org["count"]*1000)

    os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode commit -o "+ORDERER_ADDRESS+" --channelID "+CHANNEL_NAME+" --name mycc --version 1.0 --sequence 1 --init-required --tls true --cafile "+ TLS_CA_FILE + commandSuffix)
    


    ### Invoking the chaincode
    print("")
    print("Invoking the chaincode...")
    print("")
    sys.stdout.flush()
    
    os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer chaincode invoke -o "+ORDERER_ADDRESS+" --isInit --tls true --cafile "+TLS_CA_FILE+" -C "+CHANNEL_NAME+" -n mycc" + commandSuffix + " -c '{\"Args\":[\"Init\",\"a\",\"100\",\"b\",\"200\"]}' --waitForEvent")


