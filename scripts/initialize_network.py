import sys
import os
import time

## ENV files ##

CHAINCODE_UTIL_CONTAINER="cli"
ORDERER_ADDRESS="orderer0.example.com:7050"
CHANNEL_NAME="mychannel"
CHANNELS_CONFIG_PATH="/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts"
TLS_CA_FILE = "/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer0.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"



## Create channel ##
## TODO: Multi channel support ##
# os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer channel create -o "
#           +ORDERER_ADDRESS+" -c "
#           +CHANNEL_NAME+" -f "+CHANNELS_CONFIG_PATH+"/channel.tx --tls --cafile "+TLS_CA_FILE)



## Join Channel ##
# os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer channel join -b "+CHANNEL_NAME+".block")


## ORG 2 join channel ##

#os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp && export CORE_PEER_ADDRESS=peer0.org2.example.com:9051 CORE_PEER_LOCALMSPID='Org2MSP' && export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt && peer channel join -b mychannel.block'")


### Update Anchor Peers  ORG1 ###
#os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer channel update -o "+ORDERER_ADDRESS+" -c "+CHANNEL_NAME+" -f ./channel-artifacts/Org1MSPanchors.tx --tls --cafile "+TLS_CA_FILE)

### Update Anchor Peers ORG2 ###
os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" /bin/bash -c 'export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp && export CORE_PEER_ADDRESS=peer0.org2.example.com:9051 CORE_PEER_LOCALMSPID='Org2MSP' && export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt && peer channel update -o "+ORDERER_ADDRESS+" -c "+CHANNEL_NAME+" -f ./channel-artifacts/Org2MSPanchors.tx --tls --cafile '"+TLS_CA_FILE)










# docker run --rm     -e CORE_PEER_MSPCONFIGPATH= "/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp" \
#                     -e CORE_PEER_ADDRESS="peer0.org2.example.com:9051"
#                     -e CORE_PEER_LOCALMSPID="Org2MSP"
#                     -e CORE_PEER_TLS_ROOTCERT_FILE="/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"
#                     hyperledger/fabric-tools:${FABRIC_VERSION} \
#                     configtxgen -profile $channel_profile -outputAnchorPeersUpdate /channels/${channel_name}/${org_msp}_anchors_tx.pb -channelID $channel_name -asOrg $org_msp /configtx.yaml

############ Getting inside docker method ###############

# os.system("docker exec -it cli bash")
# time.sleep(2)



# ### Create channel ###

# os.system("CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp")
# os.system("CORE_PEER_ADDRESS=peer0.org1.example.com:7051")
# os.system("CORE_PEER_LOCALMSPID='Org1MSP'")
# os.system("CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
# os.system("echo lol")