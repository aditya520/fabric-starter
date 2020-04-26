import sys
import os
import time
import subprocess

## ENV files ##

CHAINCODE_UTIL_CONTAINER="cli"
ORDERER_ADDRESS="orderer0.example.com:7050"
CHANNEL_NAME="mychannel"
CHANNELS_CONFIG_PATH="/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts"
TLS_CA_FILE = "/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer0.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"


###Create channel ##
##TODO: Multi channel support ##
print("Create channel...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer channel create -o "
          +ORDERER_ADDRESS+" -c "
          +CHANNEL_NAME+" -f "+CHANNELS_CONFIG_PATH+"/channel.tx --tls --cafile "+TLS_CA_FILE)



# Join Channel ##
print("Join Channel...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer channel join -b "+CHANNEL_NAME+".block")


# ORG 2 join channel ##
print("ORG 2 join channel...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp && export CORE_PEER_ADDRESS=peer0.org2.example.com:9051 CORE_PEER_LOCALMSPID='Org2MSP' && export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt && peer channel join -b mychannel.block'")


## Update Anchor Peers  ORG1 ###
print("Update Anchor Peers  ORG1...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer channel update -o "+ORDERER_ADDRESS+" -c "+CHANNEL_NAME+" -f ./channel-artifacts/Org1MSPanchors.tx --tls --cafile "+TLS_CA_FILE)

### Update Anchor Peers ORG2 ###
print("pdate Anchor Peers ORG2...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp && export CORE_PEER_ADDRESS=peer0.org2.example.com:9051 CORE_PEER_LOCALMSPID='Org2MSP' && export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt && peer channel update -o "+ORDERER_ADDRESS+" -c "+CHANNEL_NAME+" -f ./channel-artifacts/Org2MSPanchors.tx --tls --cafile '"+TLS_CA_FILE)

# chaincode Dependecies ##
print("chaincode Dependecies...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'cd /opt/gopath/src/github.com/hyperledger/fabric-samples/chaincode/abstore/go && export GO111MODULE=on && go mod vendor && cd -'")

# Package Chaincode ##
print("Package Chaincode...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode package mycc.tar.gz --path github.com/hyperledger/fabric-samples/chaincode/abstore/go/ --lang golang --label mycc_1")

# Installing Chaincode Org 1##
print("Installing Chaincode Org 1...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode install mycc.tar.gz")

# # Querying Chaincode
print("Querying Chaincode...")
sys.stdout.flush()
PACKAGE_ID_OUTPUT=subprocess.check_output("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode queryinstalled 2>&1 | awk -F \"[, ]+\" '/Label: /{print $3}'",shell=True)
PACKAGE_ID = str(PACKAGE_ID_OUTPUT,'utf-8').rstrip()
os.environ["PACKAGE_ID"] = PACKAGE_ID
print(PACKAGE_ID)

# ## Installing Chaincode Org 2##
print("Installing Chaincode Org 2...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp && export CORE_PEER_ADDRESS=peer0.org2.example.com:9051 && export CORE_PEER_LOCALMSPID='Org2MSP' && export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt && peer lifecycle chaincode install mycc.tar.gz'")


# ## Approve Chaincode for Org1 ##
print("Approve Chaincode for Org1..")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp && export CORE_PEER_ADDRESS=peer0.org1.example.com:7051 && export CORE_PEER_LOCALMSPID='Org1MSP' && export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt && peer lifecycle chaincode approveformyorg --channelID "+CHANNEL_NAME+" --name mycc --version 1.0 --init-required --package-id "+PACKAGE_ID+" --sequence 1 --tls true --cafile '"+TLS_CA_FILE)

# ## Approve Chaincode for Org2 ##
print("Approve Chaincode for Org2...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp && export CORE_PEER_ADDRESS=peer0.org2.example.com:9051 && export CORE_PEER_LOCALMSPID='Org2MSP' && export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt && peer lifecycle chaincode approveformyorg --channelID "+CHANNEL_NAME+" --name mycc --version 1.0 --init-required --package-id "+PACKAGE_ID+" --sequence 1 --tls true --cafile '"+TLS_CA_FILE)


# # ## Approve Chaincode for Org1 ##
# print("Approve Chaincode for Org1..")
# sys.stdout.flush()
# os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp && export CORE_PEER_ADDRESS=peer0.org1.example.com:7051 && export CORE_PEER_LOCALMSPID='Org1MSP' && export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt && peer lifecycle chaincode approveformyorg --channelID "+CHANNEL_NAME+" --name mycc --version 1.0 --init-required --package-id "+PACKAGE_ID+" --sequence 1 --tls true --cafile '"+TLS_CA_FILE)

## Check commit Readiness
print("Check commit Readiness...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode checkcommitreadiness --channelID "+CHANNEL_NAME+" --name mycc --version 1.0 --init-required --sequence 1 --tls true --cafile "+TLS_CA_FILE+" --output json")


## Commit the chaincode
print("Commit the chaincode...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer lifecycle chaincode commit -o "+ORDERER_ADDRESS+" --channelID "+CHANNEL_NAME+" --name mycc --version 1.0 --sequence 1 --init-required --tls true --cafile "+TLS_CA_FILE+" --peerAddresses peer0.org1.example.com:7051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses peer0.org2.example.com:9051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt")


### Invoking the chaincode
print("Invoking the chaincode...")
sys.stdout.flush()
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer chaincode invoke -o "+ORDERER_ADDRESS+" --isInit --tls true --cafile "+TLS_CA_FILE+" -C "+CHANNEL_NAME+" -n mycc --peerAddresses peer0.org1.example.com:7051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses peer0.org2.example.com:9051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{\"Args\":[\"Init\",\"a\",\"100\",\"b\",\"100\"]}' --waitForEvent")



