import yaml
import json

yaml.SafeDumper.ignore_aliases = lambda *args: True

with open('../samples/python-input.json') as f:
    jsonData = json.load(f)


with open("../docker-files/boilerplate_files/crypto-config-boilerplate.yaml") as f:
    crypto_doc = yaml.load(f)


n_user = 1 # Hardocded for now

peerOrgs = crypto_doc["PeerOrgs"]

for i in range(0, len(jsonData["organizations"]["peerOrgs"])):
    org = jsonData["organizations"]["peerOrgs"][i]["url"]
    org_peer_count = int(jsonData["organizations"]["peerOrgs"][i]["count"])

    if not "Name" in peerOrgs:
        peerOrgs["Name"] = jsonData["channel"][0]["orgs"][i]
    if not "Domain" in peerOrgs:
        peerOrgs["Domain"] = org
    if not "EnableNodeOUs" in peerOrgs:
        peerOrgs["EnableNodeOUs"] = "true"
    if not "Template" in peerOrgs:
        peerOrgs["Template"] = {}
        if not "Count" in peerOrgs["Template"]:
            peerOrgs["Template"]["Count"] = org_peer_count

    if not "Users" in peerOrgs:
        peerOrgs["Users"] = {}
        if not "Count" in peerOrgs["Users"]:
            peerOrgs["Users"]["Count"] = n_user


crypto_doc["PeerOrgs"].update(peerOrgs)

with open("../crypto-config/crypto-config.yaml", "w") as f:
        yaml.safe_dump(crypto_doc, f)

