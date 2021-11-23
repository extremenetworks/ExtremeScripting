package main

/*
#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######
*/

import (
	"encoding/json"
	"fmt"
	"sort"
	"strconv"
	"strings"
	"time"
)

/*
 ######   #######  ##    ##  ######  ########    ###    ##    ## ########  ######
##    ## ##     ## ###   ## ##    ##    ##      ## ##   ###   ##    ##    ##    ##
##       ##     ## ####  ## ##          ##     ##   ##  ####  ##    ##    ##
##       ##     ## ## ## ##  ######     ##    ##     ## ## ## ##    ##     ######
##       ##     ## ##  ####       ##    ##    ######### ##  ####    ##          ##
##    ## ##     ## ##   ### ##    ##    ##    ##     ## ##   ###    ##    ##    ##
 ######   #######  ##    ##  ######     ##    ##     ## ##    ##    ##     ######
*/

const (
	gqlDeviceListQuery string = `
		query {
			network {
				devices {
					up
					ip
				}
			}
		}
	`
	gqlMutationQuery string = `
		mutation {
			network {
				rediscoverDevices(input: {devices: [{ipAddress: "%s"}]}) {
					status
					message
				}
			}
		}
	`
	gqlDeviceDataQuery string = `
		query {
			network {
				device(ip: "%s") {
					id
					up
					sysName
					sysLocation
					nickName
					baseMac
					ip
					entityData {
						allPorts {
							ifIndex
							ifName
							ifOperStatus
							vlanList
						}
					}
				}
				deviceVlans(ip: "%s") {
					vid
				}
			}
		}
	`
)

/*
######## ##    ## ########  ########  ######
   ##     ##  ##  ##     ## ##       ##    ##
   ##      ####   ##     ## ##       ##
   ##       ##    ########  ######    ######
   ##       ##    ##        ##             ##
   ##       ##    ##        ##       ##    ##
   ##       ##    ##        ########  ######
*/

// Used for parsing the list of devices returned by XMC
type deviceList struct {
	Data struct {
		Network struct {
			Devices []struct {
				Up bool   `json:"up"`
				IP string `json:"ip"`
			} `json:"devices"`
		} `json:"network"`
	} `json:"data"`
}

// Used to parse the result of each single mutation (device refresh)
type mutationMessage struct {
	Data struct {
		Network struct {
			RediscoverDevices struct {
				Status  string `json:"status"`
				Message string `json:"message"`
			} `json:"rediscoverDevices"`
		} `json:"network"`
	} `json:"data"`
}

// Used to store the result of ports and VLANs for each single device
type deviceData struct {
	Data struct {
		Network struct {
			Device struct {
				ID          int    `json:"id"`
				Up          bool   `json:"up"`
				SysName     string `json:"sysName"`
				SysLocation string `json:"sysLocation"`
				NickName    string `json:"nickName"`
				BaseMac     string `json:"baseMac"`
				IP          string `json:"ip"`
				EntityData  struct {
					AllPorts []struct {
						IfIndex      int      `json:"ifIndex"`
						IfName       string   `json:"ifName"`
						IfOperStatus string   `json:"ifOperStatus"`
						VlanList     []string `json:"vlanList"`
					} `json:"allPorts"`
				} `json:"entityData"`
			} `json:"device"`
			DeviceVlans []struct {
				Vid int `json:"vid"`
			} `json:"deviceVlans"`
		} `json:"network"`
	} `json:"data"`
}

// Used to store the values for each row that is written to outfile
type resultSet struct {
	ID          int
	BaseMac     string
	IP          string
	SysUpDown   string
	SysName     string
	SysLocation string
	IfName      string
	IfStatus    string
	Untagged    []string
	Tagged      []string
}

// Convert a single resultSet to an array
func (rs *resultSet) ToArray() []string {
	retVal := []string{strconv.Itoa(rs.ID), rs.BaseMac, rs.IP, rs.SysUpDown, rs.SysName, rs.SysLocation, rs.IfName, rs.IfStatus, strings.Join(rs.Untagged, ","), strings.Join(rs.Tagged, ",")}
	return retVal
}

/*
######## ##     ## ##    ##  ######   ######
##       ##     ## ###   ## ##    ## ##    ##
##       ##     ## ####  ## ##       ##
######   ##     ## ## ## ## ##        ######
##       ##     ## ##  #### ##             ##
##       ##     ## ##   ### ##    ## ##    ##
##        #######  ##    ##  ######   ######
*/

