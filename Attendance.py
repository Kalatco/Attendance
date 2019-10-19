# File: Attendance.py
# Author: Andrew Raftovich
# Date: Fall 2019
#
# About: This class connects to a Google Sheets document to modify and append data as directed.
#
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import sys

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

			# TODO: If file not found, create a json file and prompt info from the user.

		# Authenticate input file
		cred_file = self.my_students_dict['keyFile']
		self.creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, self.scope)
		self.client = gspread.authorize(self.creds)

		# Get the Google Sheet path
		sheet_name = self.my_students_dict['sheet']
		self.sheet = self.client.open(sheet_name).sheet1
		self.data = self.sheet.get_all_records()

		# students in your section, excluding row/col describers.
		self.my_students = self.my_students_dict['students']
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


	# adds a student to the sub-set that already exists in the Sheets Data.
	def addStudent(self, student):
		for definedStudent in self.all_students:
			if(student == definedStudent):
				self.my_students.append(student)
				break


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

# END of Attendance class



#------------------------------------------------------------------------------------------------------


# testing code

grader = Attendance()

grader.addScore("Section 2", "Bill", 2)
grader.addScore("Section 2", "Sam", 2)
grader.addScore("Section 2", "Andrew", 2)
grader.addScore("Section 2", "Max", 2)



grader.submitScores("Section 2")

print(grader.getDefinedGrades("Section 2"))




