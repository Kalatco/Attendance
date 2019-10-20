# Attendance Program

Andrew Raftovich, Fall 2019

## About

This program was created to simplify attendance taking through a Google Sheets document by instead of
inserting scores manually into the Sheet, this program provides a GUI (Graphical User Interface) to allow
users to easily insert/modify scores for their students in their section from the full list of students in 
the class.

![example of Google Sheets](/example.png)

The file contains some basic information before the section scores which will not be affected by the program.
Section scores are in a range from 0 (no points) to 2 (full points).

## Usage

1. To get the program to work, the owner of the Google Sheets document must supply users with the 
   Google Drive API credentials JSON file which must be inserted into the same file as the other
   Python classes.

2. After that, users can run through the start up process for the program and add all students inside their section
   and also create table numbers to further simplify attendance taking.  The students and tables you choose will be 
   saved locally on your computer so you will only need to do this step once.

3. When setup is complete, you will be able to log on to the application and quickly be able to access and modify grades
   for a specified section.

## Dependencies

	Python, Tkinter, and Bash Scripting
