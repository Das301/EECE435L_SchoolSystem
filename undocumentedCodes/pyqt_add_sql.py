import sys
import os
from PyQt5.QtWidgets import QApplication, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QMessageBox, QComboBox, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
import csv
import sqlite3

app = QApplication(sys.argv)

conn = sqlite3.connect(os.path.basename(QFileDialog.getOpenFileName()[0]))
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# list of already existing courses
cursor.execute("SELECT course_id, name from courses")
courses = [x[0] + " : " + x[1] for x in cursor.fetchall()]  # will be used many times later

window = QWidget()
window.setWindowTitle("PyQt5 Tabs Example")
window.setGeometry(0, 0, 640, 460)

layout = QVBoxLayout()

tab_widget = QTabWidget()

# Creating the tabs
addStuffTab = QWidget()
registerCoursesTab = QWidget()
assignCoursesTab = QWidget()
displayTab = QWidget()
searchTab = QWidget()
editTab = QWidget()
deleteTab = QWidget()
exportTab = QWidget()

#creating the layouts
addStuffTabLayout = QHBoxLayout()
registerCoursesTabLayout = QVBoxLayout()
assignCoursesTabLayout = QVBoxLayout()
displayTabLayout = QVBoxLayout()
searchTabLayout = QVBoxLayout()
editTabLayout = QVBoxLayout()
deleteTabLayout = QVBoxLayout()
exportTabLayout = QVBoxLayout()

#export data to csv
def export_to_csv(filename):
    if filename[-4:] == ".csv":
        filename = filename[:-4]
    
    cursor.execute("SELECT * FROM students")
    dataStudents = cursor.fetchall()
    with open(filename+'Students.csv', 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['ID', 'Name', 'Age', 'Email'])
        csvwriter.writerows(dataStudents)
    
    cursor.execute("SELECT * FROM instructors")
    dataInstructors = cursor.fetchall()
    with open(filename+'Instructors.csv', 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['ID', 'Name', 'Age', 'Email'])
        csvwriter.writerows(dataInstructors)
    
    cursor.execute("SELECT courses.course_id, courses.name, courses.instructor_id, instructors.name FROM courses JOIN instructors ON instructors.instructor_id=courses.instructor_id")
    dataCourses = cursor.fetchall()
    with open(filename+'Courses.csv', 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['ID', 'Name', 'Instructor ID', 'Instructor Name'])
        csvwriter.writerows(dataCourses)
    
    cursor.execute("SELECT registered_courses.student_id, students.name, registered_courses.course_id FROM registered_courses JOIN students ON registered_courses.student_id=students.student_id")
    registeredCourses = cursor.fetchall()
    with open(filename+'Registration.csv', 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['ID', 'Name', 'Course ID'])
        csvwriter.writerows(registeredCourses)

    fileNameBox.setText('')

exportFrame = QFrame()
exportFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
exportFrame.setLineWidth(1)
exportFrame.setFixedHeight(100)
exportFrameLayout = QHBoxLayout()

exportFrameLayout.addWidget(QLabel('Enter file name (without .csv extension):'))
fileNameBox = QLineEdit()
fileNameBox.resize(70, 20)
exportFrameLayout.addWidget(fileNameBox)
exportFrameLayout.addWidget(QPushButton("Export to CSV", clicked=lambda: export_to_csv(fileNameBox.text())))
exportFrame.setLayout(exportFrameLayout)

exportTabLayout.addWidget(exportFrame)
exportTabLayout.addStretch()

#delete records
def deleteRecord(id, category):
    if category=="Student Records":
        cursor.execute("SELECT * FROM students WHERE student_id=?", (id, ))
        if cursor.fetchone() is None:
            QMessageBox.critical(window, "ERROR", "Student ID " + id + " does not exist!")
            delLabel.setText('')
            return
        else:
            if QMessageBox.question(window, "Delete Record", "Are you sure you want to delete this record", QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No) == QMessageBox.Yes:
                cursor.execute("DELETE FROM students WHERE student_id=?", (id, ))
                conn.commit()
            else:
                delLabel.setText('')
                return
    elif category=="Instructor Records":
        cursor.execute("SELECT * FROM instructors WHERE instructor_id=?", (id, ))
        if cursor.fetchone() is None:
            QMessageBox.critical(window, "ERROR", "Instructor ID " + id + " does not exist!")
            delLabel.setText('')
            return
        else:
            if QMessageBox.question(window, "Delete Record", "Are you sure you want to delete this record", QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No) == QMessageBox.Yes:
                cursor.execute("DELETE FROM instructors WHERE instructor_id=?", (id, ))
                conn.commit()
            else:
                delLabel.setText('')
                return
    elif category=="Course Records":
        cursor.execute("SELECT * FROM courses WHERE course_id=?", (id, ))
        if cursor.fetchone() is None:
            QMessageBox.critical(window, "ERROR", "Course ID " + id + " does not exist!")
            delLabel.setText('')
            return
        else:
            if QMessageBox.question(window, "Delete Record", "Are you sure you want to delete this record", QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No) == QMessageBox.Yes:
                cursor.execute("DELETE FROM courses WHERE course_id=?", (id, ))
                conn.commit()
            else:
                delLabel.setText('')
                return
    delLabel.setText('Operation performed successfully')

    studentsTable.clearContents()
    instructorsTable.clearContents()
    coursesTable.clearContents()

    fillStudentTables()
    fillInstructorTables()
    fillCourseTables()
    return

