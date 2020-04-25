package utils

import (
	"bufio"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"net/url"
	"os"
	"os/exec"
	"path/filepath"
	"reflect"
	"strconv"
	"strings"

	strfmt "github.com/go-openapi/strfmt"
	uuid "github.com/google/uuid"
	log "github.com/sirupsen/logrus"
)

// NewUUID is creating a new unique identifier in UUID v4 format
func NewUUID() strfmt.UUID {
	return strfmt.UUID(uuid.New().String())
}

// CreateStringPointer returns the memory address of the string passed in input
func CreateStringPointer(s string) *string {
	return &s
}

// AsJSON returns the input object in a JSON format
func AsJSON(object interface{}) string {
	prettyJSON, err := json.MarshalIndent(object, "", "    ")
	if err != nil {
		log.Warningln("Error in printing as json. Returning empty string.")
		return ""
	}

	return string(prettyJSON)
}

//MapKeyToArray returns the map keys as a string array
func MapKeyToArray(object interface{}) []string {
	keys := reflect.ValueOf(object).MapKeys()
	strkeys := make([]string, len(keys))
	for i := 0; i < len(keys); i++ {
		strkeys[i] = keys[i].String()
	}

	return strkeys
}

//QueryParamsToMap parses the values from the query string to be used by the API
func QueryParamsToMap(path string) url.Values {
	path = normalise(path)
	log.Debugln("Path with params: ", path)

	u, _ := url.Parse(path)
	q, _ := url.ParseQuery(u.RawQuery)

	return q
}

//Used to convert any escaped characters back to ASCII
func normalise(s string) string {
	s = strings.ReplaceAll(s, "\\u0026", "&")
	s = strings.ReplaceAll(s, "\"", "")

	return s
}

//AsUniqueSlice returns a slice with unique values
func AsUniqueSlice(slice []string) []string {
	keys := make(map[string]bool)
	list := []string{}

	for _, entry := range slice {
		if _, value := keys[entry]; !value {
			keys[entry] = true
			list = append(list, entry)
		}
	}

	return list
}

//MapStructFieldToJSONTag maps the struct field value to the json tag
func MapStructFieldToJSONTag(object interface{}) map[string]string {
	m := make(map[string]string)
	val := reflect.ValueOf(object)
	for i := 0; i < val.Type().NumField(); i++ {
		tag := val.Type().Field(i).Tag.Get("json")
		//Need only the tag name, not properties
		key := strings.Split(tag, ",")
		m[key[0]] = val.Type().Field(i).Name
	}
	log.Debugln("Map: ", m)

	return m
}

//DecodeJSON implements encoding from any structure to a new JSON structure
func DecodeJSON(input interface{}, output interface{}) error {
	data, err := json.Marshal(input)
	if err != nil {
		return errors.New("Unable to retrieve data: " + err.Error())
	}
	err = json.Unmarshal(data, output)
	if err != nil {
		return errors.New("Unable to retrieve data: " + err.Error())
	}

	return nil
}

//DeleteFromStructSlice removes an object from a slice of struct objects, if a value is equal to a certain field
func DeleteFromStructSlice(value, field string, list interface{}) {
	listReflect := reflect.ValueOf(list).Elem()
	for i := 0; i < listReflect.Len(); i++ {
		val := reflect.Indirect(listReflect.Index(i))
		if value == val.FieldByName(field).Interface().(string) {
			result := reflect.AppendSlice(listReflect.Slice(0, i), listReflect.Slice(i+1, listReflect.Len()))
			listReflect.Set(result)
			break
		}
	}
}

//FilterStructFields will filter an wrt to the corresponding argument passed to the function
func FilterStructFields(filters []string, fieldToJSONTagMap map[string]string, object interface{}) {
	filterMap := make(map[string]bool)
	for _, filter := range filters {
		filterMap[fieldToJSONTagMap[filter]] = true
	}

	v := reflect.ValueOf(object).Elem()
	for i := 0; i < v.NumField(); i++ {
		if _, exists := filterMap[v.Type().Field(i).Name]; !exists {
			log.Debugln("Going to delete value for: ", v.Type().Field(i).Name)
			field := v.FieldByName(v.Type().Field(i).Name)
			zeroValue := reflect.Zero(v.Field(i).Type())
			field.Set(zeroValue)
		}
	}
}

// ConvertStringArray will convert the string array into a specified type
func ConvertStringArray(strArr []string, arrType string) (interface{}, error) {
	switch arrType {
	case "bool":
		newArr := []bool{}
		for _, val := range strArr {
			if newVal, err := strconv.ParseBool(val); err == nil {
				newArr = append(newArr, newVal)
			} else {
				return nil, err
			}
		}
		return newArr, nil
	case "float64":
		newArr := []float64{}
		for _, val := range strArr {
			if newVal, err := strconv.ParseFloat(val, 64); err == nil {
				newArr = append(newArr, newVal)
			} else {
				return nil, err
			}
		}
		return newArr, nil
	default:
		return nil, errors.New("Cannot parse array")
	}
}

func CreateFile(fileName string) (*os.File, error) {
	dir, err := os.Getwd()
	if err != nil {
		return nil, err
	}

	file, err := os.Create(filepath.Join(dir, fileName))
	if err != nil {
		return nil, err
	}

	return file, nil
}

func WriteFile(fileName string, bytes []byte) error {
	err := ioutil.WriteFile(fileName, bytes, 0644)
	if err != nil {
		return err
	}

	return nil
}

// RunScript runs the python script
func RunScript(script string, args string) error {
	cmd := exec.Command("python3", "./scripts/"+script, args)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return err
	}
	stderr, err := cmd.StderrPipe()
	if err != nil {
		return err
	}
	err = cmd.Start()
	if err != nil {
		return err
	}

	go copyOutput(stdout)
	go copyOutput(stderr)
	cmd.Wait()

	return nil
}

func copyOutput(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
}
