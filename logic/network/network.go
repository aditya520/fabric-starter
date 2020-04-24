package network

import (
	"encoding/json"
	"fabric_starter/common/utils"
	fileModels "fabric_starter/datasources/models"
	"fabric_starter/models"
	"strconv"
	"strings"
)

func CreateNetwork(networkObj *models.Object) (string, error) {

	fileName := "fixtures/" + networkObj.Name + ".json"
	var obj fileModels.Object
	obj.Channel = networkObj.Channel
	obj.EPolicy = networkObj.EPolicy

	domain := ".example.com"

	for i := 0; i < len(networkObj.Network.Orgs); i++ {
		count, err := strconv.Atoi(networkObj.Network.Orgs[i].NoOfPeers)
		if err != nil {
			return "", nil
		}
		mspID := strings.Title(strings.ToLower(networkObj.Network.Orgs[i].Name)) + "MSP"
		var peerOrgObj = fileModels.PeerOrg{
			Name:  networkObj.Network.Orgs[i].Name,
			URL:   networkObj.Network.Orgs[i].Name + domain,
			Count: count,
			MspID: mspID,
		}

		obj.Organisation.PeerOrg = append(obj.Organisation.PeerOrg, peerOrgObj)
	}

	obj.Organisation.OrdererOrg.URL = []string{networkObj.Network.Orderer.Name + domain}
	obj.Organisation.OrdererOrg.Consensus = networkObj.Network.Orderer.Consensus
	obj.Organisation.OrdererOrg.MspID = "OrdererMSP"

	file, err := utils.CreateFile(fileName)
	if err != nil {
		return "", err
	}
	file.Close()

	bytes, err := json.MarshalIndent(obj, "", "    ")

	err = utils.WriteFile(fileName, bytes)
	if err != nil {
		return "", nil
	}

	utils.RunScript(fileName)
	return "Success", nil
}
