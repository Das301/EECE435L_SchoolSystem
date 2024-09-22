import sys
import os
from PyQt5.QtWidgets import QApplication, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QMessageBox, QComboBox, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from classes import School
import classes
import csv

app = QApplication(sys.argv)

my_school = School(os.path.basename(QFileDialog.getOpenFileName()[0]))
# list of already existing courses
courses = [x.course_id + " : " + x.course_name for x in my_school.courses] # will be used many times later

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
    
    dataStudents = [(x.student_id, x.name, x.age, x._email) for x in my_school.students]
    with open(filename+'Students.csv', 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['ID', 'Name', 'Age', 'Email'])
        csvwriter.writerows(dataStudents)
    
    dataInstructors = [(x.instructor_id, x.name, x.age, x._email) for x in my_school.instructors]
    with open(filename+'Instructors.csv', 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['ID', 'Name', 'Age', 'Email'])
        csvwriter.writerows(dataInstructors)
    
    dataCourses = [(x.course_id, x.course_name, x.instructor.instructor_id, x.instructor.name) if x.instructor is not None else (x.course_id, x.course_name, "TBA", "TBA") for x in my_school.courses]
    with open(filename+'Courses.csv', 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['ID', 'Name', 'Instructor ID', 'Instructor Name'])
        csvwriter.writerows(dataCourses)
    
    registeredCourses = []
    for x in my_school.students:
        for y in x.registered_courses:
            registeredCourses.append((x.student_id, x.name, y.course_id))
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
    object_to_delete = None
    if category=="Student Records":
        found = False
        for x in my_school.students:
            if x.student_id == id:
                object_to_delete = x
                found=True
                break
        if not found:
            QMessageBox.critical(window, "ERROR", "Student ID " + id + " does not exist!")
            delLabel.setText('')
            return
        else:
            if QMessageBox.question(window, "Delete Record", "Are you sure you want to delete this record", QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No) == QMessageBox.Yes:
                for z in object_to_delete.registered_courses:
                    z.enrolled_student.remove(object_to_delete)
                my_school.students.remove(object_to_delete)
    elif category=="Instructor Records":
        found = False
        for x in my_school.instructors:
            if x.instructor_id == id:
                object_to_delete = x
                found=True
                break
        if not found:
            QMessageBox.critical(window, "ERROR", "Instructor ID " + id + " does not exist!")
            delLabel.setText('')
            return
        else:
            if QMessageBox.question(window, "Delete Record", "Are you sure you want to delete this record", QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No) == QMessageBox.Yes:
                for z in object_to_delete.assigned_courses:
                    z.instructor = None
                my_school.instructors.remove(object_to_delete)
    elif category=="Course Records":
        found = False
        for x in my_school.courses:
            if x.course_id == id:
                object_to_delete = x
                found=True
                break
        if not found:
            QMessageBox.critical(window, "ERROR", "Course ID " + id + " does not exist!")
            delLabel.setText('')
            return
        else:
            if QMessageBox.question(window, "Delete Record", "Are you sure you want to delete this record", QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No) == QMessageBox.Yes:
                for z in object_to_delete.enrolled_student:
                    z.registered_courses.remove(object_to_delete)
                if object_to_delete.instructor is not None:
                    object_to_delete.instructor.assigned_courses.remove(object_to_delete)
                my_school.courses.remove(object_to_delete)
    my_school.save_to_json()
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
        found = False
        for x in my_school.students:
            if x.student_id == id:
                object_to_modify = x
                found=True
                break
        if not found:
            QMessageBox.critical(window, "ERROR", "Student ID " + id + " does not exist!")
            return
        else:
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
            nameBox.setText(object_to_modify.name)
            nameFrameLayout.addWidget(nameBox)
            nameFrameLayout.addStretch()
            nameFrame.setLayout(nameFrameLayout)
            recordLayout.addWidget(nameFrame)

            ageFrame = QFrame()
            ageFrameLayout = QHBoxLayout()
            ageFrameLayout.addWidget(QLabel('Student age: '))
            ageBox = QLineEdit()
            ageBox.resize(70, 20)
            ageBox.setText(str(object_to_modify.age))
            ageFrameLayout.addWidget(ageBox)
            ageFrameLayout.addStretch()
            ageFrame.setLayout(ageFrameLayout)
            recordLayout.addWidget(ageFrame)

            emailFrame = QFrame()
            emailFrameLayout = QHBoxLayout()
            emailFrameLayout.addWidget(QLabel('Student email: '))
            emBox = QLineEdit()
            emBox.resize(70, 20)
            emBox.setText(object_to_modify._email)
            emailFrameLayout.addWidget(emBox)
            emailFrameLayout.addStretch()
            emailFrame.setLayout(emailFrameLayout)
            recordLayout.addWidget(emailFrame)

            coursesFrame = QFrame()
            coursesFrameLayout = QHBoxLayout()
            coursesFrameLayout.addWidget(QLabel('Student courses: '))
            remainingCourses = QComboBox()
            remainingCourses.addItems([x.course_id for x in object_to_modify.registered_courses])
            coursesFrameLayout.addWidget(remainingCourses)
            coursesFrameLayout.addWidget(QPushButton("X", clicked=lambda:removeFromList(remainingCourses.currentText())))
            coursesFrameLayout.addStretch()
            coursesFrame.setLayout(coursesFrameLayout)
            recordLayout.addWidget(coursesFrame)
            print('Hello')
            fields = [nameBox, ageBox, emBox, remainingCourses]
        
    elif category == "Instructor Records":
        found = False
        for x in my_school.instructors:
            if x.instructor_id == id:
                object_to_modify = x
                found=True
                break
        if not found:
            QMessageBox.critical(window, "ERROR", "Instructor ID " + id + " does not exist!")
            return
        else:
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
            nameBox.setText(object_to_modify.name)
            nameFrameLayout.addWidget(nameBox)
            nameFrameLayout.addStretch()
            nameFrame.setLayout(nameFrameLayout)
            recordLayout.addWidget(nameFrame)

            ageFrame = QFrame()
            ageFrameLayout = QHBoxLayout()
            ageFrameLayout.addWidget(QLabel('Instructor age: '))
            ageBox = QLineEdit()
            ageBox.resize(70, 20)
            ageBox.setText(str(object_to_modify.age))
            ageFrameLayout.addWidget(ageBox)
            ageFrameLayout.addStretch()
            ageFrame.setLayout(ageFrameLayout)
            recordLayout.addWidget(ageFrame)

            emailFrame = QFrame()
            emailFrameLayout = QHBoxLayout()
            emailFrameLayout.addWidget(QLabel('Instructor email: '))
            emBox = QLineEdit()
            emBox.resize(70, 20)
            emBox.setText(object_to_modify._email)
            emailFrameLayout.addWidget(emBox)
            emailFrameLayout.addStretch()
            emailFrame.setLayout(emailFrameLayout)
            recordLayout.addWidget(emailFrame)
            
            fields = [nameBox, ageBox, emBox]

    elif category == "Course Records":
        found = False
        for x in my_school.courses:
            if x.course_id == id:
                object_to_modify = x
                found=True
                break
        if not found:
            QMessageBox.critical(window, "ERROR", "Course ID " + id + " does not exist!")
            return
        else:
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
            nameBox.setText(object_to_modify.course_name)
            nameFrameLayout.addWidget(nameBox)
            nameFrameLayout.addStretch()
            nameFrame.setLayout(nameFrameLayout)
            recordLayout.addWidget(nameFrame)

            instructorFrame = QFrame()
            instructorFrameLayout = QHBoxLayout()
            instructorFrameLayout.addWidget(QLabel("Instructor ID"))
            instructorBox = QLineEdit()
            instructorBox.resize(70, 20)
            if object_to_modify.instructor is not None:
                instructorBox.setText(object_to_modify.instructor.instructor_id)
            instructorFrameLayout.addWidget(instructorBox)
            instructorFrameLayout.addStretch()
            instructorFrame.setLayout(instructorFrameLayout)
            recordLayout.addWidget(instructorFrame)
            record.setLayout(recordLayout)
            fields = [nameBox, instructorBox]
    return