def changeLabelDel(e):
    if delOptions.currentText()=="Student Records":
        delInfoLabel.setText("Enter student ID:")
    elif delOptions.currentText()=="Instructor Records":
        delInfoLabel.setText("Enter instructor ID:")
    elif delOptions.currentText()=="Course Records":
        delInfoLabel.setText("Enter course ID:")

delRecordTypeFrame = QFrame()
delRecordTypeFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
delRecordTypeFrame.setLineWidth(1)
delRecordTypeFrame.setFixedHeight(70)
delRecordTypeFrameLayout = QHBoxLayout()

delRecordTypeFrameLayout.addWidget(QLabel('Edit:'))
delOptions = QComboBox()
delOptions.addItems(['Student Records', 'Instructor Records', 'Course Records'])
delOptions.currentTextChanged.connect(changeLabelDel)
delRecordTypeFrameLayout.addWidget(delOptions)
delRecordTypeFrameLayout.addStretch()
delRecordTypeFrame.setLayout(delRecordTypeFrameLayout)

delSearchFrame = QFrame()
delSearchFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
delSearchFrame.setLineWidth(1)
delSearchFrame.setFixedHeight(70)
delSearchFrameLayout = QHBoxLayout()

delInfoLabel = QLabel('Enter student ID:')
delSearchFrameLayout.addWidget(delInfoLabel)
delSearchBox = QLineEdit()
delSearchBox.resize(70, 20)
delSearchFrameLayout.addWidget(delSearchBox)
delSearchFrameLayout.addWidget(QPushButton('Delete', clicked=lambda: deleteRecord(delSearchBox.text(), delOptions.currentText())))
delSearchFrameLayout.addStretch()
delSearchFrame.setLayout(delSearchFrameLayout)

delLabel = QLabel('')

deleteTabLayout.addWidget(delRecordTypeFrame)
deleteTabLayout.addWidget(delSearchFrame)
deleteTabLayout.addWidget(delLabel)
deleteTabLayout.addStretch()

#editing records
def changeLabel(e):
    if options.currentText()=="Student Records":
        infoLabel.setText("Enter student ID:")
    elif options.currentText()=="Instructor Records":
        infoLabel.setText("Enter instructor ID:")
    elif options.currentText()=="Course Records":
        infoLabel.setText("Enter course ID:")

def removeFromList(courseID):
    try:
        current = [fields[3].itemText(i) for i in range(fields[3].count())]
        toRemove.append(courseID)
        current.remove(courseID)
        fields[3].clear()
        fields[3].addItems(current)
    except Exception as e:
        print(e)
    
