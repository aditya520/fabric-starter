package models

import "fabric_starter/models"

type Object struct {

	// channel
	Channel []*models.Channel `json:"channel"`

	// e policy
	EPolicy *models.EPolicy `json:"e_policy,omitempty"`

	// network
	Organisation Organisation `json:"organizations,omitempty"`
}

type Organisation struct {
	PeerOrg    []PeerOrg  `json:"peerOrgs,omitempty"`
	OrdererOrg OrdererOrg `json:"ordererOrg,omitempty"`
}

type PeerOrg struct {
	Name  string `json:"name,omitempty"`
	URL   string `json:"url,omitempty"`
	Count int    `json:"count,omitempty"`
	MspID string `json:"mspID,omitempty"`
}

type OrdererOrg struct {
	URL       []string `json:"url,omitempty"`
	Consensus string   `json:"consensus,omitempty"`
	MspID     string   `json:"mspID,omitempty"`
}
