#for this part, we assume that IDs are unique

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from classes import School
import classes

my_school = School(filedialog.askopenfilename())

root = Tk()
root.title("School Management System")
root.geometry("640x350")
root.configure(background="#c9c8c7")

# list of already existing courses
courses = [x.course_id + " : " + x.course_name for x in my_school.courses] # will be used many times later

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
    object_to_delete = None
    if category=="Student Records":
        found = False
        for x in my_school.students:
            if x.student_id == id:
                object_to_delete = x
                found=True
                break
        if not found:
            messagebox.showerror("ERROR", "Student ID " + id + " does not exist!")
            return
        else:
            if messagebox.askyesno("Delete Record", "Are you sure you want to delete this record"):
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
            messagebox.showerror("ERROR", "Instructor ID " + id + " does not exist!")
            return
        else:
            if messagebox.askyesno("Delete Record", "Are you sure you want to delete this record"):
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
            messagebox.showerror("ERROR", "Course ID " + id + " does not exist!")
            return
        else:
            if messagebox.askyesno("Delete Record", "Are you sure you want to delete this record"):
                for z in object_to_delete.enrolled_student:
                    z.registered_courses.remove(object_to_delete)
                object_to_delete.instructor.assigned_courses.remove(object_to_delete)
                my_school.courses.remove(object_to_delete)
    my_school.save_to_json()
    treeview.delete(*treeview.get_children())
    fillTreeview()
    return

def changeLabel2(e):
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
    if editBox.get()=="Student Records":
        label.config(text="Enter student ID:")
    elif editBox.get()=="Instructor Records":
        label.config(text="Enter instructor ID:")
    elif editBox.get()=="Course Records":
        label.config(text="Enter course ID:")
    else:
        label.config(text="Enter ID:")

def removeFromList(courseID):
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
    global object_to_modify, fields, toRemove
    
    if category=="Student Records":
        found = False
        for x in my_school.students:
            if x.student_id == id:
                object_to_modify = x
                found=True
                break
        if not found:
            messagebox.showerror("ERROR", "Student ID " + id + " does not exist!")
            return
        else:
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
            nameBox.insert('1.0', object_to_modify.name)

            ageFrame = Frame(record)
            ageFrame.pack(side="top", fill=X, pady=5)
            Label(ageFrame, text="Student age: ").pack(side="left")
            ageBox = Text(ageFrame, height=1, width=20)
            ageBox.pack(side="left", padx=5)
            ageBox.insert('1.0', object_to_modify.age)

            emailFrame = Frame(record)
            emailFrame.pack(side="top", fill=X, pady=5)
            Label(emailFrame, text="Student email: ").pack(side="left")
            emailBox = Text(emailFrame, height=1, width=25)
            emailBox.pack(side="left", padx=5)
            emailBox.insert('1.0', object_to_modify._email)

            coursesFrame = Frame(record)
            coursesFrame.pack(side="top", fill=X, pady=5)
            Label(coursesFrame, text="Student courses: ").pack(side="left")
            remainingCourses = ttk.Combobox(coursesFrame, values=[x.course_id for x in object_to_modify.registered_courses], width=30, state="readonly")
            remainingCourses.pack(side="left", padx=5)
            Button(coursesFrame, text="X", command=lambda:removeFromList(remainingCourses.get())).pack(side="left")
            fields = [nameBox, ageBox, emailBox, remainingCourses]
        
    elif category == "Instructor Records":
        found = False
        for x in my_school.instructors:
            if x.instructor_id == id:
                object_to_modify = x
                found=True
                break
        if not found:
            messagebox.showerror("ERROR", "Instructor ID " + id + " does not exist!")
            return
        else:
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
            nameBox.insert('1.0', object_to_modify.name)

            ageFrame = Frame(record)
            ageFrame.pack(side="top", fill=X, pady=5)
            Label(ageFrame, text="Instructor age: ").pack(side="left")
            ageBox = Text(ageFrame, height=1, width=20)
            ageBox.pack(side="left", padx=5)
            ageBox.insert('1.0', object_to_modify.age)

            emailFrame = Frame(record)
            emailFrame.pack(side="top", fill=X, pady=5)
            Label(emailFrame, text="Instructor email: ").pack(side="left")
            emailBox = Text(emailFrame, height=1, width=25)
            emailBox.pack(side="left", padx=5)
            emailBox.insert('1.0', object_to_modify._email)
            fields = [nameBox, ageBox, emailBox]

    elif category == "Course Records":
        found = False
        for x in my_school.courses:
            if x.course_id == id:
                object_to_modify = x
                found=True
                break
        if not found:
            messagebox.showerror("ERROR", "Course ID " + id + " does not exist!")
            return
        else:
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
            nameBox.insert('1.0', object_to_modify.course_name)

            instructorFrame = Frame(record)
            instructorFrame.pack(side="top", fill=X, pady=5)
            Label(instructorFrame, text="Instructor ID: ").pack(side="left")
            instructorBox = Text(instructorFrame, height=1, width=20)
            instructorBox.pack(side="left", padx=5)
            instructorBox.insert('1.0', object_to_modify.instructor.instructor_id)
            fields = [nameBox, instructorBox]
    return

