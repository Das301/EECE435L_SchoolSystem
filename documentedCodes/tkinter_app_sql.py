#for this part, we assume that IDs are unique

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sqlite3

"""
Initializing the connection with the selected database, configuring the graphical user interface, getting a 
list of all the courses as it will be used in many places, and creating all the tabs of the application
"""
conn = sqlite3.connect(filedialog.askopenfilename())
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

root = Tk()
root.title("School Management System")
root.geometry("640x350")
root.configure(background="#c9c8c7")

# list of already existing courses
cursor.execute("SELECT course_id, name from courses")
courses = [x[0] + " : " + x[1] for x in cursor.fetchall()] # will be used many times later

# setting up the tabs
tabControl = ttk.Notebook(root)

addStuffTab = Frame(tabControl)
registerCoursesTab = Frame(tabControl)
assignCoursesTab = Frame(tabControl)
displayTab = Frame(tabControl)
searchTab = Frame(tabControl)
editTab = Frame(tabControl)
deleteTab = Frame(tabControl)
tabControl.add(addStuffTab, text="Add")
tabControl.add(registerCoursesTab, text="Register")
tabControl.add(assignCoursesTab, text="Assign")
tabControl.add(displayTab, text="Display")
tabControl.add(searchTab, text="Search")
tabControl.add(editTab, text="Edit")
tabControl.add(deleteTab, text="Delete")
tabControl.pack(expand=1, fill=BOTH)

#Delete Records
def deleteRecord(id, category):
    """
    This function iss responsible of deleting a record from the database. It first checks that the targeted record
    exists and verify that the user wants to proceed with the operation. It will alert the user in case the record doesn't exist.
    
    Args:
        type id: str
        id: the identifier of the target record (student, instructor or course id)
        type category: str
        category: specifies if we want to delete a student, instructor, or course record
    
    Returns:
        :return:none
    
    """

    if category=="Student Records":
        cursor.execute("SELECT * FROM students WHERE student_id=?", (id, ))
        if cursor.fetchone() is None:
            messagebox.showerror("ERROR", "Student ID " + id + " does not exist!")
            return
        else:
            if messagebox.askyesno("Delete Record", "Are you sure you want to delete this record"):
                cursor.execute("DELETE FROM students WHERE student_id=?", (id, ))
                conn.commit()
    elif category=="Instructor Records":
        cursor.execute("SELECT * FROM instructors WHERE instructor_id=?", (id, ))
        if cursor.fetchone() is None:
            messagebox.showerror("ERROR", "Instructor ID " + id + " does not exist!")
            return
        else:
            if messagebox.askyesno("Delete Record", "Are you sure you want to delete this record"):
                cursor.execute("DELETE FROM instructors WHERE instructor_id=?", (id, ))
                conn.commit()
    elif category=="Course Records":
        cursor.execute("SELECT * FROM courses WHERE course_id=?", (id, ))
        if cursor.fetchone() is None:
            messagebox.showerror("ERROR", "Course ID " + id + " does not exist!")
            return
        else:
            if messagebox.askyesno("Delete Record", "Are you sure you want to delete this record"):
                cursor.execute("DELETE FROM courses WHERE course_id=?", (id, ))
                conn.commit()
    
    deleteIdBox.delete('1.0', "end")
    treeview.delete(*treeview.get_children())
    fillTreeview()
    return

def changeLabel2(e):
    """
    This function will simply modify the label when changing the type of record we want to delete
    
    Returns:
        :return: none
    """
    if deleteBox.get()=="Student Records":
        label2.config(text="Enter student ID:")
    elif deleteBox.get()=="Instructor Records":
        label2.config(text="Enter instructor ID:")
    elif deleteBox.get()=="Course Records":
        label2.config(text="Enter course ID:")
    else:
        label2.config(text="Enter ID:")
#frame in which we choose the type of record to modify (student, instructor, course)
delete = Frame(deleteTab, height=30)
delete.pack(side="top", padx=3,pady=5, fill=X)
Label(delete, text="Edit:").pack(side="left", padx=3)
deleteBox = ttk.Combobox(delete, values=["Student Records", "Instructor Records" , "Course Records"], width=30, state="readonly")
deleteBox.pack(side="left")
deleteBox.bind("<<ComboboxSelected>>", changeLabel2)

