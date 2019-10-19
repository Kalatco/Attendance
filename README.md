# Attendance Program

## Author

Andrew Raftovich

## About

UPDATE: This program is still in its early stages of production and the GUI is not setup yet.

This program was created to simplify attendance taking through a Google Sheets document by instead of
inserting scores manually into the Sheet, this program provides a GUI (Graphical User Interface) to allow
users to easily insert scores for their particular subset of students in their section from the full list
of students in the class.

![example of Google Sheets](/example.png)

The file contains some basic information before the section scores which will not be affected by the program.
Section scores are in a range from 0 (no points) to 2 (full points).

## Dependencies

	Python, Tkinter, and Bash Scripting

## Date

Fall 2019

## Usage

To get the program to work, the owner of the Google Sheets document must supply users with the 
Google Drive API credentials JSON file which must be inserted into the same file as the other
Python classes.

After that, users can run through the start up process for the program and added students already 
defined in the full list of students that are inside their section and also create table numbers 
to furthur simplify attendance taking.  The students and tables they choose will be saved locally 
inside a JSON file.