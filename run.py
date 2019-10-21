# File: run.py
# Author: Andrew Raftovich, Fall 2019
# Contact: AndrewRaftovich@gmail.com
#
# About: This program allows users to easily modify student section participation scores 
#		 without accessing the Google Sheets document using a GUI.
#
from tkinter import *
from Attendance import Attendance

# Global variables.
SUBMIT_BUTTON_TEXT = "Submit grades"
UNSORTED_STUDENTS_TEXT = "Unsorted students"
CHANGE_CURRENT_SECTION_TITLE = "Change Section"
COLORS = {
	-1: "grey",
	0: "red",
	1: "orange",
	2: "green",
}

# The main page GUI that gets changed with each section change.
gui = None

# Creates the Attendance Instance and alerts user that the program is loaded once this class loads.
grader = Attendance()
print("Program has loaded.")

# Gets the name of the class this program is being used for.
className = grader.getClassName()

# List of all the sections from the Sheets file.
allSections = grader.getSections()

# The current section that will be displayed.
currentSection = allSections[-1]

# List of students
studentsDict = grader.getDefinedGrades(currentSection)

# List of table numbers and students in those tables
tableData = grader.getTablesDictionary()

# List of students who are not in a table.
unsortedStudents = grader.getUnsortedStudents()

#--------------------------------------------------------------------------------------------
# About: This class creates a new Tkinter window and displays the selected section.
#
class SectionViewer:

	root = None
	header = None
	submit = None
	frame = None
	sectionLabel = None

	def __init__(self, className, sectionName):
		self.sectionLabel = sectionName
		self.studentScoreDictionary = grader.getDefinedGrades(self.sectionLabel)
		self.root = Tk()
		self.root.title(className)

		# converts the strings of data to integers.
		for x in self.studentScoreDictionary:
			if self.studentScoreDictionary[x] == '':
				self.studentScoreDictionary[x] = -1
			else:
				self.studentScoreDictionary[x] = int(self.studentScoreDictionary[x])

	# Prints the main page of the applications
	def printBody(self):
		# header
		self.header = Label(self.root, text=className+": "+self.sectionLabel, font=("arial", 16, "bold"), height=2)
		self.header.bind("<Button 1>", self.changeSection) #changeSection() is a global method
		self.header.pack(fill=X)

		# print tables
		for table in sorted(tableData.keys()):
			tempTable = Label(self.root, text=table, bg="black", fg="white", font=("arial",16))
			tempTable.config(height=2)
			tempTable.pack(fill=X)

			for std in sorted(tableData[table]):
				temp = Label(self.root, text=std, bg = COLORS[self.studentScoreDictionary[std]], fg="black", font=("arial",16))
				temp.config(height=2)
				temp.pack(fill=X)
				temp.bind("<Button 1>", self.updateAttendance)

		# print students not in a table
		if(len(unsortedStudents) > 0):
			unsorted = Label(self.root, text=UNSORTED_STUDENTS_TEXT, bg="black", fg="white", font=("arial",16))
			unsorted.config(height=2)
			unsorted.pack(fill=X)
			for std in sorted(unsortedStudents):
				temp = Label(self.root, text=std, bg = COLORS[self.studentScoreDictionary[std]], fg="black", font=("arial",16))
				temp.config(height=2)
				temp.pack(fill=X)
				temp.bind("<Button 1>", self.updateAttendance)

		# footer
		self.submit = Label(self.root, text=SUBMIT_BUTTON_TEXT, font=("arial", 16,"bold"), height=2, fg="green3")
		self.submit.pack(fill=X)
		self.submit.bind("<Button 1>", self.submitGrades)

		self.frame = Frame(self.root, width=300, height=len(self.studentScoreDictionary)*2)
		self.frame.pack()
		self.frame.mainloop()

	# Prompts user to change section when clicked.
	def changeSection(self, event):
		self.root.destroy()
		ChangeSection()

	# submits the scores to the Google Sheets
	def submitGrades(self, event):
		grader.submitScores(self.sectionLabel)
		self.submit.config(fg="green3")

	# Updates the numerical value of a student.
	def updateAttendance(self, event):
		std = event.widget.cget("text")

		if(self.studentScoreDictionary[std] == -1):
			self.studentScoreDictionary[std] = 2
	
		elif (self.studentScoreDictionary[std] == 2):
			self.studentScoreDictionary[std] = 1

		elif (self.studentScoreDictionary[std] == 1):
			self.studentScoreDictionary[std] = 0

		else:
			self.studentScoreDictionary[std] = -1

		score = self.studentScoreDictionary[std]
		if(score == -1):
			score = ''

		grader.addScore(self.sectionLabel, std, score)
		event.widget.config(background=COLORS[self.studentScoreDictionary[std]])
		self.submit.config(fg="red")

# End of SectionViewer class
#---------------------------------------------------------------------------------------
# About: This class creates a new page to prompt the user to change the current section.
#
class ChangeSection:
	root = None

	def __init__(self):
		self.root = Tk()
		self.root.wm_title(CHANGE_CURRENT_SECTION_TITLE)
		for sec in sorted(allSections):
			temp = Label(self.root, text=sec, fg="black", font=("arial",16))
			temp.config(height=2)
			temp.pack(fill=X)
			temp.bind("<Button 1>", self.setSection)

		self.popFrame = Frame(self.root, width=200, height=len(allSections)*2)
		self.popFrame.pack()
		self.popFrame.mainloop()

	# Changes the main GUI to the current section.
	def setSection(self, event):
		name = event.widget.cget("text")
		currentSection = name
		studentsDict = grader.getDefinedGrades(name)

		self.root.destroy()
		gui = SectionViewer(className, name)
		gui.printBody()

# End of ChangeSection Class.
#----------------------------------------------------------------------------

# Runs the startup code.
gui = SectionViewer(className, currentSection)
gui.printBody()

