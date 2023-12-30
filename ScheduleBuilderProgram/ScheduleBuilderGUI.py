import PySimpleGUI as sg
import numpy as np
import ScheduleBuilder as schb
import operator
import GraphWeek as gw

"""This is the file to execute for the program"""

print("This window will show your results after you submit:")

def create_row(row_counter):
	""" Create a row for class input """
	row = [
		sg.pin(
			sg.Col([
				[
					sg.Button('X', border_width = 0,
					button_color=(sg.theme_text_color(), sg.theme_background_color()),
					key=('-DEL-', row_counter)),
					
					sg.Text('Class:'),
					sg.Input(size=(20,1), key=('-CLASS-', row_counter, -1)),
					
					sg.Text('Start Time:'),
					sg.Input(size=(8, 1), key=('-START-', row_counter, -1)),
					sg.Listbox(['AM','PM'],size=(3, 2), key=('-AMPM1-', row_counter, -1)),
					
					sg.Text('End Time:'),
					sg.Input(size=(8, 1), key=('-END-', row_counter, -1)),
					sg.Listbox(['AM','PM'],size=(3, 2), key=('-AMPM2-', row_counter, -1)),
					
					sg.Listbox(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
					key=('-DAYS-', row_counter, -1), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size = (10,5)),
					
					sg.Button('Add Alt', key=('-ADD_ALT-', row_counter))
				]
			],
			key=('-ROW-', row_counter)
			)
		)
	]
	return row
	
def create_alt_row(row_counter, alt_counter):
	"""Create a sub row in a class for alternate times"""
	alt_row = [
		sg.pin(
			sg.Col([
				[
					sg.Text("-----------------------------------------------"),
					
					sg.Button('X', border_width = 1,
					button_color=(sg.theme_text_color(), sg.theme_background_color()),
					key=('-ALT_DEL-', row_counter, alt_counter)),
					
					sg.Text('Start Time:'),
					sg.Input(size=(8, 1), key=('-START-', row_counter, alt_counter)),
					sg.Listbox(['AM','PM'],size=(3, 1), key=('-AMPM1-', row_counter, alt_counter)),
					
					sg.Text('End Time:'),
					sg.Input(size=(8, 1), key=('-END-', row_counter, alt_counter)),
					sg.Listbox(['AM','PM'],size=(3, 1), key=('-AMPM2-', row_counter, alt_counter)),
					
					sg.Listbox(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
					key=('-DAYS-', row_counter, alt_counter), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
					size = (10,5))
					
				]
			],
			key=('-ALT_ROW-', row_counter, alt_counter)
			)
		)
	]
	return alt_row
	
#Initializing Tabs for the TabGroup
Tab1 = sg.Tab("Class 1", [create_row(1)], visible=True, key=("-TAB-", 1))
Tab2 = sg.Tab("Class 2", [create_row(2)], visible=False, key=("-TAB-", 2))
Tab3 = sg.Tab("Class 3", [create_row(3)], visible=False, key=("-TAB-", 3))
Tab4 = sg.Tab("Class 4", [create_row(4)], visible=False, key=("-TAB-", 4))
Tab5 = sg.Tab("Class 5", [create_row(5)], visible=False, key=("-TAB-", 5))
Tab6 = sg.Tab("Class 6", [create_row(6)], visible=False, key=("-TAB-", 6))
Tab7 = sg.Tab("Class 7", [create_row(7)], visible=False, key=("-TAB-", 7))
Tab8 = sg.Tab("Class 8", [create_row(8)], visible=False, key=("-TAB-", 8))
Tab9 = sg.Tab("Class 9", [create_row(9)], visible=False, key=("-TAB-", 9))
Tab10 = sg.Tab("Class 10", [create_row(10)], visible=False, key=("-TAB-", 10))
	
layout = [
	[sg.Text('Add classes and times')],
	[sg.TabGroup([[Tab1], [Tab2], [Tab3], [Tab4], [Tab5], [Tab6], [Tab7], [Tab8], [Tab9], [Tab10]], key=('-TAB_GROUP-', 1, -1))], 
	[sg.Text("Exit", enable_events=True, key='-EXIT-'),
	sg.Text("+", enable_events=True, key='-ADD_ROW-'), sg.Button('Submit', key='-SUBMIT_BUTTON-')]
	]
	
visPanel = [True, False, False, False, False, False, False, False, False, False] #Keeps track of which tabs are visible

window = sg.Window('Schedule Builder', layout, use_default_focus=False, font='15')

alt_counter = 0
alt_tracker = [[], [], [], [], [], [], [], [], [], []] #keep track of 3rd value in tuple keys used for the alt rows

