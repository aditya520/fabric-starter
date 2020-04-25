import sys
import os
import time

# CHAINCODE_UTIL_CONTAINER="cli"
# ORDERER_ADDRESS="orderer0.example.com:7050"
# CHANNEL_NAME="mychannel"
# CHANNELS_CONFIG_PATH="/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts"
# TLS_CA_FILE = "/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer0.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"

# ## Create channel ##
# ## TODO: Multi channel support ##
# os.system("docker exec "+CHAINCODE_UTIL_CONTAINER+" peer channel create -o "
#           +ORDERER_ADDRESS+" -c "
#           +CHANNEL_NAME+" -f "+CHANNELS_CONFIG_PATH+"/channel.tx --tls --cafile "+TLS_CA_FILE+" || exit 1")


############ Getting inside docker method ###############

os.system("docker exec -it cli bash")
time.sleep(2)



### Create channel ###

os.system("CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp")
os.system("CORE_PEER_ADDRESS=peer0.org1.example.com:7051")
os.system("CORE_PEER_LOCALMSPID='Org1MSP'")
os.system("CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
os.system("echo lol")