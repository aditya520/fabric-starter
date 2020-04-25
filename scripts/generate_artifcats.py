import sys
import os

# def create_artifacts():
os.system("which cryptogen")

cur_dir = os.getcwd() 
file_list = os.listdir(cur_dir)



### Certificates ###
os.system("cryptogen generate --config=./crypto-config/final_files/crypto-config.yaml")

os.system("export FABRIC_CFG_PATH=$PWD")


### orderer genesis block ###

os.system("configtxgen -profile SampleMultiNodeEtcdRaft -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block")