interList = [] #Defined both outside and inside process_results for handling
def process_results(): #Read the values from user input and display combinations of classes
	count = 1 #tracks the class number (key[1]) in the for loop below
	numAlts = 0 #track index to add alts in clean_values, until max value defined in alt_tracker_size
	alt_tracker_size = [] #track the number of alts each class has
	for arrayAlts in alt_tracker:
		alt_tracker_size.append(len(arrayAlts))

	clean_values = {} # clean_values = {'class_name': [ [times for alt 1], [times for alt 2]] ...

	#values has the first row of each class first, then the alts at the end
	
	for key, value in values.items(): #creates clean_values, a dict with class name as key and everything else in a list
		if visPanel[count-1] and key[0] == '-CLASS-':
			clean_values[value] = [[]] #2D array, list of each possible alternate information
		elif visPanel[count-1] and key[1] == count and key[0] != '-TAB_GROUP-': #primary times for the class added to first list
			clean_values[values[('-CLASS-', count, -1)]][0].append(value)
			if key[0] == '-DAYS-': #indicates that loop has reached the next class
				count += 1
		elif value and key[0] == '-START-':	#loop reaches this point when alt times begin in values
			numAlts += 1
			altTraverse = 0 #used to track each element of an alt being added
			count = -1 #ensures that the code above does not run
			clean_values[values[('-CLASS-', key[1], -1)]].append([])
			clean_values[values[('-CLASS-', key[1], -1)]][numAlts].append(value)
			
		elif numAlts > 0: #statement prevents index error in line below
			if value and key[2] == alt_tracker[key[1]-1][numAlts - 1]:
				clean_values[values[('-CLASS-', key[1], -1)]][numAlts].append(value)
			altTraverse += 1
			if numAlts >= alt_tracker_size[key[1]-1] and altTraverse == 4: #reset numAlts for the next class, altTraverse = 4 corresponds to 'Day' field
				numAlts = 0
		
		elif key[0] == '-DAYS-' and key[1] != 10: #Add value to count for next class if second elif-if statement does not run
			count += 1
		

	for className, options in clean_values.items(): #insert class name as the first element of each time option (for formatting purposes)s
		for option in options:
			option.insert(0, className)


	classNames = [] #Store class names, easier to handle the clean_values dictionary in a loop
	for className in clean_values.keys():
		classNames.append(className)
		
	global interList
	interList = []

	for i in range(len(clean_values[classNames[0]])): #Using first class as initial values in interList
		interList.append([])
		interList[-1].append(clean_values[classNames[0]][i])
	for count in range(1, len(clean_values)): #Building all combinations off of the first class
		interList = schb.combo(interList, clean_values[classNames[count]])
		
	numCombos = 0
	for option in interList: #formatting for display
		numCombos += 1
		print("Combination " + str(numCombos) + ":")
		for classOption in option:
			print(classOption[0] + " | " + classOption[1] + " " + classOption[2][0]
					+ " - " + classOption[3] + " " + classOption[4][0] + ", ", end = "")
			print(classOption[5])
		print("-----------------")

	print("You have " + str(len(interList)) + " possible combinations!")
	print("-----------------")

	for conflictPair in schb.conflict_list:
		print("This pair is in conflict: ")
		for aClass in conflictPair:
			print(aClass)
		print("")