#frame to search for specific record according to ID (must enter the full ID)
searchFrame2 = Frame(deleteTab, height=30)
searchFrame2.pack(side="top", padx=3,pady=5, fill=X)
label2 = Label(searchFrame2, text="Enter ID:")
label2.pack(side="left", padx=3)
deleteIdBox = Text(searchFrame2, height=1, width=22)
deleteIdBox.pack(side="left", padx=3)
Button(searchFrame2, text="Delete", relief="raised", command=lambda: deleteRecord(deleteIdBox.get(1.0, "end-1c"), deleteBox.get())).pack(side="left")


#Edit Records
def changeLabel(e):
    """
    This function will simply modify the label when changing the type of record we want to edit
    
    Returns:
        :return: none
    """
    if editBox.get()=="Student Records":
        label.config(text="Enter student ID:")
    elif editBox.get()=="Instructor Records":
        label.config(text="Enter instructor ID:")
    elif editBox.get()=="Course Records":
        label.config(text="Enter course ID:")
    else:
        label.config(text="Enter ID:")

def removeFromList(courseID):
    """
    This function is used to update the list of courses the student wants to drop and the list of courses he/she wants to keep
    
    Args:
        type courseID: str
        courseID: id of the course the student wants to drop

    Returns:
        :return: none
    """
    try:
        current = list(fields[3]['values'])
        toRemove.append(courseID)
        current.remove(courseID)
        fields[3]['values'] = current
        fields[3].set("")
    except Exception as e:
        print(e)
    
