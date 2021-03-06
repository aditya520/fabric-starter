// Code generated by go-swagger; DO NOT EDIT.

package models

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"github.com/go-openapi/errors"
	strfmt "github.com/go-openapi/strfmt"
	"github.com/go-openapi/swag"
)

// ExtraOrg extra org
// swagger:model extraOrg
type ExtraOrg struct {

	// channel name
	ChannelName string `json:"channelName,omitempty"`

	// name
	Name string `json:"name,omitempty"`

	// org
	Org *Orgs `json:"org,omitempty"`
}

// Validate validates this extra org
func (m *ExtraOrg) Validate(formats strfmt.Registry) error {
	var res []error

	if err := m.validateOrg(formats); err != nil {
		res = append(res, err)
	}

	if len(res) > 0 {
		return errors.CompositeValidationError(res...)
	}
	return nil
}

func (m *ExtraOrg) validateOrg(formats strfmt.Registry) error {

	if swag.IsZero(m.Org) { // not required
		return nil
	}

	if m.Org != nil {
		if err := m.Org.Validate(formats); err != nil {
			if ve, ok := err.(*errors.Validation); ok {
				return ve.ValidateName("org")
			}
			return err
		}
	}

	return nil
}

// MarshalBinary interface implementation
func (m *ExtraOrg) MarshalBinary() ([]byte, error) {
	if m == nil {
		return nil, nil
	}
	return swag.WriteJSON(m)
}

// UnmarshalBinary interface implementation
func (m *ExtraOrg) UnmarshalBinary(b []byte) error {
	var res ExtraOrg
	if err := swag.ReadJSON(b, &res); err != nil {
		return err
	}
	*m = res
	return nil
}
