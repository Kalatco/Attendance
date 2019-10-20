from tkinter import *
from Attendance import Attendance

# File: run.py
#
# About: This file contains a basic working GUI for the project, this code is
#		 still far from completion.
#

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

# converts the strings of data to integers.
for x in studentsDict:
	if studentsDict[x] == '':
		studentsDict[x] = -1
	else:
		studentsDict[x] = int(studentsDict[x])

#----------------------------------------------------------------------

# Updates the attendance number for the current student.
def updateAttendance(event):
	std = event.widget.cget("text")

	if(studentsDict[std] == -1):
		studentsDict[std] = 2
	
	elif (studentsDict[std] == 2):
		studentsDict[std] = 1

	elif (studentsDict[std] == 1):
		studentsDict[std] = 0

	else:
		studentsDict[std] = -1

	score = studentsDict[std]
	if(score == -1):
		score = ''

	updateScore(std, score)
	event.widget.config(background=COLORS[studentsDict[std]])
	submit.config(fg="red")

def updateScore(std, score):
	grader.addScore(currentSection, std, score)


def submitGrades(event):
	grader.submitScores(currentSection)
	submit.config(fg="green3")

def changeSection(event):
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


def setSection(event):
	name = event.widget.cget("text")
	currentSection = name
	studentsDict = grader.getDefinedGrades(name)
	print("oof")

#--------------------------------------------------------------------------------------------

root = Tk()
root.title("Attendance Program")
#root.resizable(False, False)

# header
header = Label(root, text=className+": "+currentSection, font=("arial", 16, "bold"), height=2)
header.bind("<Button 1>", changeSection)
header.pack(fill=X)

# body
#for std in sorted(students.keys()):
#	temp = Label(root, text=students[std], bg = COLORS[students[std]], fg="black", font=("arial",16))
#	temp.config(height=2)
#	temp.pack(fill=X)
#	temp.bind("<Button 1>", updateAttendance)
#	myButtons.append(temp)

# print students who are in a table
for table in sorted(tableData.keys()):
	tempTable = Label(root, text=table, bg="black", fg="white", font=("arial",16))
	tempTable.config(height=2)
	tempTable.pack(fill=X)
	myTables.append(tempTable)
	for std in sorted(tableData[table]):
		temp = Label(root, text=std, bg = COLORS[studentsDict[std]], fg="black", font=("arial",16))
		temp.config(height=2)
		temp.pack(fill=X)
		temp.bind("<Button 1>", updateAttendance)
		myStudents.append(temp)

# print students not in a table
if(len(unsortedStudents) > 0):
	unsorted = Label(root, text="Remaining Students", bg="black", fg="white", font=("arial",16))
	unsorted.config(height=2)
	unsorted.pack(fill=X)
	for std in sorted(unsortedStudents):
		temp = Label(root, text=std, bg = COLORS[studentsDict[std]], fg="black", font=("arial",16))
		temp.config(height=2)
		temp.pack(fill=X)
		temp.bind("<Button 1>", updateAttendance)
		myUnsortedStudents.append(temp)


# footer
submit = Label(root, text=SUBMIT_BUTTON_TEXT, font=("arial", 16,"bold"), height=2, fg="green3")
submit.pack(fill=X)
submit.bind("<Button 1>", submitGrades)


frame = Frame(root, width=300, height=len(studentsDict)*2)
frame.pack()
frame.mainloop()




#
# About: This class creates a new Tkinter window and displays the selected section.
#
class sectionViewer:

	root = Tk()
	myStudents = []
	myUnsortedStudents = []
	myTables = []

	def __init__(self, className, sectionName, studentDictionary, ):
		pass

	def printHead(self):
		pass

	def printTables(self):
		pass

	def printUnsortedStudents(self):
		pass

	def printSubmit(self):
		pass

	def updateAttendance(self, event):
		pass

	def updateScore(self, event):
		pass

	def submitGrades(self, event):
		pass

# End of sectionViewer class