#look for entity with specified ID and if found, load its data
def lookFor(id, category):
    """
    This function is responsible to search for the record we would like to modify and display its information on the window. The user will be informed in case the record is not found.
    
    Argss:
        type id: str
        id: identifier of the record to edit
        type category: str
        category: record type to edit (student, instructor, course)   

    Returns:
        :return: none
    """

    global object_to_modify, fields, toRemove
    
    if category=="Student Records":
        cursor.execute("SELECT * FROM students WHERE student_id=?", (id,))
        record2 = cursor.fetchone()
        if record2 is None:
            messagebox.showerror("ERROR", "Student ID " + id + " does not exist!")
            return
        else:
            object_to_modify = ("Student", id)
            for widget in record.winfo_children():
                widget.destroy()
            toRemove = []
            idFrame = Frame(record)
            idFrame.pack(side="top", fill=X)
            Label(idFrame, text="Student ID: "+id).pack(side="left") #ID cannot be changed

            nameFrame = Frame(record)
            nameFrame.pack(side="top", fill=X, pady=5)
            Label(nameFrame, text="Student name: ").pack(side="left")
            nameBox = Text(nameFrame, height=1, width=20)
            nameBox.pack(side="left", padx=5)
            nameBox.insert('1.0', record2[1])

            ageFrame = Frame(record)
            ageFrame.pack(side="top", fill=X, pady=5)
            Label(ageFrame, text="Student age: ").pack(side="left")
            ageBox = Text(ageFrame, height=1, width=20)
            ageBox.pack(side="left", padx=5)
            ageBox.insert('1.0', record2[2])

            emailFrame = Frame(record)
            emailFrame.pack(side="top", fill=X, pady=5)
            Label(emailFrame, text="Student email: ").pack(side="left")
            emailBox = Text(emailFrame, height=1, width=25)
            emailBox.pack(side="left", padx=5)
            emailBox.insert('1.0', record2[3])

            cursor.execute("SELECT course_id FROM registered_courses WHERE student_id=?", (id,))
            data = cursor.fetchall()
            coursesFrame = Frame(record)
            coursesFrame.pack(side="top", fill=X, pady=5)
            Label(coursesFrame, text="Student courses: ").pack(side="left")
            remainingCourses = ttk.Combobox(coursesFrame, values=[x[0] for x in data], width=30, state="readonly")
            remainingCourses.pack(side="left", padx=5)
            Button(coursesFrame, text="X", command=lambda:removeFromList(remainingCourses.get())).pack(side="left")
            fields = [nameBox, ageBox, emailBox, remainingCourses]
        
    elif category == "Instructor Records":
        cursor.execute("SELECT * FROM instructors WHERE instructor_id=?", (id,))
        record2 = cursor.fetchone()
        if record2 is None:
            messagebox.showerror("ERROR", "Instructor ID " + id + " does not exist!")
            return
        else:
            object_to_modify = ("Instructor", id)
            for widget in record.winfo_children():
                widget.destroy()

            idFrame = Frame(record)
            idFrame.pack(side="top", fill=X)
            Label(idFrame, text="Instructor ID: "+id).pack(side="left") #ID cannot be changed

            nameFrame = Frame(record)
            nameFrame.pack(side="top", fill=X, pady=5)
            Label(nameFrame, text="Instructor name: ").pack(side="left")
            nameBox = Text(nameFrame, height=1, width=20)
            nameBox.pack(side="left", padx=5)
            nameBox.insert('1.0', record2[1])

            ageFrame = Frame(record)
            ageFrame.pack(side="top", fill=X, pady=5)
            Label(ageFrame, text="Instructor age: ").pack(side="left")
            ageBox = Text(ageFrame, height=1, width=20)
            ageBox.pack(side="left", padx=5)
            ageBox.insert('1.0', record2[2])

            emailFrame = Frame(record)
            emailFrame.pack(side="top", fill=X, pady=5)
            Label(emailFrame, text="Instructor email: ").pack(side="left")
            emailBox = Text(emailFrame, height=1, width=25)
            emailBox.pack(side="left", padx=5)
            emailBox.insert('1.0', record2[3])
            fields = [nameBox, ageBox, emailBox]

    elif category == "Course Records":
        cursor.execute("SELECT * FROM courses WHERE course_id=?", (id,))
        record2 = cursor.fetchone()
        if record2 is None:
            messagebox.showerror("ERROR", "Course ID " + id + " does not exist!")
            return
        else:
            object_to_modify = ("Course", id, record2[2])

            for widget in record.winfo_children():
                widget.destroy()

            idFrame = Frame(record)
            idFrame.pack(side="top", fill=X)
            Label(idFrame, text="Course ID: "+id).pack(side="left") #ID cannot be changed

            nameFrame = Frame(record)
            nameFrame.pack(side="top", fill=X, pady=5)
            Label(nameFrame, text="Course name: ").pack(side="left")
            nameBox = Text(nameFrame, height=1, width=20)
            nameBox.pack(side="left", padx=5)
            nameBox.insert('1.0', record2[1])

            instructorFrame = Frame(record)
            instructorFrame.pack(side="top", fill=X, pady=5)
            Label(instructorFrame, text="Instructor ID: ").pack(side="left")
            instructorBox = Text(instructorFrame, height=1, width=20)
            instructorBox.pack(side="left", padx=5)
            if record2[2] is not None:
                instructorBox.insert('1.0', record2[2])
            fields = [nameBox, instructorBox]
    return

