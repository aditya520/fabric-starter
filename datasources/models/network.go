package models

import "fabric_starter/models"

type Object struct {

	// channel
	Channel []*models.Channel `json:"channel"`

	// e policy
	EPolicy *models.EPolicy `json:"e_policy,omitempty"`

	// network
	Organisation Organisation `json:"network,omitempty"`
}

type Organisation struct {
	PeerOrg    []PeerOrg  `json:"peerOrgs"`
	OrdererOrg OrdererOrg `json:"ordererOrg"`
}

type PeerOrg struct {
	URL   string `json:"url"`
	Count int    `json:"count"`
	MspID string `json:"mspID"`
}

type OrdererOrg struct {
	URL       []string `json:"url"`
	Consensus string   `json:"consensus"`
	MspID     string   `json:"mspID"`
}
