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
myButtons = []
grader = Attendance()
print("Program has loaded.")
grader.updateJson()

className = grader.getClassName()
currentSection = grader.getSections()[-1]
students = grader.getDefinedGrades(currentSection)

# converts the strings of data to integers.
for x in students:
	if students[x] == '':
		students[x] = -1
	else:
		students[x] = int(students[x])

#----------------------------------------------------------------------

# Updates the attendance number for the current student.
def updateAttendance(event):
	std = event.widget.cget("text")

	if(students[std] == -1):
		students[std] = 2
	
	elif (students[std] == 2):
		students[std] = 1

	elif (students[std] == 1):
		students[std] = 0

	else:
		students[std] = -1

	score = students[std]
	if(score == -1):
		score = ''

	updateScore(std, score)
	event.widget.config(background=COLORS[students[std]])
	submit.config(fg="red")

def updateScore(std, score):
	grader.addScore(currentSection, std, score)


def submitGrades(event):
	grader.submitScores(currentSection)
	submit.config(fg="green")


#--------------------------------------------------------------------------------------------

root = Tk()
root.title("Attendance Program")
root.resizable(False, False)

# header
header = Label(root, text=className+": "+currentSection, font=("arial", 16, "bold"), height=2)
header.pack(fill=X)

# body
for student in sorted(students.keys()):
	temp = Label(root, text=student, bg = COLORS[students[student]], fg="black", font=("arial",16))
	temp.config(height=2)
	temp.pack(fill=X)
	temp.bind("<Button 1>", updateAttendance)
	myButtons.append(temp)

# footer
submit = Label(root, text=SUBMIT_BUTTON_TEXT, font=("arial", 16,"bold"), height=2, fg="green")
submit.pack(fill=X)
submit.bind("<Button 1>", submitGrades)


frame = Frame(root, width=300, height=len(students)*2)
frame.pack()
frame.mainloop()
