import json
from tkinter import messagebox

class Person(object):
    """
    This is a simple class representing a person. It is used as a super class for the Student and Instructor classes.
    
    Args:
        type name: str
        name: name of the person
        type age: int, must be positive
        age: age of the person
        type email: str, must contain @ character
        email: email address of the person
    """
    def __init__(self, name, age, email):
        """
        Constructor method for the person object
        """
        assert type(name)==str and type(age) == int and age>0 and type(email)==str and '@' in email, "Invalid inputs"
        self.name = name
        self.age = age
        self._email = email
    
    def introduce(self):
        """
        Returns a string in which the person tells her name and age
        """
        print(f"Hello, I am {self.name} and I am {self.age} years old")

class Student(Person):
    """
    This a class used to represent a student. It inherits the basic attributes and methods of a student from the :class:`Person`
    Args:
        type id: str 
        id: id of the student
        type name: str
        name: name of the student
        type age: int, must be positive
        age: age of the student
        type email: str, must contain @ character
        email: email address of the student
    """
    def __init__(self, id, name, age, email):
        """
        Constructor method for the student class
        """
        assert type(id) == str and type(name)== str and type(age) == int and age>0 and type(email)==str and '@' in email, "Invalid inputs"
        self.student_id = id
        self.registered_courses = []
        Person.__init__(self, name, age, email)
    
    def register_course(self, course):
        """
        Method used to register a student in a course
        
        Args:
            type course: :class:`Course`
            course: course to which the student want to register
        """
        assert type(course) == Course, 'Invalid class. Must be a Course class.'
        self.registered_courses.append(course)
        course.add_student(self)

class Instructor(Person):
    """
    This a class used to represent a instructor. It inherits the basic attributes and methods of a instructor from the :class:`Person`
    Args:
        type id: str 
        id: id of the instructor
        type name: str
        name: name of the instructor
        type age: int, must be positive
        age: age of the instructor
        type email: str, must contain @ character
        email: email address of the instructor
    """
    def __init__(self, id, name, age, email):
        """
        Constructor method for the instructor class
        """
        assert type(id) == str and type(name)== str and type(age) == int and age>0 and type(email)==str and '@' in email, "Invalid inputs"
        self.instructor_id = id
        self.assigned_courses = []
        Person.__init__(self, name, age, email)
    
    def assign_course(self, course):
        """
        Method used to assign the instructor to a course
        Args:
            type course: :class:`Course`
            course: course to which the instructor is assigned to
            
        """
        assert type(course) == Course, 'Invalid class. Must be a Course class.'
        self.assigned_courses.append(course)
        course.instructor = self

class Course(object):
    """
    This is a class used to represent a course.
    Args:
        type id: str
        id: id of the course
        type name: str
        name: name of the course
    """
    def __init__(self, id, name):
        assert type(id) == str and type(name)== str, 'All parameters must be of string type'
        self.course_id = id
        self.course_name = name
        self.instructor = None
        self.enrolled_student = []
    
    def add_student(self, student):
        """
        function used to add a student to the list of enrolled student
        
        Args:
            type student: `:class:Student`
            student: student that wants to get enrolled in the course

        Returns:   
            :return: None
        """
        assert type(student) == Student, "Invalid class. Must be a Student class."
        self.enrolled_student.append(student)

