import sqlite3

"""this script is responsible of creating all the tables in the database as well as defining all the primary and foreign keys"""

conn = sqlite3.connect('mySchool.db')
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

cursor.execute("CREATE TABLE if not exists students(student_id TEXT PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL, email TEXT NOT NULL);")
cursor.execute("CREATE TABLE if not exists instructors(instructor_id TEXT PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL, email TEXT NOT NULL);")
cursor.execute("CREATE TABLE if not exists courses(course_id TEXT PRIMARY KEY, name TEXT NOT NULL, instructor_id TEXT, FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id) ON DELETE SET NULL ON UPDATE NO ACTION);")

cursor.execute("CREATE TABLE if not exists registered_courses(student_id TEXT NOT NULL, course_id TEXT NOT NULL, PRIMARY KEY(student_id, course_id), FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE ON UPDATE NO ACTION, FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE ON UPDATE NO ACTION)")
conn.commit()

conn.close()