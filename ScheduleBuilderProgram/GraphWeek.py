import PySimpleGUI as sg
import ScheduleBuilder as schb

"""Support program creating a graphic display for ScheduleBuilderGUI"""

numWindows = 0 #used in keys of elements, avoids error for using the same layout

def fill_time(start_time, end_time , day, visWindow): #times in 24h hormat, fill a timeslot in black
	bot_right = 120
	if day == "Tuesday":
		bot_right = 240
	elif day == "Wednesday":
		bot_right = 360
	elif day == "Thursday":
		bot_right = 480
	elif day == "Friday":
		bot_right = 600
	start_hour = start_time // 100
	end_hour = end_time // 100
	start_minute = start_time % 100
	end_minute = end_time % 100
	
	visWindow[('-GRAPH-', numWindows)].draw_rectangle((bot_right - 120, 810 - (58 * (start_hour - 8)) - (14.5 * (start_minute / 15))), 
										(bot_right, 810 - (58 * (end_hour - 8)) - (14.5 * (end_minute / 15))), fill_color = 'black')

def create_col_layout(numWindows):
	font = ('Arial', 13)
	col_layout = [ [sg.Text("8:00 AM", font = font, key = ('-TEXT-', 1, numWindows))],
				   [sg.Text("8:30 AM", font = font, key = ('-TEXT-', 2, numWindows))],
				   [sg.Text("9:00 AM", font = font, key = ('-TEXT-', 3, numWindows))],
				   [sg.Text("9:30 AM", font = font, key = ('-TEXT-', 4, numWindows))],
				   [sg.Text("10:00 AM", font = font, key = ('-TEXT-', 5, numWindows))],
				   [sg.Text("10:30 AM", font = font, key = ('-TEXT-', 6, numWindows))],
				   [sg.Text("11:00 AM", font = font, key = ('-TEXT-', 7, numWindows))],
				   [sg.Text("11:30 AM", font = font, key = ('-TEXT-', 8, numWindows))],
				   [sg.Text("12:00 PM", font = font, key = ('-TEXT-', 9, numWindows))],
				   [sg.Text("12:30 PM", font = font, key = ('-TEXT-', 10, numWindows))],
				   [sg.Text("1:00 PM", font = font, key = ('-TEXT-', 11, numWindows))],
				   [sg.Text("1:30 PM", font = font, key = ('-TEXT-', 12, numWindows))],
				   [sg.Text("2:00 PM", font = font, key = ('-TEXT-', 13, numWindows))],
				   [sg.Text("2:30 PM", font = font, key = ('-TEXT-', 14, numWindows))],
				   [sg.Text("3:00 PM", font = font, key = ('-TEXT-', 15, numWindows))],
				   [sg.Text("3:30 PM", font = font, key = ('-TEXT-', 16, numWindows))],
				   [sg.Text("4:00 PM", font = font, key = ('-TEXT-', 17, numWindows))],
				   [sg.Text("4:30 PM", font = font, key = ('-TEXT-', 18, numWindows))],
				   [sg.Text("5:00 PM", font = font, key = ('-TEXT-', 19, numWindows))],
				   [sg.Text("5:30 PM", font = font, key = ('-TEXT-', 20, numWindows))],
				   [sg.Text("6:00 PM", font = font, key = ('-TEXT-', 21, numWindows))],
				   [sg.Text("6:30 PM", font = font, key = ('-TEXT-', 22, numWindows))],
				   [sg.Text("7:00 PM", font = font, key = ('-TEXT-', 23, numWindows))],
				   [sg.Text("7:30 PM", font = font, key = ('-TEXT-', 24, numWindows))],
				   [sg.Text("8:00 PM", font = font, key = ('-TEXT-', 25, numWindows))],
				   [sg.Text("8:30 PM", font = font, key = ('-TEXT-', 26, numWindows))],
				   [sg.Text("9:00 PM", font = font, key = ('-TEXT-', 27, numWindows))],
				   [sg.Text("9:30 PM", font = font, key = ('-TEXT-', 28, numWindows))],
				   [sg.Text("10:00 PM", font = font, key = ('-TEXT-', 29, numWindows))]
				 ]
	return col_layout

def create_layout(numWindows):
	layout = [
				[sg.Text("                               Monday", key = ('-MONDAY-', numWindows)),
				 sg.Text("              Tuesday", key = ('-TUESDAY-', numWindows)),
				 sg.Text("             Wednesday", key = ('-WEDNESDAY-', numWindows)),
				 sg.Text("            Thursday", key = ('-THURSDAY-', numWindows)),
				 sg.Text("              Friday", key = ('-FRIDAY-', numWindows))],
				[sg.Column(create_col_layout(numWindows), element_justification = 'right', key = ('-COLUMN-', numWindows)), sg.Graph(canvas_size = (600, 810), graph_bottom_left = (0, 0), 
				graph_top_right = (600, 810), background_color = 'lightblue', key = ('-GRAPH-', numWindows))]
			 ]
	return layout

def make_visWindow(optionList): 
	global numWindows
	visWindow = sg.Window("Schedule", create_layout(numWindows), finalize = True)
			
	for aClass in optionList:
		startTime = int(schb.convertAMPM_24(aClass[1], aClass[2][0]))
		endTime = int(schb.convertAMPM_24(aClass[3], aClass[4][0]))
		days = aClass[5]
		for day in days:
			fill_time(startTime, endTime, day, visWindow)
	
	for i in range(0, 5): #creates a grid
		for j in range(0, 28):
			visWindow[('-GRAPH-', numWindows)].draw_rectangle((120*i, 810 - (29*j)), (120 + (120*i), 810 - (29*(j+1))), line_color = 'gray')
	
	while True:
		event, values = visWindow.read() 
		if event == sg.WIN_CLOSED:
			break
	
	visWindow.close()
	numWindows += 1
	
	