# Step 2
class School(object):
    """
    This is a complex class used to represent an entire school. It makes use of the simple classes `:class:Student`, `:class:Instructor`, `:class:Course`
    
    Args:
        type json_file: str, defaults to empty string
        json_file: the location of the json file to load the data from into the class
    """
    def __init__(self,json_file=""):
        """
        constructor method for the School class. Takes the data from the json file (if selected) and loads it into distinct lists for Students, Instructors, and Courses
        """
        if json_file != "" and json_file[-5:] != ".json":
            json_file = ""
            print("Wrong file extension entered. Will save data to another file")
        self.students = []
        self.instructors = []
        self.courses = []
        self.fileName = json_file
        if json_file != "":
            with open(json_file, 'r') as open_file:
                data = json.load(open_file)
            

            for z in data['instructors']:
                self.instructors.append(Instructor(z['id'], z['name'], z['age'], z['email']))
            
            for y in data['courses']:
                self.courses.append(Course(y['id'], y['name']))
                if y['instructor_id'] != "":
                    for i in self.instructors:
                        if i.instructor_id == y['instructor_id']:
                            i.assign_course(self.courses[-1])
                            break
            
            for x in data['students']:
                self.students.append(Student(x['id'], x['name'], x['age'], x['email']))
                for i in x['courses']:
                    for j in self.courses:
                        if i == j.course_id:
                            self.students[-1].register_course(j)
                            break
    
    def save_to_json(self):
        """
        Saves any modified data into the json file. If json file specified at the start, data will be saved into it, otherwise, data will be saved in output_file.json file.
        
        Returns:
            :return: None
        """
        data = {}
        data['students'] = []
        for i in self.students:
            temp = {}
            temp['id'] = i.student_id
            temp['name'] = i.name
            temp['age'] = i.age
            temp['email'] = i._email
            temp['courses'] = [x.course_id for x in i.registered_courses]
            data['students'].append(temp)
        
        data['instructors'] = []
        for j in self.instructors:
            temp = {}
            temp['id'] = j.instructor_id
            temp['name'] = j.name
            temp['age'] = j.age
            temp['email'] = j._email
            data['instructors'].append(temp)
        
        data['courses'] = []
        for k in self.courses:
            temp = {}
            temp['id'] = k.course_id
            temp['name'] = k.course_name
            if k.instructor is not None:
                temp['instructor_id'] = k.instructor.instructor_id
            else:
                temp['instructor_id'] = ""
            data['courses'].append(temp)
        
        json_data = json.dumps(data)

        if self.fileName != "":
            with open(self.fileName, 'w') as output:
                output.write(json_data)
        else:
            with open("output_file.json", 'w') as output:
                output.write(json_data)
        print("operation successful")

    def add_student_to_school(self, id, name, age, email):
        """
        Adds a student to the school system. Performs necessary checks on the inputs. Creates a `:class:Student` object to store the data in it then places it in the students list
        
        Args:
            type id: str
            id: id of the student
            type name: str
            name: name of the student
            type age: int, must be positive
            age: age of the student
            type email: str, must contain @ character
            email: email address of the student
        
        Returns:
            :return: the created student
            :rtype: `:class:Student`
        """
        try:
            age = int(age)
            if id == "" or name == "" or email == "" or '@' not in email:
                messagebox.showwarning("WARNING", "Invalid or missing fields!")
                return
        except Exception as e:
            messagebox.showwarning("Entered age is not a number")
            return "Age is not an integer"
        for x in self.students:
            if x.student_id == id:
                messagebox.showwarning("WARNING", "Student with ID " + id + " already exists!")
                return
        self.students.append(Student(id, name, age, email))
        print(self.students[-1].name, self.students[-1].student_id)
        return self.students[-1]
    
    def add_instructor_to_school(self, id, name, age, email):
        """
        Adds an instructor to the school system. Performs necessary checks on the inputs. Creates a `:class:Instructor` object to store the data in it then places it in the instructors list
        Args:
            type id: str
            id: id of the instructor
            type name: str 
            name: name of the instructor
            type age: int, must be positive
            age: age of the instructor
            type email: str, must contain @ character
            email: email address of the instructor

        Returns:   
            :return: the created instructor
            :rtype: `:class:Instructor`
        """
        try:
            age = int(age)
            if id == "" or name == "" or email == "" or '@' not in email:
                messagebox.showwarning("WARNING", "Invalid or missing fields!")
                return
        except Exception as e:
            messagebox.showwarning("WARNING", "Entered age is not a number")
            return "Age is not an integer"
        for x in self.instructors:
            if x.instructor_id == id:
                messagebox.showwarning("WARNING", "Instructor with ID " + id + " already exists!")
                return
        self.instructors.append(Instructor(id, name, age, email))
        print(self.instructors[-1].name, self.instructors[-1].instructor_id)
        return self.instructors[-1]
    
    def add_course_to_school(self, id, name):
        """
        Adds a course to the school system. Performs necessary checks on the inputs. Creates a `:class:Course` object to store the data in it then places it in the courses list
        
        Args:
            type id: str 
            id: id of the course
            type name: str
            name: name of the course
        
        Returns:
            :return: the created course
            :rtype: `:class:Course`
        """
        if id == "" or name == "":
            messagebox.showwarning("WARNING", "Missing field")
            return "Missing field"
        for x in self.courses:
            if x.course_id == id:
                messagebox.showwarning("WARNING", "Course with ID " + id + " already exists!")
                return
        self.courses.append(Course(id, name))
        print(self.courses[-1].course_name, self.courses[-1].course_id)
        return self.courses[-1]