def editAndSave():
    global object_to_modify, fields, toRemove
    if type(object_to_modify) == classes.Student:
        try:
            int(fields[1].get(1.0, 'end-1c'))
        except:
            messagebox.showerror("ERROR", "Invalid data type! Age must be an integer!")
            return
        object_to_modify.name = fields[0].get(1.0, 'end-1c')
        object_to_modify.age = int(fields[1].get(1.0, 'end-1c'))
        object_to_modify._email = fields[2].get(1.0, 'end-1c')
        for x in toRemove:
            for i in object_to_modify.registered_courses:
                if i.course_id == x:
                    i.enrolled_student.remove(object_to_modify)
                    object_to_modify.registered_courses.remove(i)
                    break
    elif type(object_to_modify) == classes.Instructor:
        try:
            int(fields[1].get(1.0, 'end-1c'))
        except:
            messagebox.showerror("ERROR", "Invalid data type! Age must be an integer!")
            return
        object_to_modify.name = fields[0].get(1.0, 'end-1c')
        object_to_modify.age = int(fields[1].get(1.0, 'end-1c'))
        object_to_modify._email = fields[2].get(1.0, 'end-1c')
    elif type(object_to_modify) == classes.Course:
        if fields[1].get(1.0, 'end-1c') != object_to_modify.instructor.instructor_id:
            object_to_modify.instructor.assigned_courses.remove(object_to_modify)
            if fields[1].get(1.0, 'end-1c') == "":
                object_to_modify.instructor = None
            else:
                found = False
                for x in my_school.instructors:
                    if x.instructor_id == fields[1].get(1.0, 'end-1c'):
                        object_to_modify.instructor = x
                        found = True
                        break
                if not found:
                    object_to_modify.instructor = None
                    messagebox.showerror("ERROR", "Instructor with ID " + fields[1].get(1.0, 'end-1c') + " does not exist! Course will be unassigned.")
        object_to_modify.course_name = fields[0].get(1.0, 'end-1c')
        

    my_school.save_to_json()
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
    if attribute!="Age":
        keyword = keyword.lower()
    rows = []
    if category == "":
        messagebox.showerror("ERROR", "No category selected!")
    elif category=="Students": #searching among students records
        rows.append(("ID", "Name", "Age", "Email"))
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
                    messagebox.showerror("ERROR", "Invalid data type passed! Must be integer!")
                    return
            elif attribute=="Course enrolled":
                for z in x.registered_courses:
                    if keyword in z.course_id.lower() or keyword in z.course_name.lower(): #giving the user the choice to search either by course ID or course Name
                        rows.append((x.student_id, x.name, x.age, x._email))
    elif category=="Instructors": #searching among instructor records
        rows.append(("ID", "Name", "Age", "Email"))
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
                    messagebox.showerror("ERROR", "Invalid data type passed! Must be integer!")
                    return
    elif category=="Courses": #searching among courses records
        rows.append(("Course ID", "Course Name", "Instructor"))
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
    students = treeview.insert("", END, text="Students") #adding all students info
    for x in my_school.students:
        temp_row = treeview.insert(students, END, text=x.student_id) #show ids first as they are unique to each student
        treeview.insert(temp_row, END, text="Name: "+ x.name) #student's name
        treeview.insert(temp_row, END, text="Age: "+ str(x.age)) #student's age
        treeview.insert(temp_row, END, text="Email: "+ x._email) #student's email
        coursesRegistered = treeview.insert(temp_row, END, text="Registered Courses") #student's courses
        for y in x.registered_courses:
            treeview.insert(coursesRegistered, END, text=y.course_id)

    instructors = treeview.insert("", END, text="Instructors")
    for z in my_school.instructors:
        temp_row2 = treeview.insert(instructors, END, text=z.instructor_id) #show ids first as they are unique to each instructor
        treeview.insert(temp_row2, END, text="Name: "+ z.name) #instructor's name
        treeview.insert(temp_row2, END, text="Age: "+ str(z.age)) #instructor's age
        treeview.insert(temp_row2, END, text="Email: "+ z._email) #instructor's email
        coursesAssigned = treeview.insert(temp_row2, END, text="Assigned Courses") #instructor's courses
        for t in z.assigned_courses:
            treeview.insert(coursesAssigned, END, text=t.course_id)

    courses = treeview.insert("", END, text="Courses") 
    for s in my_school.courses: 
        temp_row3 = treeview.insert(courses, END, text=s.course_id) #show course ID first as it should be unique
        treeview.insert(temp_row3, END, text="Name: " + s.course_name) # course name
        if s.instructor is not None:
            treeview.insert(temp_row3, END, text="Instructor ID: " + s.instructor.instructor_id) # course instructor ID
            treeview.insert(temp_row3, END, text="Instructor Name: " + s.instructor.name) # course instructor name
        else:
            treeview.insert(temp_row3, END, text="Instructor ID: TBA")
            treeview.insert(temp_row3, END, text="Instructor Name: TBA")
        
        enrolledStudents = treeview.insert(temp_row3, END, text="Enrolled students")
        for i in s.enrolled_student:
            treeview.insert(enrolledStudents, END, text=i.student_id)
    treeview.pack(fill=BOTH, expand=True)