#look for entity with specified ID and if found, load its data
def lookFor(id, category):
    global object_to_modify, fields, toRemove
    
    if category=="Student Records":
        cursor.execute("SELECT * FROM students WHERE student_id=?", (id,))
        record2 = cursor.fetchone()
        if record2 is None:
            QMessageBox.critical(window, "ERROR", "Student ID " + id + " does not exist!")
            return
        else:
            object_to_modify = ("Student", id)
            for child in record.findChildren(QWidget):
                child.deleteLater()
            toRemove = []

            idFrame = QFrame()
            idFrameLayout = QHBoxLayout()
            idFrameLayout.addWidget(QLabel('Student ID: '+id))
            idFrameLayout.addStretch()
            idFrame.setLayout(idFrameLayout)
            recordLayout.addWidget(idFrame)

            nameFrame = QFrame()
            nameFrameLayout = QHBoxLayout()
            nameFrameLayout.addWidget(QLabel('Student name: '))
            nameBox = QLineEdit()
            nameBox.resize(70, 20)
            nameBox.setText(record2[1])
            nameFrameLayout.addWidget(nameBox)
            nameFrameLayout.addStretch()
            nameFrame.setLayout(nameFrameLayout)
            recordLayout.addWidget(nameFrame)

            ageFrame = QFrame()
            ageFrameLayout = QHBoxLayout()
            ageFrameLayout.addWidget(QLabel('Student age: '))
            ageBox = QLineEdit()
            ageBox.resize(70, 20)
            ageBox.setText(str(record2[2]))
            ageFrameLayout.addWidget(ageBox)
            ageFrameLayout.addStretch()
            ageFrame.setLayout(ageFrameLayout)
            recordLayout.addWidget(ageFrame)

            emailFrame = QFrame()
            emailFrameLayout = QHBoxLayout()
            emailFrameLayout.addWidget(QLabel('Student email: '))
            emBox = QLineEdit()
            emBox.resize(70, 20)
            emBox.setText(record2[3])
            emailFrameLayout.addWidget(emBox)
            emailFrameLayout.addStretch()
            emailFrame.setLayout(emailFrameLayout)
            recordLayout.addWidget(emailFrame)

            coursesFrame = QFrame()
            coursesFrameLayout = QHBoxLayout()
            coursesFrameLayout.addWidget(QLabel('Student courses: '))
            remainingCourses = QComboBox()
            cursor.execute("SELECT course_id FROM registered_courses WHERE student_id=?", (id,))
            remainingCourses.addItems([x[0] for x in cursor.fetchall()])
            coursesFrameLayout.addWidget(remainingCourses)
            coursesFrameLayout.addWidget(QPushButton("X", clicked=lambda:removeFromList(remainingCourses.currentText())))
            coursesFrameLayout.addStretch()
            coursesFrame.setLayout(coursesFrameLayout)
            recordLayout.addWidget(coursesFrame)
            print('Hello')
            fields = [nameBox, ageBox, emBox, remainingCourses]
        
    elif category == "Instructor Records":
        cursor.execute("SELECT * FROM instructors WHERE instructor_id=?", (id,))
        record2 = cursor.fetchone()
        if record2 is None:
            QMessageBox.critical(window, "ERROR", "Instructor ID " + id + " does not exist!")
            return
        else:
            object_to_modify = ("Instructor", id)
            for child in record.findChildren(QWidget):
                child.deleteLater()
            toRemove = []

            idFrame = QFrame()
            idFrameLayout = QHBoxLayout()
            idFrameLayout.addWidget(QLabel('Instructor ID: '+id))
            idFrameLayout.addStretch()
            idFrame.setLayout(idFrameLayout)
            recordLayout.addWidget(idFrame)

            nameFrame = QFrame()
            nameFrameLayout = QHBoxLayout()
            nameFrameLayout.addWidget(QLabel('Instructor name: '))
            nameBox = QLineEdit()
            nameBox.resize(70, 20)
            nameBox.setText(record2[1])
            nameFrameLayout.addWidget(nameBox)
            nameFrameLayout.addStretch()
            nameFrame.setLayout(nameFrameLayout)
            recordLayout.addWidget(nameFrame)

            ageFrame = QFrame()
            ageFrameLayout = QHBoxLayout()
            ageFrameLayout.addWidget(QLabel('Instructor age: '))
            ageBox = QLineEdit()
            ageBox.resize(70, 20)
            ageBox.setText(str(record2[2]))
            ageFrameLayout.addWidget(ageBox)
            ageFrameLayout.addStretch()
            ageFrame.setLayout(ageFrameLayout)
            recordLayout.addWidget(ageFrame)

            emailFrame = QFrame()
            emailFrameLayout = QHBoxLayout()
            emailFrameLayout.addWidget(QLabel('Instructor email: '))
            emBox = QLineEdit()
            emBox.resize(70, 20)
            emBox.setText(record2[3])
            emailFrameLayout.addWidget(emBox)
            emailFrameLayout.addStretch()
            emailFrame.setLayout(emailFrameLayout)
            recordLayout.addWidget(emailFrame)
            
            fields = [nameBox, ageBox, emBox]

    elif category == "Course Records":
        cursor.execute("SELECT * FROM courses WHERE course_id=?", (id,))
        record2 = cursor.fetchone()
        if record2 is None:
            QMessageBox.critical(window, "ERROR", "Course ID " + id + " does not exist!")
            return
        else:
            object_to_modify = ("Course", id, record2[2])

            for child in record.findChildren(QWidget):
                child.deleteLater()
            toRemove = []

            idFrame = QFrame()
            idFrameLayout = QHBoxLayout()
            idFrameLayout.addWidget(QLabel('Course ID: '+id))
            idFrameLayout.addStretch()
            idFrame.setLayout(idFrameLayout)
            idFrameLayout.addStretch()
            idFrame.setLayout(idFrameLayout)
            recordLayout.addWidget(idFrame)

            nameFrame = QFrame()
            nameFrameLayout = QHBoxLayout()
            nameFrameLayout.addWidget(QLabel('Course name: '))
            nameBox = QLineEdit()
            nameBox.resize(70, 20)
            nameBox.setText(record2[1])
            nameFrameLayout.addWidget(nameBox)
            nameFrameLayout.addStretch()
            nameFrame.setLayout(nameFrameLayout)
            recordLayout.addWidget(nameFrame)

            instructorFrame = QFrame()
            instructorFrameLayout = QHBoxLayout()
            instructorFrameLayout.addWidget(QLabel("Instructor ID"))
            instructorBox = QLineEdit()
            instructorBox.resize(70, 20)
            instructorBox.setText(record2[2])
            instructorFrameLayout.addWidget(instructorBox)
            instructorFrameLayout.addStretch()
            instructorFrame.setLayout(instructorFrameLayout)
            recordLayout.addWidget(instructorFrame)
            record.setLayout(recordLayout)
            fields = [nameBox, instructorBox]
    return