def editAndSave():
    global object_to_modify, fields, toRemove
    if type(object_to_modify) == classes.Student:
        try:
            int(fields[1].text())
        except:
            QMessageBox.critical(window, "ERROR", "Invalid data type! Age must be an integer!")
            return
        object_to_modify.name = fields[0].text()
        object_to_modify.age = int(fields[1].text())
        object_to_modify._email = fields[2].text()
        for x in toRemove:
            for i in object_to_modify.registered_courses:
                if i.course_id == x:
                    i.enrolled_student.remove(object_to_modify)
                    object_to_modify.registered_courses.remove(i)
                    break
    elif type(object_to_modify) == classes.Instructor:
        try:
            int(fields[1].text())
        except:
            QMessageBox.critical(window, "ERROR", "Invalid data type! Age must be an integer!")
            return
        object_to_modify.name = fields[0].text()
        object_to_modify.age = int(fields[1].text())
        object_to_modify._email = fields[2].text()
    elif type(object_to_modify) == classes.Course:
        if fields[1].text() != object_to_modify.instructor.instructor_id:
            object_to_modify.instructor.assigned_courses.remove(object_to_modify)
            if fields[1].text() == "":
                object_to_modify.instructor = None
            else:
                found = False
                for x in my_school.instructors:
                    if x.instructor_id == fields[1].text():
                        object_to_modify.instructor = x
                        found = True
                        break
                if not found:
                    object_to_modify.instructor = None
                    QMessageBox.critical(window, "ERROR", "Instructor with ID " + fields[1].text() + " does not exist! Course will be unassigned.")
        object_to_modify.course_name = fields[0].text()
        

    my_school.save_to_json()
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
        for x in my_school.students:
            if attribute=="Name":
                if keyword in x.name.lower():
                    rows.append((x.student_id, x.name, x.age, x._email))
            elif attribute=="ID":
                if keyword in x.student_id.lower():
                    rows.append((x.student_id, x.name, x.age, x._email))
            elif attribute=="Email":
                if keyword in x._email.lower():
                    rows.append((x.student_id, x.name, x.age, x._email))
            elif attribute=="Age":
                try:
                    keyword = int(keyword)
                    if keyword==x.age:
                        rows.append((x.student_id, x.name, x.age, x._email))
                except:
                    QMessageBox.critical(window, "ERROR", "Invalid data type passed! Must be integer!")
                    return
            elif attribute=="Course enrolled":
                for z in x.registered_courses:
                    if keyword in z.course_id.lower() or keyword in z.course_name.lower(): #giving the user the choice to search either by course ID or course Name
                        rows.append((x.student_id, x.name, x.age, x._email))

    elif category=="Instructors": #searching among instructor records
        for x in my_school.instructors:
            if attribute=="Name":
                if keyword in x.name.lower():
                    rows.append((x.instructor_id, x.name, x.age, x._email))
            elif attribute=="ID":
                if keyword in x.instructor_id.lower():
                    rows.append((x.instructor_id, x.name, x.age, x._email))
            elif attribute=="Email":
                if keyword in x._email.lower():
                    rows.append((x.instructor_id, x.name, x.age, x._email))
            elif attribute=="Age":
                try:
                    keyword = int(keyword)
                    if keyword==x.age:
                        rows.append((x.instructor_id, x.name, x.age, x._email))
                except:
                    QMessageBox.critical(window, "ERROR", "Invalid data type passed! Must be integer!")
                    return
    elif category=="Courses": #searching among courses records
        for x in my_school.courses:
            if attribute=="Name":
                if keyword in x.course_name.lower():
                    if x.instructor is not None:
                        rows.append((x.course_id, x.course_name, x.instructor.name))
                    else:
                        rows.append((x.course_id, x.course_name, "TBA"))
            elif attribute=="ID":
                if keyword in x.course_id.lower():
                    if x.instructor is not None:
                        rows.append((x.course_id, x.course_name, x.instructor.name))
                    else:
                        rows.append((x.course_id, x.course_name, "TBA"))
            elif attribute=="Instructor":
                if x.instructor is not None and keyword in x.instructor.name.lower():
                    rows.append((x.course_id, x.course_name, x.instructor.name))
    
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
    studentsTable.setRowCount(len(my_school.students))
    for x in my_school.students:
        studentsTable.setItem(row, 0, QTableWidgetItem(x.student_id))
        studentsTable.setItem(row, 1, QTableWidgetItem(x.name))
        studentsTable.setItem(row, 2, QTableWidgetItem(str(x.age)))
        studentsTable.setItem(row, 3, QTableWidgetItem(x._email))
        row += 1