def editAndSave():
    """
    This function is responsible to update the record's data. It will first validate that all the data is in a valid format before ssubmitting the update to the database.
    The function takes no parameter, the data is directly extracted from the fields present on the window and the record to update is recognized through the object_to_modify tuple
    which indicates the type of record to modify (i.e. what table(s) to perform the update on) and the id of the record.
    
    Returns:
        :return: none
    """
    global object_to_modify, fields, toRemove
    if object_to_modify[0] == "Student":
        try:
            int(fields[1].get(1.0, 'end-1c'))
        except:
            messagebox.showerror("ERROR", "Invalid data type! Age must be an integer!")
            return
        cursor.execute("UPDATE students SET name=?, age=?, email=? WHERE student_id=?", (fields[0].get(1.0, 'end-1c'), int(fields[1].get(1.0, 'end-1c')), fields[2].get(1.0, 'end-1c'), object_to_modify[1],))
        conn.commit()

        for x in toRemove:
            cursor.execute("DELETE FROM registered_courses WHERE student_id=? AND course_id=?", (object_to_modify[1], x,))
            conn.commit()
    elif object_to_modify[0] == "Instructor":
        try:
            int(fields[1].get(1.0, 'end-1c'))
        except:
            messagebox.showerror("ERROR", "Invalid data type! Age must be an integer!")
            return
        cursor.execute("UPDATE instructors SET name=?, age=?, email=? WHERE instructor_id=?", (fields[0].get(1.0, 'end-1c'), int(fields[1].get(1.0, 'end-1c')), fields[2].get(1.0, 'end-1c'), object_to_modify[1],))
        conn.commit()
    elif object_to_modify[0] == "Course":
        try:
            if fields[1].get(1.0, 'end-1c') == "":
                cursor.execute("UPDATE courses SET name=?, instructor_id=? WHERE course_id=?", (fields[0].get(1.0, 'end-1c'), None, object_to_modify[1]))
            else:
                cursor.execute("UPDATE courses SET name=?, instructor_id=? WHERE course_id=?", (fields[0].get(1.0, 'end-1c'), fields[1].get(1.0, 'end-1c'), object_to_modify[1]))
            conn.commit()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("ERROR", "Instructor with ID " + fields[1].get(1.0, 'end-1c') + " does not exist! Course will be unassigned.")
            cursor.execute("UPDATE courses SET name=?, instructor_id=? WHERE course_id=?", (fields[0].get(1.0, 'end-1c'), None, object_to_modify[1]))
            conn.commit()
        
    object_to_modify = None
    fields = None
    toRemove = []
    for widget in record.winfo_children():
        widget.destroy()
    treeview.delete(*treeview.get_children())
    fillTreeview()
    return

#frame in which we choose the type of record to modify (student, instructor, course)
edit = Frame(editTab, height=30)
edit.pack(side="top", padx=3,pady=5, fill=X)
Label(edit, text="Edit:").pack(side="left", padx=3)
editBox = ttk.Combobox(edit, values=["Student Records", "Instructor Records" , "Course Records"], width=30, state="readonly")
editBox.pack(side="left")
editBox.bind("<<ComboboxSelected>>", changeLabel)
object_to_modify = None
fields = None
toRemove = []

#frame to search for specific record according to ID (must enter the full ID)
searchFrame = Frame(editTab, height=30)
searchFrame.pack(side="top", padx=3,pady=5, fill=X)
label = Label(searchFrame, text="Enter ID:")
label.pack(side="left", padx=3)
editIdBox = Text(searchFrame, height=1, width=22)
editIdBox.pack(side="left", padx=3)
Button(searchFrame, text="Search", relief="raised", command=lambda: lookFor(editIdBox.get(1.0, "end-1c"), editBox.get())).pack(side="left")

#frame to display record information
record = Frame(editTab, highlightbackground='black', highlightthickness=1)
record.pack(side='top', padx=5, pady=5, fill=X)

tempEdit = Frame(editTab)
tempEdit.pack(side="top", fill=X)
Button(tempEdit, text="Edit and Save", relief="raised", command=lambda:editAndSave()).pack(side="left", padx=5)

#Search and Filter
#function to change the filter according to the search category
def changeFilters(e):
    """
    This function will simply modify the options in the attributesBox drop down list when changing the type of record we are searching in as each category has different filters
    
    Returns:
        :return: none
    """
    attributesBox.set("")
    if categoryBox.get() == "Students":
        attributesBox['values'] = ['ID', 'Name', 'Age', 'Email', 'Course enrolled']
    elif categoryBox.get() == "Instructors":
        attributesBox['values'] = ['ID', 'Name', 'Age', 'Email']
    elif categoryBox.get() == "Courses":
        attributesBox['values'] = ['ID', 'Name', 'Instructor']
    else:
        attributesBox['values'] = []