def editAndSave():
    global object_to_modify, fields, toRemove
    if object_to_modify[0] == "Student":
        try:
            int(fields[1].text())
        except:
            QMessageBox.critical(window, "ERROR", "Invalid data type! Age must be an integer!")
            return
        cursor.execute("UPDATE students SET name=?, age=?, email=? WHERE student_id=?", (fields[0].text(), int(fields[1].text()), fields[2].text(), object_to_modify[1],))
        conn.commit()

        for x in toRemove:
            cursor.execute("DELETE FROM registered_courses WHERE student_id=? AND course_id=?", (object_to_modify[1], x,))
            conn.commit()
    elif object_to_modify[0] == "Instructor":
        try:
            int(fields[1].text())
        except:
            QMessageBox.critical(window, "ERROR", "Invalid data type! Age must be an integer!")
            return
        cursor.execute("UPDATE instructors SET name=?, age=?, email=? WHERE instructor_id=?", (fields[0].text(), int(fields[1].text()), fields[2].text(), object_to_modify[1],))
        conn.commit()
    elif object_to_modify[0] == "Course":
        try:
            if fields[1].text() == "":
                cursor.execute("UPDATE courses SET name=?, instructor_id=? WHERE course_id=?", (fields[0].text(), None, object_to_modify[1]))
            else:
                cursor.execute("UPDATE courses SET name=?, instructor_id=? WHERE course_id=?", (fields[0].text(), fields[1].text(), object_to_modify[1]))
            conn.commit()
        except sqlite3.IntegrityError as e:
            QMessageBox.critical(window, "ERROR", "Instructor with ID " + fields[1].text() + " does not exist! Course will be unassigned.")
            cursor.execute("UPDATE courses SET name=?, instructor_id=? WHERE course_id=?", (fields[0].text(), None, object_to_modify[1]))
            conn.commit()
        
    object_to_modify = None
    fields = None
    toRemove = []
    for child in record.findChildren(QWidget):
        child.deleteLater()
    studentsTable.clearContents()
    instructorsTable.clearContents()
    coursesTable.clearContents()

    fillStudentTables()
    fillInstructorTables()
    fillCourseTables()
    return

recordTypeFrame = QFrame()
recordTypeFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
recordTypeFrame.setLineWidth(1)
recordTypeFrame.setFixedHeight(70)
recordTypeFrameLayout = QHBoxLayout()

recordTypeFrameLayout.addWidget(QLabel('Edit:'))
options = QComboBox()
options.addItems(['Student Records', 'Instructor Records', 'Course Records'])
options.currentTextChanged.connect(changeLabel)
recordTypeFrameLayout.addWidget(options)
recordTypeFrameLayout.addStretch()
recordTypeFrame.setLayout(recordTypeFrameLayout)

searchFrame = QFrame()
searchFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
searchFrame.setLineWidth(1)
searchFrame.setFixedHeight(70)
searchFrameLayout = QHBoxLayout()

infoLabel = QLabel('Enter student ID:')
searchFrameLayout.addWidget(infoLabel)
searchBox = QLineEdit()
searchBox.resize(70, 20)
searchFrameLayout.addWidget(searchBox)
searchFrameLayout.addWidget(QPushButton('Search', clicked=lambda: lookFor(searchBox.text(), options.currentText())))
searchFrameLayout.addWidget(QPushButton('Edit', clicked=lambda: editAndSave()))
searchFrameLayout.addStretch()
searchFrame.setLayout(searchFrameLayout)

record = QFrame()
record.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
record.setLineWidth(1)
recordLayout = QVBoxLayout()
record.setLayout(recordLayout)

object_to_modify = None
fields = None
toRemove = []

editTabLayout.addWidget(recordTypeFrame)
editTabLayout.addWidget(searchFrame)
editTabLayout.addWidget(record)
editTabLayout.addStretch()

#Searching and Filtering of data
def changeFilters(e):
    if records.currentText() == "Students":
        filtersBox.clear()
        filtersBox.addItems(['ID', 'Name', 'Age', 'Email', 'Course enrolled'])
    elif records.currentText() == "Instructors":
        filtersBox.clear()
        filtersBox.addItems(['ID', 'Name', 'Age', 'Email'])
    elif records.currentText() == "Courses":
        filtersBox.clear()
        filtersBox.addItems(['ID', 'Name', 'Instructor'])

