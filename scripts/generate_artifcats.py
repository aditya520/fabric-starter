import sys
import os

# def create_artifacts():
# os.system("which cryptogen")

# cur_dir = os.getcwd()
# file_list = os.listdir(cur_dir)

def create_artifacts(jsonData):

    print("")
    print("Generating artifacts...")
    print("")
    sys.stdout.flush()
    ### Certificates ###
    os.system("cryptogen generate --config=./network/crypto-config.yaml --output=./network/crypto-config")

    ### orderer genesis block ###

    os.system("configtxgen -profile SampleMultiNodeEtcdRaft -channelID byfn-sys-channel -outputBlock ./network/channel-artifacts/genesis.block -configPath ./network")

    ### Setting up the env variable ###
    #TODO: Set up for multi channel

    for i in range(0,len(jsonData["channel"])):
        CHANNEL_NAME=jsonData["channel"][0]["name"]


    # print (jsonData)
    PROFILE_NAME = "TwoOrgsChannel"


    ### Channel Configuration Transaction ###

    os.system("configtxgen -profile "+PROFILE_NAME+" -outputCreateChannelTx ./network/channel-artifacts/channel.tx -configPath ./network -channelID "+ CHANNEL_NAME)

    os.system("configtxgen -profile "+PROFILE_NAME+" -outputAnchorPeersUpdate ./network/channel-artifacts/Org1MSPanchors.tx -configPath ./network -channelID "+ CHANNEL_NAME +" -asOrg Org1MSP")

    os.system("configtxgen -profile "+PROFILE_NAME+" -outputAnchorPeersUpdate ./network/channel-artifacts/Org2MSPanchors.tx -configPath ./network -channelID "+ CHANNEL_NAME +" -asOrg Org2MSP")