while True:
	event, values = window.read() #event is a button clicked, values is a dictionary
	
	if event == sg.WIN_CLOSED or event == '-EXIT-':
		break
	if event == '-ADD_ROW-': #Finds a not visible column and makes it visible
		for row in range(0, 10):
			if not visPanel[row]:
				visPanel[row] = True
				window[('-TAB-', row + 1)].Update(visible=True)
				break		

	elif event[0] == '-DEL-': #event here is the key to the delete button, a tuple
		window[('-CLASS-', event[1], -1)].update('')
		window[('-START-', event[1], -1)].update('')
		window[('-AMPM1-', event[1], -1)].update(set_to_index=[])
		window[('-END-', event[1], -1)].update('')
		window[('-AMPM2-', event[1], -1)].update(set_to_index=[]) #Reset input boxes to empty
		window[('-TAB-', event[1])].Update(visible=False)
		visPanel[event[1] - 1] = False
		
		for alt_number in alt_tracker[event[1]-1]: #clear existing associated alt rows as well
			window[('-START-', event[1], alt_number)].update('')
			window[('-AMPM1-', event[1], alt_number)].update(set_to_index=[])
			window[('-END-', event[1], alt_number)].update('')
			window[('-AMPM2-', event[1], alt_number)].update(set_to_index=[])
			window[('-ALT_ROW-', event[1], alt_number)].update(visible=False)	
		
	elif event[0] == '-ADD_ALT-':
		alt_counter += 1
		window.extend_layout(window[('-TAB-', event[1])], [create_alt_row(event[1], alt_counter)])		
		alt_tracker[event[1]-1].append(alt_counter) #3rd value in key added to tracker
		
		
		
	elif event[0] == '-ALT_DEL-':
		window[('-START-', event[1], event[2])].update('')
		window[('-AMPM1-', event[1], event[2])].update(set_to_index=[])
		window[('-END-', event[1], event[2])].update('')
		window[('-AMPM2-', event[1], event[2])].update(set_to_index=[])
		alt_tracker[event[1]-1].remove(event[2]) #value in alt tracker removed
		window[('-ALT_ROW-', event[1], event[2])].update(visible=False)
	if event == '-SUBMIT_BUTTON-':
		schb.conflict_list = []
		flag = False
		print("--------------------------------------------------------------------------")
		for tabCount in range(0, 10): #Catches any unfilled fields
			if visPanel[tabCount]:
				if not values[('-CLASS-', tabCount + 1, -1)]:
					print("Please fill out: Classname " + str(tabCount + 1))
					flag = True
				if not values[('-START-', tabCount + 1, -1)]:
					print("Please fill out: Start time for class " + str(tabCount + 1))
					flag = True
				elif len(values[('-START-', tabCount + 1, -1)]) < 4 or len(values[('-START-', tabCount + 1, -1)]) > 5:
					print("Check your times for class " + str(tabCount + 1))
					flag = True
				if not values[('-AMPM1-', tabCount + 1, -1)]:
					print("Please fill out: AM or PM for start of class " + str(tabCount + 1))
					flag = True
				if not values[('-END-', tabCount + 1, -1)]:
					print("Please fill out: End time for class " + str(tabCount + 1))
					flag = True
				elif len(values[('-END-', tabCount + 1, -1)]) < 4 or len(values[('-END-', tabCount + 1, -1)]) > 5:
					print("Check your times for class " + str(tabCount + 1))
					flag = True
				if not values[('-AMPM2-', tabCount + 1, -1)]:
					print("Please fill out: AM or PM for end of class " + str(tabCount + 1))
					flag = True
				if not values[('-DAYS-', tabCount + 1, -1)]:
					print("Please fill out: Days for class " + str(tabCount + 1))
					flag = True
				
				for alt in alt_tracker[tabCount]:
					if not values[('-START-', tabCount + 1, alt)]:
						print("Please fill out: Start time for alt of class " + str(tabCount + 1))
						flag = True
					elif len(values[('-START-', tabCount + 1, alt)]) < 4 or len(values[('-START-', tabCount + 1, alt)]) > 5:
						print("Check your times for class " + str(tabCount + 1))
						flag = True
					if not values[('-AMPM1-', tabCount + 1, alt)]:
						print("Please fill out: AM or PM for start of alt of class " + str(tabCount + 1))
						flag = True
					if not values[('-END-', tabCount + 1, alt)]:
						print("Please fill out: End time for alt of class " + str(tabCount + 1))
						flag = True
					elif len(values[('-END-', tabCount + 1, alt)]) < 4 or len(values[('-END-', tabCount + 1, alt)]) > 5:
						print("Check your times for class " + str(tabCount + 1))
						flag = True
					if not values[('-AMPM2-', tabCount + 1, alt)]:
						print("Please fill out: AM or PM for end of alt of class " + str(tabCount + 1))
						flag = True
					if not values[('-DAYS-', tabCount + 1, alt)]:
						print("Please fill out: Days for alt of class " + str(tabCount + 1))
						flag = True
					
		if not flag:
			process_results()
			window.disappear()
	
			interList_sorted = interList #Each option sorted by start time of each class
			for option in interList_sorted:
				for aClass in option:
					aClass.append(int(schb.convertAMPM_24(aClass[1], aClass[2][0]))) #adds start time in 24h format for sorting
			for option in interList_sorted:
				option = option.sort(key=operator.itemgetter(6)) #sort by start time as the key
			
			x = 0
			while x != "-1":
				print("Enter a combination number to view in further detail, 0 to re-enter classes, or -1 to quit")
				x = input()
				if x == "0":
					window.reappear()
					break
				elif x != "-1":
					try:
						interList_sorted[int(x)-1]
						print("***********************")
						print("Monday:")
						for aClass in interList_sorted[int(x)-1]:
							if "Monday" in aClass[5]:
								print(aClass[0] + " | " + aClass[1] + " " + aClass[2][0] + " - " + aClass[3] + " " + aClass[4][0])
						print("---")
						print("Tuesday:")
						for aClass in interList_sorted[int(x)-1]:
							if "Tuesday" in aClass[5]:
								print(aClass[0] + " | " + aClass[1] + " " + aClass[2][0] + " - " + aClass[3] + " " + aClass[4][0])
						print("---")
						print("Wednesday:")
						for aClass in interList_sorted[int(x)-1]:
							if "Wednesday" in aClass[5]:
								print(aClass[0] + " | " + aClass[1] + " " + aClass[2][0] + " - " + aClass[3] + " " + aClass[4][0])
						print("---")
						print("Thursday:")
						for aClass in interList_sorted[int(x)-1]:
							if "Thursday" in aClass[5]:
								print(aClass[0] + " | " + aClass[1] + " " + aClass[2][0] + " - " + aClass[3] + " " + aClass[4][0])	
						print("---")
						print("Friday:")
						for aClass in interList_sorted[int(x)-1]:
							if "Friday" in aClass[5]:
								print(aClass[0] + " | " + aClass[1] + " " + aClass[2][0] + " - " + aClass[3] + " " + aClass[4][0])	
						print("***********************")
						gw.make_visWindow(interList_sorted[int(x)-1])
					except IndexError:
						print("Not a valid combination")
		
					
				print("---------------")
	

window.close()