def search(category, attribute, keyword):
    if attribute!="Age":
        keyword = keyword.lower()
    rows = []
    if category == "":
        QMessageBox.critical(window, "ERROR", "No category selected!")
    elif category=="Students": #searching among students records
        rows.append(("ID", "Name", "Age", "Email"))
        if attribute=="Name":
            cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f'%{keyword}%',))
        elif attribute=="ID":
            cursor.execute("SELECT * FROM students WHERE student_id LIKE ?", (f'%{keyword}%',))
        elif attribute=="Email":
            cursor.execute("SELECT * FROM students WHERE email LIKE ?", (f'%{keyword}%',))
        elif attribute=="Age":
            try:
                keyword = int(keyword)
                cursor.execute("SELECT * FROM students WHERE age=?", (keyword,))
            except:
                QMessageBox.critical(window, "ERROR", "Invalid data type passed! Must be integer!")
                return
        elif attribute=="Course enrolled":
            cursor.execute("SELECT DISTINCT students.student_id, students.name, students.age, students.email FROM students JOIN registered_courses ON students.student_id = registered_courses.student_id WHERE registered_courses.course_id LIKE ?", (f'%{keyword}%',))
        for x in cursor.fetchall():
            rows.append(x)
            
    elif category=="Instructors": #searching among instructor records
        rows.append(("ID", "Name", "Age", "Email"))
        if attribute=="Name":
            cursor.execute("SELECT * FROM instructors WHERE name LIKE ?", (f'%{keyword}%',))
        elif attribute=="ID":
            cursor.execute("SELECT * FROM instructors WHERE instructor_id LIKE ?", (f'%{keyword}%',))
        elif attribute=="Email":
            cursor.execute("SELECT * FROM instructors WHERE email LIKE ?", (f'%{keyword}%',))
        elif attribute=="Age":
            try:
                keyword = int(keyword)
                cursor.execute("SELECT * FROM instructors WHERE age=?", (keyword,))
            except:
                QMessageBox.critical(window, "ERROR", "Invalid data type passed! Must be integer!")
                return
        for x in cursor.fetchall():
            rows.append(x)

    elif category=="Courses": #searching among courses records
        rows.append(("Course ID", "Course Name", "Instructor"))
        if attribute=="Name":
            cursor.execute("SELECT * FROM courses WHERE name LIKE ?", (f'%{keyword}%',))
        elif attribute=="ID":
            cursor.execute("SELECT * FROM courses WHERE course_id LIKE ?", (f'%{keyword}%',))
        elif attribute=="Instructor":
            cursor.execute("SELECT courses.course_id, courses.name, instructors.name FROM courses JOIN instructors ON instructors.instructor_id=courses.instructor_id WHERE instructors.name LIKE ?", (f'%{keyword}%',))
        for x in cursor.fetchall():
            rows.append(x)
    
    if category=="Students" or category=="Instructors":
        results.clear()
        results.setColumnCount(4)
        results.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email'])
        results.setColumnWidth(2, 30)
        results.setColumnWidth(3, 220)
        results.setRowCount(len(rows))
        index = 0
        for i in rows:
            results.setItem(index, 0, QTableWidgetItem(i[0]))
            results.setItem(index, 1, QTableWidgetItem(i[1]))
            results.setItem(index, 2, QTableWidgetItem(str(i[2])))
            results.setItem(index, 3, QTableWidgetItem(i[3]))
            index += 1
    elif category=="Courses":
        results.clear()
        results.setColumnCount(3)
        results.setHorizontalHeaderLabels(['ID', 'Name', 'Instructor'])
        results.setColumnWidth(1, 220)
        results.setColumnWidth(2, 120)
        results.setRowCount(len(rows))
        index = 0
        for i in rows:
            results.setItem(index, 0, QTableWidgetItem(i[0]))
            results.setItem(index, 1, QTableWidgetItem(i[1]))
            results.setItem(index, 2, QTableWidgetItem(i[2]))
            index += 1
    

categories = QFrame()
categories.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
categories.setLineWidth(1)
categories.setFixedHeight(70)
categoriesLayout = QHBoxLayout()

categoriesLayout.addWidget(QLabel('Search in:'))
records = QComboBox()
records.addItems(['Students', 'Instructors', 'Courses'])
records.currentTextChanged.connect(changeFilters)
categoriesLayout.addWidget(records)
categoriesLayout.addStretch()
categories.setLayout(categoriesLayout)

filters = QFrame()
filters.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
filters.setLineWidth(1)
filters.setFixedHeight(70)
filtersLayout = QHBoxLayout()

filtersLayout.addWidget(QLabel('Filter by:'))
filtersBox = QComboBox()
filtersBox.addItems(['ID', 'Name', 'Age', 'Email', 'Course enrolled'])
filtersLayout.addWidget(filtersBox)
filtersLayout.addWidget(QLabel('Enter keyword:'))
box = QLineEdit()
box.resize(70, 20)
filtersLayout.addWidget(box)
filtersLayout.addWidget(QPushButton('Search', clicked=lambda: search(records.currentText(), filtersBox.currentText(), box.text())))
filtersLayout.addStretch()
filters.setLayout(filtersLayout)