#function responsible to search for the records that matches the passed keyword according to the attribute and category selected
def search(category, attribute, keyword):
    """
    Function responsible to search for the records that matches the passed keyword according to the attribute and category selected. Records displayed in a tabular format.
    
    Args:
        type category: str
        category: the type of record we are looking for (student, instructor, or course)
        type attribute: str
        attribute: the filter used for searching, different options for each category
        type keyword: str
        keyword: keyword to be looked for in the specified table. We search for the records where the field contains the keyword but is not necessarilly equal to it

    Returns:
        :return: none  
    """
    if attribute!="Age":
        keyword = keyword.lower()
    rows = []
    if category == "":
        messagebox.showerror("ERROR", "No category selected!")
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
                messagebox.showerror("ERROR", "Invalid data type passed! Must be integer!")
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
                messagebox.showerror("ERROR", "Invalid data type passed! Must be integer!")
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
    
    for widget in results.winfo_children(): #deleting all the previously displayed rows
        widget.destroy()
    
    for i in range(len(rows[0])): # displaying all the new rows
        tempFrame = Frame(results)
        tempFrame.pack(side="left", fill=Y)
        for j in range(len(rows)):
            # the table consist of text boxes with a disabled state
            if rows[0][i] == "Email" or rows[0][i] == "Course Name":
                t = Text(tempFrame, height=1, width=30) #giving these text boxes a greater width as their content tend to be bigger
            else:
                t = Text(tempFrame, height=1, width=15)
            t.pack(side="top")
            t.insert("1.0", rows[j][i])
            t['state'] = "disabled" 
    

#Choosing whether to search in students, instructors, or courses records
categories = Frame(searchTab, height=30)
categories.pack(side="top", padx=3,pady=5, fill=X)
Label(categories, text="Search by:").pack(side="left", padx=3)
categoryBox = ttk.Combobox(categories, values=["Students", "Instructors" , "Courses"], width=30, state="readonly")
categoryBox.pack(side="left")
categoryBox.bind("<<ComboboxSelected>>", changeFilters)

#Filtering data according to specific attributes for each entity
attributes = Frame(searchTab, height=30, highlightbackground='black', highlightthickness=1)
attributes.pack(side="top", padx=3, pady=5, fill=X)
Label(attributes, text="Filter by:").pack(side="left", padx=3, pady=5)
attributesBox = ttk.Combobox(attributes, values=[], width=30, state="readonly")
attributesBox.pack(side="left", pady=5)
Label(attributes, text="Keyword:").pack(side="left", padx=3)
keyword = Text(attributes, height=1, width=22)
keyword.pack(side="left", pady=5)
Button(attributes, text="Search", width=10, relief="raised", command=lambda: search(categoryBox.get(), attributesBox.get(), keyword.get(1.0, "end-1c"))).pack(side="left", padx=3, pady=5)

#creating a scrollable area to display the search results
def on_frame_configure(event):
    # Reset the scroll region to encompass the inner frame
    canvas.configure(scrollregion=canvas.bbox("all"))
