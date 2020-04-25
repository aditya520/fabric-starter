package models

type ExtraOrg struct {
	Name string `json:"name,omitempty"`

	ChannelName string `json:"channelName,omitempty"`

	Organisation Organisation `json:"organizations,omitempty"`
}