results = QTableWidget(window)
results.setFixedHeight(250)

searchTabLayout.addWidget(categories)
searchTabLayout.addWidget(filters)
searchTabLayout.addWidget(results)
searchTabLayout.addStretch()

#Displaying all data
def fillStudentTables():
    row = 0
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    studentsTable.setRowCount(len(data))
    for x in data:
        studentsTable.setItem(row, 0, QTableWidgetItem(x[0]))
        studentsTable.setItem(row, 1, QTableWidgetItem(x[1]))
        studentsTable.setItem(row, 2, QTableWidgetItem(str(x[2])))
        studentsTable.setItem(row, 3, QTableWidgetItem(x[3]))
        row += 1

def fillInstructorTables():  
    row = 0
    cursor.execute("SELECT * FROM instructors")
    data = cursor.fetchall()
    instructorsTable.setRowCount(len(data))
    for x in data:
        instructorsTable.setItem(row, 0, QTableWidgetItem(x[0]))
        instructorsTable.setItem(row, 1, QTableWidgetItem(x[1]))
        instructorsTable.setItem(row, 2, QTableWidgetItem(str(x[2])))
        instructorsTable.setItem(row, 3, QTableWidgetItem(x[3]))
        row += 1

def fillCourseTables():   
    row = 0
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    coursesTable.setRowCount(len(data))
    for x in data:
        coursesTable.setItem(row, 0, QTableWidgetItem(x[0]))
        coursesTable.setItem(row, 1, QTableWidgetItem(x[1]))
        row += 1

studentsTable = QTableWidget(window)
instructorsTable = QTableWidget(window)
coursesTable = QTableWidget(window)

studentsTable.setFixedHeight(150)
studentsTable.setColumnCount(4)
studentsTable.setColumnWidth(2, 30)
studentsTable.setColumnWidth(3, 220)

instructorsTable.setFixedHeight(150)
instructorsTable.setColumnCount(4)
instructorsTable.setColumnWidth(2, 30)
instructorsTable.setColumnWidth(3, 220)

coursesTable.setFixedHeight(150)
coursesTable.setColumnCount(2)
coursesTable.setColumnWidth(1, 260)

studentsTable.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email'])
instructorsTable.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email'])
coursesTable.setHorizontalHeaderLabels(['ID', 'Name'])

fillStudentTables()
fillInstructorTables()
fillCourseTables()

displayTabLayout.addWidget(studentsTable)
displayTabLayout.addWidget(instructorsTable)
displayTabLayout.addWidget(coursesTable)

# Course assignment

def assign(instructor_id, course):
    course = course.split(" : ")[0]
    if instructor_id=="":
        return
    course = course.split(" : ")[0]
    try:
        cursor.execute("SELECT instructor_id FROM courses WHERE course_id=?", (course,))
        if cursor.fetchone()[0] is None:
            cursor.execute("UPDATE courses SET instructor_id=? WHERE course_id=?", (instructor_id, course))
            conn.commit()
        else:
            QMessageBox.warning(window, "WARNING", "Course "+course+ " is already assigned!")
            resLabel2.setText('')
            return
    except sqlite3.IntegrityError as e:
        QMessageBox.warning(window, "ERROR", "Instructor ID "+instructor_id+ " does not exist!")
        resLabel2.setText('')
        return
    resLabel2.setText('Course assigned successfully!')
    return

#Frame to enter the instructor ID
iidFrame = QFrame()
iidFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
iidFrame.setLineWidth(1)
iidFrame.setFixedHeight(70)
iidFrame_layout = QHBoxLayout()

iidFrame_layout.addWidget(QLabel('Enter Instructor ID:'))
iIDbox = QLineEdit()
iIDbox.resize(70, 20)
iidFrame_layout.addWidget(iIDbox)
iidFrame_layout.addStretch()

#Frame to choose the course
iCoursesFrame = QFrame()
iCoursesFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
iCoursesFrame.setLineWidth(1)
iCoursesFrame.setFixedHeight(70)
iCoursesFrame_layout = QHBoxLayout()
iCoursesFrame_layout.addWidget(QLabel('Choose a course:'))
coursesBox = QComboBox()
coursesBox.addItems(courses)
iCoursesFrame_layout.addWidget(coursesBox)
iCoursesFrame_layout.addWidget(QPushButton('Assign course', clicked=lambda: assign(iIDbox.text(), coursesBox.currentText())))
iCoursesFrame_layout.addStretch()

#label to show the operation's result
resLabel2 = QLabel('')