resultFrame = Frame(searchTab, width=440, height=30, highlightbackground='black', highlightthickness=1)
resultFrame.pack(side="top", fill=BOTH, expand=True, padx=3, pady=5)
canvas = Canvas(resultFrame)
canvas.pack(side="left", fill=BOTH, expand=True)
scrollbar = Scrollbar(resultFrame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side="right", fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

results = Frame(canvas, width=590)
canvas.create_window((0, 0), window=results, anchor="nw")
results.bind("<Configure>", on_frame_configure)

#Displaying all records in a treeview
def fillTreeview(): # this function can be used to reset the treeview when data is added/modified
    """
    this function is used to build the tree view
    
    Returns:
        :return: none
    """
    students = treeview.insert("", END, text="Students") #adding all students info
    cursor.execute("SELECT * FROM students")
    for x in cursor.fetchall():
        temp_row = treeview.insert(students, END, text=x[0]) #show ids first as they are unique to each student
        treeview.insert(temp_row, END, text="Name: "+ x[1]) #student's name
        treeview.insert(temp_row, END, text="Age: "+ str(x[2])) #student's age
        treeview.insert(temp_row, END, text="Email: "+ x[3]) #student's email
        cursor.execute("SELECT course_id FROM registered_courses WHERE student_id=?", (x[0],))
        coursesRegistered = treeview.insert(temp_row, END, text="Registered Courses") #student's courses
        for y in cursor.fetchall():
            treeview.insert(coursesRegistered, END, text=y[0])

    instructors = treeview.insert("", END, text="Instructors")
    cursor.execute("SELECT * FROM instructors")
    for z in cursor.fetchall():
        temp_row2 = treeview.insert(instructors, END, text=z[0]) #show ids first as they are unique to each instructor
        treeview.insert(temp_row2, END, text="Name: "+ z[1]) #instructor's name
        treeview.insert(temp_row2, END, text="Age: "+ str(z[2])) #instructor's age
        treeview.insert(temp_row2, END, text="Email: "+ z[3]) #instructor's email
        coursesAssigned = treeview.insert(temp_row2, END, text="Assigned Courses") #instructor's courses
        cursor.execute("SELECT course_id FROM courses WHERE instructor_id=?", (z[0], ))
        for t in cursor.fetchall():
            treeview.insert(coursesAssigned, END, text=t[0])

    courses = treeview.insert("", END, text="Courses")
    cursor.execute("SELECT courses.course_id, courses.name, courses.instructor_id, instructors.name FROM courses LEFT JOIN instructors ON courses.instructor_id=instructors.instructor_id")
    for s in cursor.fetchall(): 
        temp_row3 = treeview.insert(courses, END, text=s[0]) #show course ID first as it should be unique
        treeview.insert(temp_row3, END, text="Name: " + s[1]) # course name
        if s[2] is not None:
            treeview.insert(temp_row3, END, text="Instructor ID: " + s[2]) # course instructor ID
            treeview.insert(temp_row3, END, text="Instructor Name: " + s[3]) # course instructor name
        else:
            treeview.insert(temp_row3, END, text="Instructor ID: TBA")
            treeview.insert(temp_row3, END, text="Instructor Name: TBA")
        
        enrolledStudents = treeview.insert(temp_row3, END, text="Enrolled students")
        cursor.execute("SELECT student_id FROM registered_courses WHERE course_id=?", (s[0],))
        for i in cursor.fetchall():
            treeview.insert(enrolledStudents, END, text=i[0])
    treeview.pack(fill=BOTH, expand=True)

treeview = ttk.Treeview(displayTab) #creating the treeview
fillTreeview()

#Assign courses to instructors
def assign(instructor_id, course):
    """
    this function is responsible of assigning an instructor to a course by updating the instructor field in the courses table.
    
    Args:
        type instructor_id: str
        instructor_id: id of the instructor to assign the course to
        type course: str
        course: id of the course we want to assign teh instructor to  
    
    Returns:
        :return: none
    """
    if instructor_id=="":
        return
    course = course.split(" : ")[0]
    try:
        cursor.execute("SELECT instructor_id FROM courses WHERE course_id=?", (course,))
        if cursor.fetchone()[0] is None:
            cursor.execute("UPDATE courses SET instructor_id=? WHERE course_id=?", (instructor_id, course))
            conn.commit()
        else:
            messagebox.showwarning("WARNING", "Course "+course+ " is already assigned!")
            return
    except sqlite3.IntegrityError as e:
        messagebox.showerror("ERROR", "Instructor ID "+instructor_id+ " does not exist!")
        return

    coursesBox.set("")
    treeview.delete(*treeview.get_children())
    fillTreeview()        
    return

top_box = Frame(assignCoursesTab, width=440, height=30, relief='raised', highlightbackground='black', highlightthickness=1)
top_box.pack(side="top", padx=3,pady=3, fill=X)
Label(top_box, text="Enter your instructor ID: ").pack(side="left", padx=5)
IDbox_instructors = Text(top_box, height=1, width=15) # box for instructor ID
IDbox_instructors.pack(side="left", padx=2, pady=2)

top_box2 = Frame(assignCoursesTab, width=440, height=30) # frame for drop down list and asssign button
top_box2.pack(side="top", padx=3,pady=3, fill=X)
coursesBox = ttk.Combobox(top_box2, values=courses, width=30, state="readonly") #drop down list of courses
coursesBox.pack(side="left", padx=8)
Button(top_box2, text="Assign Course", relief="raised", command=lambda: assign(IDbox_instructors.get(1.0, "end-1c"), coursesBox.get())).pack(side="left")

#Register courses for students
def register(student_id, course):
    """
    this function is responsible of registering a student to a course by adding a row to the registered_courses table consisting of the student id and the course id.
    
    Args:
        type student_id: str
        student_id: id of the student
        type course: str
        course: id of the course   
    
    Returns:
        :return: none
    """
    course = course.split(" : ")[0]
    try:
        cursor.execute("INSERT INTO registered_courses VALUES(?, ?)", (student_id, course))
        conn.commit()
    except sqlite3.IntegrityError as e:
        cursor.execute("SELECT * FROM registered_courses WHERE student_id=? AND course_id=?", (student_id, course))
        if len(cursor.fetchall())>=1:
            messagebox.showerror("ERROR", "Student with ID "+student_id+" is already enrolled in the course "+course+"!")
        else:
            messagebox.showerror("ERROR", "Student with ID "+student_id+" does not exist!")
        return
    
    courseBox.set("")
    treeview.delete(*treeview.get_children())
    fillTreeview()
    return

#input box for user ID. We assume that user's ID are unique and enough to distinguish between students
temp = Frame(registerCoursesTab, width=440, height=30, relief='raised', highlightbackground='black', highlightthickness=1)
temp.pack(side="top", padx=3,pady=3, fill=X)
Label(temp, text="Enter your student ID: ").pack(side="left", padx=5)
IDbox = Text(temp, height=1, width=15) # box for student ID
IDbox.pack(side="left", padx=2, pady=2)

temp2 = Frame(registerCoursesTab, width=440, height=30) # frame for drop down list and register button
temp2.pack(side="top", padx=3,pady=3, fill=X)
courseBox = ttk.Combobox(temp2, values=courses, width=30, state="readonly") #drop down list of courses
courseBox.pack(side="left", padx=8)
Button(temp2, text="Register Course", relief="raised", command=lambda: register(IDbox.get(1.0, "end-1c"), courseBox.get())).pack(side="left")

#Adding students, instructors, and courses tab
def add_something(something):
    """
    function responsible of adding a student, instructor, or course to the database. The data iss directly extracted from the fields on the window.
    
    Args:
        type something: str
        something: record type we want to add (student, instructor, or course)
        

    Returns:
        :return: none
    """
    if something=="student":
        #verifying validity of inputs
        try:
            try:
                int(sAge.get(1.0, "end-1c"))
            except:
                messagebox.showerror("ERROR", "Invalid data type! Age must be an integer!")
                return
            if sID.get(1.0, "end-1c") == "" or sName.get(1.0, "end-1c")=="" or int(sAge.get(1.0, "end-1c"))<=0 or sEmail.get(1.0, "end-1c")=="" or '@' not in sEmail.get(1.0, "end-1c"):
                messagebox.showerror("ERROR", "Missing or invalid fields")
                return
            conn.execute("INSERT INTO students VALUES(?, ?, ?, ?)", (sID.get(1.0, "end-1c"), sName.get(1.0, "end-1c"), sAge.get(1.0, "end-1c"), sEmail.get(1.0, "end-1c")))
        except sqlite3.IntegrityError as e:
            messagebox.showerror("ERROR", "Entered student ID already exists!")
            return
        
        sID.delete('1.0', "end") #clearing the entry boxes
        sName.delete('1.0', "end")
        sAge.delete('1.0', "end")
        sEmail.delete('1.0', "end")

    elif something == "instructor":
        #verifying validity of inputs
        try:
            try:
                int(iAge.get(1.0, "end-1c"))
            except:
                messagebox.showerror("ERROR", "Invalid data type! Age must be an integer!")
                return
            if iID.get(1.0, "end-1c") == "" or iName.get(1.0, "end-1c")=="" or int(iAge.get(1.0, "end-1c"))<=0 or iEmail.get(1.0, "end-1c")=="" or '@' not in iEmail.get(1.0, "end-1c"):
                messagebox.showerror("ERROR", "Missing or invalid fields")
                return

            conn.execute("INSERT INTO instructors VALUES(?, ?, ?, ?)", (iID.get(1.0, "end-1c"), iName.get(1.0, "end-1c"), iAge.get(1.0, "end-1c"), iEmail.get(1.0, "end-1c")))
        except sqlite3.IntegrityError as e:
            messagebox.showerror("ERROR", "Entered instructor ID already exists!")
            return
        
        iID.delete('1.0', "end") #clearing the entry boxes
        iName.delete('1.0', "end")
        iAge.delete('1.0', "end")
        iEmail.delete('1.0', "end")
    else:
        #verifying validity of inputs
        if cID.get(1.0, "end-1c") == "" or cName.get(1.0, "end-1c")=="":
            messagebox.showwarning("WARNING", "Missing field")
            return "Missing field"

        try:
            conn.execute("INSERT INTO courses VALUES(?, ?, ?)", (cID.get(1.0, "end-1c"), cName.get(1.0, "end-1c"), None))
        except sqlite3.IntegrityError as e:
            messagebox.showerror("ERROR", "Entered course ID already exists!")
            return
        
        # updating the list of courses presented in other tabs
        courses.append(cID.get(1.0, "end-1c") + " : " + cName.get(1.0, "end-1c"))
        courseBox['values'] = courses
        coursesBox['values'] = courses
        coursesBox.set("")
        courseBox.set("")
        # clearing the input boxes
        cID.delete('1.0', "end")
        cName.delete('1.0', "end")
    conn.commit()
    treeview.delete(*treeview.get_children())
    fillTreeview()
    return

frame1 = Frame(addStuffTab, width=145, height=330, relief='raised', highlightbackground='black', highlightthickness=2)
frame2 = Frame(addStuffTab, width=145, height=330, relief='raised', highlightbackground='black', highlightthickness=2)
frame3 = Frame(addStuffTab, width=145, height=330, relief='raised', highlightbackground='black', highlightthickness=2)

frame1.pack(side="left", fill=BOTH, expand=True, padx=5, pady=5)
frame2.pack(side="left", fill=BOTH, expand=True, padx=5, pady=5)
frame3.pack(side="left", fill=BOTH, expand=True, padx=5, pady=5)

#Student frame
Label(frame1, text="Student info").pack(side="top",pady=5)

Label(frame1, text="Enter student ID:").pack(side="top", fill=X)
sID = Text(frame1, height=1, width=16)
sID.pack(side="top", padx=2, pady=2)

Label(frame1, text="Enter student name:").pack(side="top", fill=X)
sName = Text(frame1, height=1, width=16)
sName.pack(side="top", padx=2, pady=2)

Label(frame1, text="Enter student age:").pack(side="top", fill=X)
sAge = Text(frame1, height=1, width=16)
sAge.pack(side="top", padx=2, pady=2)

Label(frame1, text="Enter student email:").pack(side="top", fill=X)
sEmail = Text(frame1, height=1, width=16)
sEmail.pack(side="top", padx=2, pady=5)

Button(frame1, text="Add student", relief="raised", command=lambda: add_something("student")).pack(side="bottom", pady=15)

#Instructor frame
Label(frame2, text="Instructor info").pack(side="top", pady=5)

Label(frame2, text="Enter instructor ID:").pack(side="top", fill=X)
iID = Text(frame2, height=1, width=16)
iID.pack(side="top", padx=2, pady=2)

Label(frame2, text="Enter instructor name:").pack(side="top", fill=X)
iName = Text(frame2, height=1, width=16)
iName.pack(side="top", padx=2, pady=2)

Label(frame2, text="Enter instructor age:").pack(side="top", fill=X)
iAge = Text(frame2, height=1, width=16)
iAge.pack(side="top", padx=2, pady=2)

Label(frame2, text="Enter instructor email:").pack(side="top", fill=X)
iEmail = Text(frame2, height=1, width=16)
iEmail.pack(side="top", padx=2, pady=5)

Button(frame2, text="Add instructor", relief="raised", command=lambda: add_something("instructor")).pack(side="bottom", pady=15)

#Course frame
Label(frame3, text="Course info").pack(side="top", pady=5)

Label(frame3, text="Enter course ID:").pack(side="top", fill=X)
cID = Text(frame3, height=1, width=16)
cID.pack(side="top", padx=2, pady=2)

Label(frame3, text="Enter course name:").pack(side="top", fill=X)
cName = Text(frame3, height=1, width=16)
cName.pack(side="top", padx=2, pady=2)

Button(frame3, text="Add course", relief="raised", command=lambda: add_something("course")).pack(side="bottom", pady=15)

root.mainloop()
