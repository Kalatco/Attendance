# File: Attendance.py
# Author: Andrew Raftovich
# Date: Fall 2019
#
# About: This class connects to a Google Sheets document to modify and append data as directed.
#
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
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

		# Get the Google Sheet name
		sheet_name = self.my_students_dict['sheet']
		self.sheet = self.client.open(sheet_name).sheet1
		self.data = self.sheet.get_all_records()

		# students in your section, excluding row/col describers.
		self.my_students = self.my_students_dict['students']
		self.all_students = self.sheet.col_values(1)[1:]
		self.all_sections = self.sheet.row_values(1)[1:]


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


	# updates the Sheets data for a specific date and clears temporary data.
	def submitScores(self, date):
		if(date in self.section_scores and date in self.all_sections):
			sectionNumber = 0

			for x in range(len(self.getSections())):
				if(self.getSections()[x] == date):
					sectionNumber = x+2
					break

			if(sectionNumber != 0):
				for student, score in self.section_scores[date].items():
					row = 0
					for x in range(len(self.getAllStudents())):
						if(student == self.getAllStudents()[x]):
							row = x+2
							break

					self.sheet.update_cell(row, sectionNumber, score)

			# dump values of date in dictionary
			self.section_scores[date] = {}


	# returns the temporary section grades
	def getTempGrades(self):
		return self.section_scores

# END of Attendance class



# testing code

p1 = Attendance()

print("my students")
print(p1.getMyStudents())

p1.addScore("Section 3", "Andrew", 2)
p1.addScore("Section 3", "Sam", 0)

p1.submitScores("Section 3")