// Fetches the complete list of managed devices from XMC
func discoverManagedDevices() ([]string, []string) {
	stdErr.Println("Discovering managed devices...")

	body, bodyErr := client.QueryAPI(gqlDeviceListQuery)
	if bodyErr != nil {
		stdErr.Fatalf("Could not fetch device list: %s\n", bodyErr)
	}
	proactiveTokenRefresh()

	devices := deviceList{}
	jsonErr := json.Unmarshal(body, &devices)
	if jsonErr != nil {
		stdErr.Fatalf("Could not decode JSON: %s\n", jsonErr)
	}

	var upDevices []string
	var downDevices []string
	for _, d := range devices.Data.Network.Devices {
		if d.Up {
			upDevices = append(upDevices, d.IP)
		} else {
			downDevices = append(downDevices, d.IP)
		}
	}
	sort.Strings(upDevices)
	stdErr.Println("Finished discovering managed devices.")

	return upDevices, downDevices
}

// Triggers a rediscover for a list of devices
func rediscoverDevices(ipList []string) []string {
	var rediscoveredDevices []string
	for _, deviceIP := range ipList {
		body, bodyErr := client.QueryAPI(fmt.Sprintf(gqlMutationQuery, deviceIP))
		if bodyErr != nil {
			stdErr.Printf("Could not mutate device %s: %s\n", deviceIP, bodyErr)
			continue
		}
		proactiveTokenRefresh()

		mutation := mutationMessage{}
		jsonErr := json.Unmarshal(body, &mutation)
		if jsonErr != nil {
			stdErr.Printf("Could not decode JSON: %s\n", jsonErr)
			continue
		}

		if mutation.Data.Network.RediscoverDevices.Status == "SUCCESS" {
			stdErr.Printf("Successfully triggered rediscover for %s.\n", deviceIP)
			rediscoveredDevices = append(rediscoveredDevices, deviceIP)
		} else {
			stdErr.Printf("Rediscover for %s failed: %s\n", deviceIP, mutation.Data.Network.RediscoverDevices.Message)
		}

		stdErr.Printf("Waiting for %d second(s)...\n", config.RefreshInterval)
		time.Sleep(time.Second * time.Duration(config.RefreshInterval))
	}
	for i := config.RefreshWait; i > 0; i-- {
		proactiveTokenRefresh()
		stdErr.Printf("Waiting for %d minute(s) to finish rediscover...\n", i)
		time.Sleep(time.Minute * time.Duration(1))
	}
	return rediscoveredDevices
}

// Fetches the detailed data for a single device from XMC
func queryDevice(deviceIP string) ([]resultSet, error) {
	var deviceResult []resultSet

	body, bodyErr := client.QueryAPI(fmt.Sprintf(gqlDeviceDataQuery, deviceIP, deviceIP))
	if bodyErr != nil {
		return deviceResult, fmt.Errorf("Could not query device %s: %s", deviceIP, bodyErr)
	}
	proactiveTokenRefresh()

	jsonData := deviceData{}
	jsonErr := json.Unmarshal(body, &jsonData)
	if jsonErr != nil {
		return deviceResult, fmt.Errorf("Could not decode JSON: %s", jsonErr)
	}

	device := jsonData.Data.Network.Device
	vlans := jsonData.Data.Network.DeviceVlans
	ports := jsonData.Data.Network.Device.EntityData.AllPorts

	stdErr.Printf("Fetched data for %s: Got %d VLANs and %d ports.\n", device.IP, len(vlans), len(ports))

	systemResult := resultSet{}
	systemResult.ID = device.ID
	systemResult.BaseMac = device.BaseMac
	systemResult.IP = device.IP
	systemResult.SysUpDown = "down"
	if device.Up {
		systemResult.SysUpDown = "up"
	}
	systemResult.SysName = device.SysName
	systemResult.SysLocation = device.SysLocation
	systemResult.IfName = "SYSTEM"
	systemResult.IfStatus = "N/A"
	for _, vlan := range vlans {
		systemResult.Tagged = append(systemResult.Tagged, strconv.Itoa(vlan.Vid))
	}
	deviceResult = append(deviceResult, systemResult)

	for _, port := range ports {
		portResult := resultSet{}
		portResult.ID = device.ID
		portResult.BaseMac = device.BaseMac
		portResult.IP = device.IP
		portResult.SysUpDown = "down"
		if device.Up {
			portResult.SysUpDown = "up"
		}
		portResult.SysName = device.SysName
		portResult.SysLocation = device.SysLocation
		portResult.IfName = port.IfName
		portResult.IfStatus = port.IfOperStatus
		for _, vlan := range port.VlanList {
			if strings.Contains(vlan, "Untagged") {
				portResult.Untagged = append(portResult.Untagged, strings.Split(vlan, "[")[0])
			} else if strings.Contains(vlan, "Tagged") {
				portResult.Tagged = append(portResult.Tagged, strings.Split(vlan, "[")[0])
			}
		}
		deviceResult = append(deviceResult, portResult)
	}

	return deviceResult, nil
}