def fillInstructorTables():  
    row = 0
    instructorsTable.setRowCount(len(my_school.instructors))
    for x in my_school.instructors:
        instructorsTable.setItem(row, 0, QTableWidgetItem(x.instructor_id))
        instructorsTable.setItem(row, 1, QTableWidgetItem(x.name))
        instructorsTable.setItem(row, 2, QTableWidgetItem(str(x.age)))
        instructorsTable.setItem(row, 3, QTableWidgetItem(x._email))
        row += 1

def fillCourseTables():   
    row = 0
    coursesTable.setRowCount(len(my_school.courses))
    for x in my_school.courses:
        coursesTable.setItem(row, 0, QTableWidgetItem(x.course_id))
        coursesTable.setItem(row, 1, QTableWidgetItem(x.course_name))
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
    instructor = None
    for x in my_school.instructors:
        if x.instructor_id == instructor_id:
            instructor = x
            break
    if instructor is None:
        QMessageBox.critical(window, "ERROR", "Instructor with ID " + instructor_id + " was not found!")
        resLabel2.setText('')
        return
    
    assigned = False
    for y in instructor.assigned_courses:
        if y.course_id == course:
            assigned = True
            break
    if not assigned:
        for z in my_school.courses:
            if z.course_id == course:
                if z.instructor is None:
                    instructor.assign_course(z)
                    resLabel2.setText('Course assigned successfully!')
                    break
                else:
                    QMessageBox.critical(window, "ERROR", "The course " + course + " is already assigned to a professor")
                    resLabel2.setText('')
                    return
    else:
        QMessageBox.warning(window, "WARNING", "Instructor with ID " + instructor_id + " is already assigned to the course " + course)
        resLabel2.setText('')
    my_school.save_to_json()
    pass

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
    student = None
    #looking for student with entered id
    for x in my_school.students:
        if x.student_id == student_id:
            student = x
            break
    if student is None:
        QMessageBox.critical(window, "ERROR", "Student with ID " + student_id + " was not found!")
        resLabel.setText('')
        return
    
    # checking if the student is already registered to the course
    registered = False
    for z in student.registered_courses:
        if z.course_id == course:
            registered = True
            break
    if not registered:
        for k in my_school.courses:
            if k.course_id == course:
                student.register_course(k)
                break
    else:
        QMessageBox.warning(window, "WARNING", "Student is already registered to the course " + course)
        resLabel.setText('')
        return
    resLabel.setText('Course registered successfully!')
    my_school.save_to_json()
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
        my_school.add_student_to_school(sID.text(), sName.text(), sAge.text(), sEmail.text())
        sID.setText("")
        sName.setText("")
        sAge.setText("")
        sEmail.setText("")
        studentsTable.clearContents()
        fillStudentTables()
    elif something == "instructor":
        my_school.add_instructor_to_school(iID.text(), iName.text(), iAge.text(), iEmail.text())
        iID.setText("")
        iName.setText("")
        iAge.setText("")
        iEmail.setText("")
        instructorsTable.clearContents()
        fillInstructorTables()
    else:
        my_school.add_course_to_school(cID.text(), cName.text())
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
    my_school.save_to_json()
    
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