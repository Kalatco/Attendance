# File: Attendance.py
# Author: Andrew Raftovich
# Date: Fall 2019
# Contact: AndrewRaftovich@gmail.com
#
# About: This class connects to a Google Sheets document to modify and append data as directed.
#
print("loading...give me a few seconds.")
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import json
import sys
import os.path

INPUT_FILE = "stdinfo.json"

class Attendance:

	# variables for Google Sheets API call
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
			 "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = None
	client = None
	sheet = None
	data = None

	# JSON data of input as a Dictionary
	my_students_dict = None

	# Lists containing misc. sheet data.
	my_students = None
	all_students = None
	all_sections = None

	# Dictionary containing temporary student data.
	section_scores = {}


	def __init__(self):

		# open the program input file.
		try:
			with open(INPUT_FILE, 'r') as f:
				self.my_students_dict = json.load(f)
		except:
			print("file not found, now ending program")
			sys.exit()

		# Authenticate input file
		cred_file = self.my_students_dict["keyFile"]
		self.creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, self.scope)
		self.client = gspread.authorize(self.creds)

		# Get the Google Sheet path
		sheet_name = self.my_students_dict["sheet"]
		self.sheet = self.client.open(sheet_name).sheet1
		self.data = self.sheet.get_all_records()

		# students in your section, excluding row/col describers.
		self.my_students = self.my_students_dict["students"]
		self.all_students = self.sheet.col_values(1)[1:]
		self.all_sections = self.sheet.row_values(1)[4:]

	# return a list of a user saved sub-set of users.
	def getMyStudents(self):
		return self.my_students

	# return a list of all updated sections
	def getSections(self):
		return(self.all_sections)

	# return a list of all updated students
	def getAllStudents(self):
		return(self.all_students)

	# returns a string of the defined Classroom name (CSC 210)
	def getClassName(self):
		return self.my_students_dict["class"]

	def getTablesDictionary(self):
		return self.my_students_dict["tables"]

	def getUnsortedStudents(self):
		return self.my_students_dict["unsorted"]

	# updates the JSON file with changed students or sections.
	def updateJson(self):
		jsonFile = open(INPUT_FILE, "w+")
		jsonFile.write(json.dumps(self.my_students_dict))
		jsonFile.close()


	# adds a student to the sub-set that already exists in the Sheets Data.
	def addStudent(self, student):
		for definedStudent in self.all_students:
			if(student == definedStudent):
				self.my_students.append(student)
				self.my_students_dict["students"].append(student)
				self.my_students_dict["unsorted"].append(student)
				break

	# adds a table to the json data
	def addTable(self, table):
		if(table not in self.my_students_dict["tables"]):
			self.my_students_dict["tables"][table] = []
		else:
			print("table already exits, no changes")

	# add a student to a specific table in the json data
	def addStudentToTable(self, table, student):
		if(table not in self.my_students_dict["tables"]):
			print(self.my_students_dict["tables"])
			self.my_students_dict["tables"][table].append(student)
			self.my_students_dict["unsorted"].remove(student)

	# adds a temporary grade to a student in the sub-set.
	def addScore(self, date, student, score):
		if(date not in self.section_scores):
			self.section_scores[date] = {}

		if(student in self.my_students):
			self.section_scores[date].update({student: score})

	# updates the Sheets data for a specific date and clears temporary data for that date.
	def submitScores(self, date):
		if(date in self.section_scores and date in self.all_sections):
			sectionNumber = 0

			for x in range(len(self.all_sections)):
				if(self.all_sections[x] == date):
					sectionNumber = x+5
					break

			if(sectionNumber != 0):
				for student, score in self.section_scores[date].items():
					row = 0
					for x in range(len(self.all_students)):
						if(student == self.all_students[x]):
							row = x+2
							break

					self.sheet.update_cell(row, sectionNumber, score)

			# dump values of date in dictionary
			self.section_scores[date] = {}


	# returns the temporary section grades  
	def getTempGrades(self, date):
		if (date in self.section_scores):
			return self.section_scores[date]
		return {}

	# gets already defined section grades for a particular section, for your subset of students
	def getDefinedGrades(self, date):
		returnDict = {}
		section = 0
		# check if section exists, and find position
		for x in range(len(self.all_sections)):
			if(date == self.all_sections[x]):
				section = x+5

		if(section == 0):
			return returnDict

		# turn data into a key/value pair with the corresponding student.
		for x in self.my_students:
			for row in range(len(self.all_students)):
				if(x == self.all_students[row]):
					returnDict[x] = self.sheet.cell(row+2, section).value
					break

		return returnDict

	# gets a list of all the defined sections that students are in from the google sheets.
	def getSectionNumbers(self):
		sectionDictionary = {}
		returnList = []
		for x in self.sheet.col_values(4)[1:]:
			if x not in sectionDictionary:
				sectionDictionary[x] = None

		for x in sorted(sectionDictionary):
			returnList.append(x)
		return returnList

	def addStudentsInSection(self, sectionNumber):
		for x in range(1, len(self.sheet.col_values(1))):
			if(self.sheet.cell(x+1, 4).value == sectionNumber):
				self.addStudent(self.sheet.cell(x+1,1).value)
		return self.my_students_dict["unsorted"]


# END of Attendance class

#-----------------------------------------------------------------------------------------------------
# About: Functions defined in this class are used to check if the user has the proper files installed.
#		 This code should always be ran before creating a Attendance class instance.

# check if program contains necessary files.
def doesStudentInfoExist():
	return os.path.exists(INPUT_FILE)

# run after doesStudentInfoExist() to check credentials
def doesStudentCredsExist():
	f = open(INPUT_FILE, 'r')
	text = json.load(f)
	return os.path.exists(text["keyFile"])

# create necessary file if it doesnt exist.
def createStudentInfoFile(className, sheetName):
	data = {
		"keyFile": "creds.json",
		"sheet": sheetName,
		"class": className,
		"students": [],
		"unsorted": [],
		"tables": {}
	}
	if(not doesStudentInfoExist()):
		with open(INPUT_FILE, 'w') as outfile:
			json.dump(data, outfile)

#------------------------------------------------------------------------------------------------------


#	Code Demonstration


#grader = Attendance()

#grader.addScore("Section 2", "Bill", 2)
#grader.addScore("Section 2", "Sam", 2)
#grader.addScore("Section 2", "Andrew", 2)
#grader.addScore("Section 2", "Max", 2) 	# since max is not in this section, his grades are unchanged.

#grader.submitScores("Section 2") 	# submits changes to the Google Sheets file
