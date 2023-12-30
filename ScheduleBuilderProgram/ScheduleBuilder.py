import numpy as np
import PySimpleGUI as psg

"""Support program creating several functions for ScheduleBuilderGUI"""

def convertAMPM_24(time, AMPM): 
	"""Takes a string (XX:XX and AM/PM) and converts to 24h format (xxxx) as a string"""
	if time[1] == ":": #add a 0 to hours starting with one digit (eg. 1:35)
		time = "0" + time
	if AMPM == "AM":
		hour = time[:2]
		minute = time[-2:]
		time_24 = hour + minute
	elif AMPM == "PM" and time[:2] != "12":
		hour = str(int(time[:2])+12)
		minute = time[-2:]
		time_24 = hour + minute	
	else: time_24 = time[:2] + time[-2:] #Special case for 12 PM 
	if time_24[0] == "0": #remove the 0 if added above
		time_24 = time_24[1:] 
	return time_24


def check_conflict_time(start1, end1, start2, end2): 
	"""check time conflict between two time intervals in 24h format"""
	
	int_start1 = int(start1)
	int_end1 = int(end1)
	int_start2 = int(start2)
	int_end2 = int(end2)
	
	if int_end1 >= int_start2 and int_end1 <= int_end2: #First check (no buffer)
		return True
	elif int_start1 <= int_end2 and int_start1 >= int_start2:
		return True
	
	if int_start1 % 100 < 15: #These next 2 if-else statements add a 15 minute buffer to the first time interval (will not change display value)
		int_start1 -= 55
	else: int_start1 -= 15
	
	if int_start2 % 100 < 15:
		int_start2 -= 55
	else: int_start2 -= 15

	
	if int_end1 > int_start2 and int_end1 < int_end2: #Second check (with buffer)
		return True
	elif int_start1 < int_end2 and int_start1 > int_start2:
		return True
	return False

def check_conflict_day(days1, days2): #input lists containing days for the class
	"""Check conflict in a day"""
	for day in days1:
		if day in days2:
			return True
	return False	

conflict_list = [] #Tracks what class options have a time conflict

def combo(list1, aClass): #list1 must be 3d array, aClass must be a 2d array
	"""list1 is a list of different combinations of classes
		aClass is for one class with one or more alt times"""
	comboList = []
	for option in list1: #option is one possible combination of class times	
		for anAlt in aClass: #anAlt is one possibile time for a single class
			flag = False
			for oneClass in option: #oneClass is a class in the option combination
				oneClassStart = convertAMPM_24(oneClass[1], oneClass[2][0])
				oneClassEnd = convertAMPM_24(oneClass[3], oneClass[4][0])
	
				anAltStart = convertAMPM_24(anAlt[1], anAlt[2][0])
				anAltEnd = convertAMPM_24(anAlt[3], anAlt[4][0])
				
				if check_conflict_time(oneClassStart, oneClassEnd, anAltStart, anAltEnd) and check_conflict_day(oneClass[5], anAlt[5]):
					flag = True
					conflict_list.append([])
					conflict_list[-1].append(oneClass)
					conflict_list[-1].append(anAlt)
			if not flag:
				comboList.append([])
				for element in option: #append each class time in option
					comboList[-1].append(element)
				comboList[-1].append(anAlt)	
	return comboList #comboList is in the same format as list1, a list of options


	



