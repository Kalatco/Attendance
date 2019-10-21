import Attendance
import sys
import os
import stat


print("Author Note: This file only needs to be ran once.")

### Start the setup code

# get the name of the class

# HARDCODED FOR SIMPLICITY
className = "CSC 210" 	#className = input("Type in the name of the class (ex: CSC 210): ")
sheetName = "tutorial"

# Check if the proper files are installed, else install the files
if( not Attendance.doesStudentInfoExist()):
	Attendance.createStudentInfoFile(className, sheetName)
	if ( not Attendance.doesStudentCredsExist()):
		print("To continue this program, insert the Creds.json file from the Google Sheets Administrator")
		sys.exit()
		
else:
	print("Would you like to reset your student info file and add change the section?")
	x = input("Insert: (yes/no)").lower()
	if(x == "yes"):
		os.remove("stdinfo.json")
		Attendance.createStudentInfoFile(className, sheetName)

print("loading Google Sheets...")
myGrades = Attendance.Attendance()
print("Attendance startup code ready")

# start adding students in the users section
sectionNumbers = availableSection = myGrades.getSectionNumbers()
sectionChosen = None

while True:
	print("List of available sections:")
	for x in sectionNumbers:
		print(x)

	sectionChose = input("Insert your section number: ")

	if(sectionChose in sectionNumbers):
		break

studentsChosen = myGrades.addStudentsInSection(sectionChose)

# list of students available
print("---------------------------")
print("Students Chosen:")
print("---------------------------")
for std in studentsChosen:
	print(std)
print("---------------------------")


# add students to tables
while True:
	table = input("Want to create a new table number? (table name / no) ")

	if(table.lower() == "no"):
		break

	myGrades.addTable(table)

	while True:
		std = input("Want to add a student to this table? (student first name / no) ")

		if(std.lower() == "no"):
			break

		foundStudent = None
		for x in studentsChosen:
			if(std.lower() in x.lower()):
				foundStudent = x

		if(foundStudent != None):
			myGrades.addStudentToTable(table, std)
		else:
			print("Student not found in section list")


while True:
	x = input("Data is recorded, do you want to save the data locally? (yes/no)").lower()
	if( x == "yes"):
		myGrades.updateJson()
		break
	elif( x == "no"):
		break


# Allows user to run GUI through ./grade.sh
st = os.stat("run.py")
os.chmod("run.py", st.st_mode | stat.S_IEXEC)

print("---------------------------")
print("Start up is finished, dont run this file again.")
print("Type \'grade\' to run the full program")
print("---------------------------")

