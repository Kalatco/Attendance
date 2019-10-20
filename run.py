from tkinter import *
from Attendance import Attendance

# File: run.py
#
# About: This file contains a working GUI, but code clean up is still in process.
#
gui = None

SUBMIT_BUTTON_TEXT = "Submit grades"
COLORS = {
	-1: "grey",
	0: "red",
	1: "orange",
	2: "green",

}
myStudents = []
myUnsortedStudents = []
myTables = []
grader = Attendance()
print("Program has loaded.")
grader.updateJson()

className = grader.getClassName()
currentSection = grader.getSections()[-1]

allSections = grader.getSections()

studentsDict = grader.getDefinedGrades(currentSection)
tableData = grader.getTablesDictionary()

unsortedStudents = grader.getUnsortedStudents()



#----------------------------------------------------------------------

# Updates the attendance number for the current student.


def updateScore11(std, score):
	pass


def submitGrades11(event):
	grader.submitScores(currentSection)
	submit.config(fg="green3")

def changeSection11():
	tempSec = []
	popup = Tk()
	popup.wm_title("Change Section")
	for sec in sorted(allSections):
		temp = Label(popup, text=sec, fg="black", font=("arial",16))
		temp.config(height=2)
		temp.pack(fill=X)
		temp.bind("<Button 1>", setSection)
		tempSec.append(temp)

	popFrame = Frame(popup, width=200, height=len(allSections)*2)
	popFrame.pack()
	popFrame.mainloop()


def setSection11(event):
	name = event.widget.cget("text")

	currentSection = name
	studentsDict = grader.getDefinedGrades(name)

	gui = sectionViewer(className, name)
	gui.printBody()

#--------------------------------------------------------------------------------------------


#
# About: This class creates a new Tkinter window and displays the selected section.
#
class sectionViewer:

	root = None
	myStudents = []
	myUnsortedStudents = []
	myTables = []
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
			self.myTables.append(tempTable)
			for std in sorted(tableData[table]):
				temp = Label(self.root, text=std, bg = COLORS[self.studentScoreDictionary[std]], fg="black", font=("arial",16))
				temp.config(height=2)
				temp.pack(fill=X)
				temp.bind("<Button 1>", self.updateAttendance)
				self.myStudents.append(temp)

		# print students not in a table
		if(len(unsortedStudents) > 0):
			unsorted = Label(self.root, text="Remaining Students", bg="black", fg="white", font=("arial",16))
			unsorted.config(height=2)
			unsorted.pack(fill=X)
			for std in sorted(unsortedStudents):
				temp = Label(self.root, text=std, bg = COLORS[self.studentScoreDictionary[std]], fg="black", font=("arial",16))
				temp.config(height=2)
				temp.pack(fill=X)
				temp.bind("<Button 1>", self.updateAttendance)
				self.myUnsortedStudents.append(temp)

		# footer
		self.submit = Label(self.root, text=SUBMIT_BUTTON_TEXT, font=("arial", 16,"bold"), height=2, fg="green3")
		self.submit.pack(fill=X)
		self.submit.bind("<Button 1>", self.submitGrades)

		self.frame = Frame(self.root, width=300, height=len(self.studentScoreDictionary)*2)
		self.frame.pack()
		self.frame.mainloop()

	def changeSection(self, event):
		self.root.destroy()
		ChangeSection()

	def submitGrades(self, event):
		grader.submitScores(self.sectionLabel)
		self.submit.config(fg="green3")

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

		self.updateScore(std, score)
		event.widget.config(background=COLORS[self.studentScoreDictionary[std]])
		self.submit.config(fg="red")

	def updateScore(self, std, score):
		grader.addScore(self.sectionLabel, std, score)

# End of sectionViewer class

#----------------------------------------------------------------------------
class ChangeSection:

	root = None
	tempSec = []

	def __init__(self):
		
		self.root = Tk()
		self.root.wm_title("Change Section")
		for sec in sorted(allSections):
			temp = Label(self.root, text=sec, fg="black", font=("arial",16))
			temp.config(height=2)
			temp.pack(fill=X)
			temp.bind("<Button 1>", self.setSection)
			self.tempSec.append(temp)

		self.popFrame = Frame(self.root, width=200, height=len(allSections)*2)
		self.popFrame.pack()
		self.popFrame.mainloop()

	def setSection(self, event):
		name = event.widget.cget("text")
		currentSection = name
		studentsDict = grader.getDefinedGrades(name)

		self.root.destroy()
		gui = sectionViewer(className, name)
		gui.printBody()

# End of ChangeSection Class.

#----------------------------------------------------------------------------

gui = sectionViewer(className, currentSection)
gui.printBody()

