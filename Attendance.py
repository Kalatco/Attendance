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

	# JSON data of input
	my_students_dict = None

	# temporary dictionary
	my_students = None
	all_students = None
	all_sections = None

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

		# students in your section
		self.my_students = self.my_students_dict['students']
		self.all_students = self.sheet.col_values(1)
		self.all_sections = self.sheet.row_values(1)


	# return a list of a user saved sub-set of users.
	def getStudents(self):
		return self.my_students

	# return a list of all updated sections
	def getSections(self):
		return(self.all_sections)

	# return a list of all updated students
	def getAllStudents(self):
		return(self.all_students)




p1 = Attendance()
print(p1.getAllStudents())