treeview = ttk.Treeview(displayTab) #creating the treeview
fillTreeview()

#Assign courses to instructors
def assign(instructor_id, course):
    course = course.split(" : ")[0]
    instructor = None
    for x in my_school.instructors:
        if x.instructor_id == instructor_id:
            instructor = x
            break
    if instructor is None:
        messagebox.showerror("ERROR", "Instructor with ID " + instructor_id + " was not found!")
        coursesBox.set("")
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
                    coursesBox.set("")
                    treeview.delete(*treeview.get_children())
                    fillTreeview()
                    break
                else:
                    messagebox.showerror("ERROR", "The course " + course + " is already assigned to a professor")
                    coursesBox.set("")
                    return
    else:
        messagebox.showwarning("WARNING", "Instructor with ID " + instructor_id + " is already assigned to the course " + course)
        coursesBox.set("")        
    pass

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
Button(top_box2, text="Save Changes", relief="raised", command=lambda: my_school.save_to_json()).pack(side="right", padx=8)

#Register courses for students
def register(student_id, course):
    course = course.split(" : ")[0]
    student = None
    #looking for student with entered id
    for x in my_school.students:
        if x.student_id == student_id:
            student = x
            break
    if student is None:
        messagebox.showerror("ERROR", "Student with ID " + student_id + " was not found!")
        courseBox.set("")
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
        messagebox.showwarning("WARNING", "Student is already registered to the course " + course)
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
Button(temp2, text="Save Changes", relief="raised", command=lambda: my_school.save_to_json()).pack(side="right", padx=8)

#Adding students, instructors, and courses tab
def add_something(something):
    if something=="student":
        my_school.add_student_to_school(sID.get(1.0, "end-1c"), sName.get(1.0, "end-1c"), sAge.get(1.0, "end-1c"), sEmail.get(1.0, "end-1c"))
        sID.delete('1.0', "end")
        sName.delete('1.0', "end")
        sAge.delete('1.0', "end")
        sEmail.delete('1.0', "end")
    elif something == "instructor":
        my_school.add_instructor_to_school(iID.get(1.0, "end-1c"), iName.get(1.0, "end-1c"), iAge.get(1.0, "end-1c"), iEmail.get(1.0, "end-1c"))
        iID.delete('1.0', "end")
        iName.delete('1.0', "end")
        iAge.delete('1.0', "end")
        iEmail.delete('1.0', "end")
    else:
        my_school.add_course_to_school(cID.get(1.0, "end-1c"), cName.get(1.0, "end-1c"))
        # updating the list of courses presented in other tabs
        courses.append(cID.get(1.0, "end-1c") + " : " + cName.get(1.0, "end-1c"))
        courseBox['values'] = courses
        coursesBox['values'] = courses
        coursesBox.set("")
        courseBox.set("")
        # clearing the input boxes
        cID.delete('1.0', "end")
        cName.delete('1.0', "end")
    treeview.delete(*treeview.get_children())
    fillTreeview()
    pass

frame1 = Frame(addStuffTab, width=145, height=330, relief='raised', highlightbackground='black', highlightthickness=2)
frame2 = Frame(addStuffTab, width=145, height=330, relief='raised', highlightbackground='black', highlightthickness=2)
frame3 = Frame(addStuffTab, width=145, height=330, relief='raised', highlightbackground='black', highlightthickness=2)
frame4 = Frame(addStuffTab, width=440, height=20)
frame4.pack(side="bottom", fill=BOTH, expand=True)
Button(frame4, text="Save Changes", relief="raised", command=lambda: my_school.save_to_json()).pack(side="left", padx=5)

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
