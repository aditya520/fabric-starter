import sys
import os

# def create_artifacts():
# os.system("which cryptogen")

# cur_dir = os.getcwd() 
# file_list = os.listdir(cur_dir)

print("")
print("Generating artifacts...")
print("")
sys.stdout.flush()
### Certificates ###
os.system("./bin/cryptogen generate --config=./network/crypto-config.yaml --output=./network/crypto-config")

### orderer genesis block ###

os.system("./bin/configtxgen -profile SampleMultiNodeEtcdRaft -channelID byfn-sys-channel -outputBlock ./network/channel-artifacts/genesis.block -configPath ./network")



