# Author: Robert Heydenbluth
# Name: vlan_existencecheck.py
# Version: 0.2
# Purpose: Reads VID and VLAN-Name as key-value-pairs from /usr/local/cfg/vlan_list.csv (delimiter: ";") and checks the Switch for existence of those VLANs
# Status: Tested Successfully...
# Tested on versions: 22.5.1.7-patch1-2.xos, 21.1.3.7-xos
# Tested on ONIE version: 22.4.1.4.xos

# ipmort Extreme OS Class
import os

# VLAN Class 
class Vlan:
	# Number of VLANs checked
	checkedVLANs = 0
	# Number of VLANs which exist (ID)
	existingIDs = 0
	# Number of VLANs which exist (name)
	existingNames = 0
	# Number of VLANs where ID and Name do not exist
	creatableVLANs = 0
	# Number of VLANs with matching id and name (not case-sensitive)
	matchingVLANs = 0
	
	def __init__(self,vid="1",name="default"):
		# Vlan ID (TAG)
		self.__vid=vid
		# Vlan ID available
		self.__vidA=False
		# Vlan Name
		self.__name=name
		# Vlan Name available
		self.__nameA=False
		# Name and ID available
		self.__creatable=False
		# Name and ID on switch = in CSV
		self.__match=False
		
	def __del__(self):
		pass
	
	# Checks if VLAN ID exists on Switch
	def CheckVidAvailablitiy(self):
		tmp = exsh.clicmd("show vlan %s" % self.__vid, capture=True)
		if (tmp.find("VLAN Interface with name") != -1):
			self.__vidA=False
			Vlan.existingIDs+=1
		else:
			self.__vidA=True
	
	# Checks if VLAN name exists on Switch
	def CkeckNameAvailability(self):
		# CLI output contains a lot of errors, wich are handeled but not suppressed
		try:
			tmp = exsh.clicmd("show vlan %s " % self.__name, capture=True)
			if (tmp.find("VLAN Interface with name") != -1):
				self.__nameA=False
				Vlan.existingNames+=1
			else:
				self.__nameA=True
		# show vlan <Vlan-Name> creates an error if no VLAN with given Name is existent Error is handled by setting name availability to True
		except:
			self.__nameA=True
	
	# Checks if the vlan (Name and ID) on the switch match (Name and ID) from the csv
	def CheckMatch(self):
		if ((not self.__nameA) & (not self.__vidA)):
			tmp = exsh.clicmd("show vlan %s" % self.__vid, capture=True)
			if (tmp.lower().find(("VLAN Interface with name %s " % self.__name).lower()) != -1):
				self.__match = True
				Vlan.matchingVLANs += 1
		elif (self.__nameA & self.__vidA):
				self.__creatable = True
				Vlan.creatableVLANs += 1
		Vlan.checkedVLANs += 1
			
	# Prints the results of previous checks
	def PritResult(self):
		if (self.__match):
			print("VLAN %s(%s) EXISTS. Name matches ID" % (self.__name, self.__vid))
		elif (self.__creatable):
			print("VLAN %s(%s) is CREATABLE" % (self.__name, self.__vid))
		elif (self.__vidA):
			print("VLAN %s(%s) is CREATABLE with another Name" % (self.__name, self.__vid))
		elif (self.__nameA): 
			print("VLAN %s(%s) EXISTS with another Name" % (self.__name, self.__vid))
		
# Class to read csv and return as nested list
class CsvReader:
	
	# Constructor, path is in the default directory on XOS switches, delimiter is the default delimiter from microsoft excel
	def __init__(self, path="/usr/local/cfg/vlan_list.csv", delimiter=";"):
		self.__path = path
		self.__delimiter = delimiter
		
	# Destructor
	def __del__(self):
		pass
		
	# Method opens file, removes whitespaces at the end and beginning of each value and returns a nested list
	def ReadValues(self):
		file=open(self.__path)
		line = " "
		wholeSet = list()
		while True:
			tupel = list()
			line = file.readline()
			if not line: break
			i = line.find(self.__delimiter)
			while (i != -1):
				tupel.append(line[:i].strip())
				line = line[i+1:]
				i = line.find(self.__delimiter)
			line=line.strip()
			tupel.append(line)
			wholeSet.append(tupel)
		return wholeSet

def main():
	
	csvr = CsvReader()
	
	values = csvr.ReadValues()
	vlans = list()
	
	for v in values:
		vlans.append(Vlan(v[0], v[1]))
		
	for v in vlans:
		v.CheckVidAvailablitiy()
		v.CkeckNameAvailability()
		v.CheckMatch()
	
	for v in vlans:
		v.PritResult()
	
	print("Check finished. %s VLANs checked. %s VLANs can be created %s VLAN Names match their ID." % (Vlan.checkedVLANs, Vlan.creatableVLANs, Vlan.matchingVLANs))	
	
main()
	