iidFrame.setLayout(iidFrame_layout)
iCoursesFrame.setLayout(iCoursesFrame_layout)
assignCoursesTabLayout.addWidget(iidFrame)
assignCoursesTabLayout.addWidget(iCoursesFrame)
assignCoursesTabLayout.addWidget(resLabel2)
assignCoursesTabLayout.addStretch()

#Student registration

def register(student_id, course):
    course = course.split(" : ")[0]
    #looking for student with entered id
    try:
        cursor.execute("INSERT INTO registered_courses VALUES(?, ?)", (student_id, course))
        conn.commit()
    except sqlite3.IntegrityError as e:
        cursor.execute("SELECT * FROM registered_courses WHERE student_id=? AND course_id=?", (student_id, course))
        if len(cursor.fetchall())>=1:
            QMessageBox.critical(window, "ERROR", "Student with ID "+student_id+" is already enrolled in the course "+course+"!")
        else:
            QMessageBox.critical(window, "ERROR", "Student with ID "+student_id+" does not exist!")
        resLabel.setText('')
        return
    resLabel.setText('Course registered successfully!')
    return

#Frame to enter the student ID
sidFrame = QFrame()
sidFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
sidFrame.setLineWidth(1)
sidFrame.setFixedHeight(70)
sidFrame_layout = QHBoxLayout()

sidFrame_layout.addWidget(QLabel('Enter Student ID:'))
IDbox = QLineEdit()
IDbox.resize(70, 20)
sidFrame_layout.addWidget(IDbox)
sidFrame_layout.addStretch()

#Frame to choose the course
sCoursesFrame = QFrame()
sCoursesFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
sCoursesFrame.setLineWidth(1)
sCoursesFrame.setFixedHeight(70)
sCoursesFrame_layout = QHBoxLayout()
sCoursesFrame_layout.addWidget(QLabel('Choose a course:'))
courseBox = QComboBox()
courseBox.addItems(courses)
sCoursesFrame_layout.addWidget(courseBox)
sCoursesFrame_layout.addWidget(QPushButton('Register course', clicked=lambda: register(IDbox.text(), courseBox.currentText())))
sCoursesFrame_layout.addStretch()

#label to show the operation's result
resLabel = QLabel('')

sidFrame.setLayout(sidFrame_layout)
sCoursesFrame.setLayout(sCoursesFrame_layout)
registerCoursesTabLayout.addWidget(sidFrame)
registerCoursesTabLayout.addWidget(sCoursesFrame)
registerCoursesTabLayout.addWidget(resLabel)
registerCoursesTabLayout.addStretch()

# adding students, instructors, and courses
def add_something(something):
    if something=="student":
        #verifying validity of inputs
        try:
            try:
                int(sAge.text())
            except:
                QMessageBox.critical(window, "ERROR", "Invalid data type! Age must be an integer!")
                return
            if sID.text() == "" or sName.text()=="" or int(sAge.text())<=0 or sEmail.text()=="" or '@' not in sEmail.text():
                QMessageBox.critical(window, "ERROR", "Missing or invalid fields")
                return
            conn.execute("INSERT INTO students VALUES(?, ?, ?, ?)", (sID.text(), sName.text(), sAge.text(), sEmail.text()))
        except sqlite3.IntegrityError as e:
            QMessageBox.critical(window, "ERROR", "Entered student ID already exists!")
            return
        sID.setText("")
        sName.setText("")
        sAge.setText("")
        sEmail.setText("")
        studentsTable.clearContents()
        fillStudentTables()
    elif something == "instructor":
        #verifying validity of inputs
        try:
            try:
                int(iAge.text())
            except:
                QMessageBox.critical(window, "ERROR", "Invalid data type! Age must be an integer!")
                return
            if iID.text() == "" or iName.text()=="" or int(iAge.text())<=0 or iEmail.text()=="" or '@' not in iEmail.text():
                QMessageBox.critical(window, "ERROR", "Missing or invalid fields")
                return

            conn.execute("INSERT INTO instructors VALUES(?, ?, ?, ?)", (iID.text(), iName.text(), iAge.text(), iEmail.text()))
        except sqlite3.IntegrityError as e:
            QMessageBox.critical(window, "ERROR", "Entered instructor ID already exists!")
            return
        iID.setText("")
        iName.setText("")
        iAge.setText("")
        iEmail.setText("")
        instructorsTable.clearContents()
        fillInstructorTables()
    else:
        #verifying validity of inputs
        if cID.text() == "" or cName.text()=="":
            QMessageBox.warning(window, "WARNING", "Missing field")
            return "Missing field"

        try:
            conn.execute("INSERT INTO courses VALUES(?, ?, ?)", (cID.text(), cName.text(), None))
        except sqlite3.IntegrityError as e:
            QMessageBox.critical(window, "ERROR", "Entered course ID already exists!")
            return
        # updating the list of courses presented in other tabs
        courses.append(cID.text() + " : " + cName.text())
        courseBox.clear()
        courseBox.addItems(courses)
        coursesBox.clear()
        coursesBox.addItems(courses)
        # clearing the input boxes
        cID.setText("")
        cName.setText("")
        coursesTable.clearContents()
        fillCourseTables()
    conn.commit()
    return

student_frame = QFrame()
student_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
student_frame.setLineWidth(1)
student_frame.setFixedWidth(210)
student_frame_layout = QVBoxLayout()

student_frame_layout.addWidget(QLabel('         Student Info'))
student_frame_layout.addWidget(QLabel('Enter Student ID:'))
sID = QLineEdit()
sID.resize(180, 20)
student_frame_layout.addWidget(sID)

student_frame_layout.addWidget(QLabel('Enter Student Name:'))
sName = QLineEdit()
sName.resize(180, 20)
student_frame_layout.addWidget(sName)

student_frame_layout.addWidget(QLabel('Enter Student Age:'))
sAge = QLineEdit()
sAge.setValidator(QIntValidator())
sAge.resize(180, 20)
student_frame_layout.addWidget(sAge)

student_frame_layout.addWidget(QLabel('Enter Student Email:'))
sEmail = QLineEdit()
sEmail.resize(180, 20)
student_frame_layout.addWidget(sEmail)

student_frame_layout.addStretch()
student_frame_layout.addWidget(QPushButton('Add Student', clicked=lambda: add_something("student")))

student_frame_layout.setAlignment(Qt.AlignCenter)
student_frame.setLayout(student_frame_layout)

instructor_frame = QFrame()
instructor_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
instructor_frame.setLineWidth(1)
instructor_frame.setFixedWidth(210)
instructor_frame_layout = QVBoxLayout()

instructor_frame_layout.addWidget(QLabel('         Instructor Info'))
instructor_frame_layout.addWidget(QLabel('Enter Instructor ID:'))
iID = QLineEdit()
iID.resize(180, 20)
instructor_frame_layout.addWidget(iID)

instructor_frame_layout.addWidget(QLabel('Enter Instructor Name:'))
iName = QLineEdit()
iName.resize(180, 20)
instructor_frame_layout.addWidget(iName)

instructor_frame_layout.addWidget(QLabel('Enter Instructor Age:'))
iAge = QLineEdit()
iAge.setValidator(QIntValidator())
iAge.resize(180, 20)
instructor_frame_layout.addWidget(iAge)

instructor_frame_layout.addWidget(QLabel('Enter Instructor Email:'))
iEmail = QLineEdit()
iEmail.resize(180, 20)
instructor_frame_layout.addWidget(iEmail)

instructor_frame_layout.addStretch()
instructor_frame_layout.addWidget(QPushButton('Add Instructor', clicked=lambda: add_something("instructor")))

instructor_frame_layout.setAlignment(Qt.AlignCenter)

instructor_frame.setLayout(instructor_frame_layout)

course_frame = QFrame()
course_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
course_frame.setLineWidth(1)
course_frame.setFixedWidth(210)
course_frame_layout = QVBoxLayout()

course_frame_layout.addWidget(QLabel('          Course Info'))
course_frame_layout.addWidget(QLabel('Enter Course ID:'))
cID = QLineEdit()
cID.resize(180, 20)
course_frame_layout.addWidget(cID)

course_frame_layout.addWidget(QLabel('Enter Course Name:'))
cName = QLineEdit()
cName.resize(180, 20)
course_frame_layout.addWidget(cName)

course_frame_layout.addStretch()
course_frame_layout.addWidget(QPushButton('Add Course', clicked=lambda: add_something("course")))

course_frame_layout.setAlignment(Qt.AlignCenter)
course_frame.setLayout(course_frame_layout)

addStuffTabLayout.addWidget(student_frame)
addStuffTabLayout.addWidget(instructor_frame)
addStuffTabLayout.addWidget(course_frame)

#setting the tabs' layout
addStuffTab.setLayout(addStuffTabLayout)
registerCoursesTab.setLayout(registerCoursesTabLayout)
assignCoursesTab.setLayout(assignCoursesTabLayout)
displayTab.setLayout(displayTabLayout)
searchTab.setLayout(searchTabLayout)
editTab.setLayout(editTabLayout)
deleteTab.setLayout(deleteTabLayout)
exportTab.setLayout(exportTabLayout)

#adding the tabs to the window
tab_widget.addTab(addStuffTab, 'Add')
tab_widget.addTab(registerCoursesTab, 'Register')
tab_widget.addTab(assignCoursesTab, 'Assign')
tab_widget.addTab(displayTab, 'Display')
tab_widget.addTab(searchTab, 'Search')
tab_widget.addTab(editTab, 'Edit')
tab_widget.addTab(deleteTab, 'Delete')
tab_widget.addTab(exportTab, 'Export')


#add the widgets to the window
layout.addWidget(tab_widget)
window.setLayout(layout)

window.show()

sys.exit(app.exec_())