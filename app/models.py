import sqlite3 as sql


class Student:

    def __init__(self,idnum,fname,mname,lname,sex,courseid):
        self.idnum = idnum
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.sex = sex
        self.courseid = courseid





    @staticmethod
    def view():
        con = sql.connect("studentdb.db")

        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('select * from students')

        studs = cur.fetchall();
        return studs

    def add(self):
        con = sql.connect("studentdb.db")
        cur = con.cursor()

        cur.execute('''INSERT INTO students(idnum,fname,mname,lname,sex,courseid)
                     VALUES (?,?,?,?,?,?)''',(self.idnum,self.fname,self.mname,self.lname,self.sex,self.courseid))

        con.commit()

    def delete(self):
        con = sql.connect("studentdb.db")
        cur = con.cursor()
        cur.execute("DELETE from students where idnum = ?", (self.idnum,))
        con.commit()


    def search(self):
        con = sql.connect("studentdb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM students where idnum = ? or fname = ? or mname = ? or lname = ? or sex = ? or courseid = ?", (self.idnum,self.fname,self.mname,self.lname,self.sex,self.courseid))

        studs = cur.fetchall();
        return studs


class Course:

    def __init__(self,courseNum,coursename,coursecode):
        self.courseNum = courseNum
        self.coursename = coursename
        self.coursecode = coursecode

    def addcourse(self):
        con = sql.connect("studentdb.db")
        cur = con.cursor()

        cur.execute('''INSERT INTO course(courseNum,coursename,coursecode)
                VALUES (?,?,?)''',(self.courseNum,self.coursename,self.coursecode))

        con.commit()

    @staticmethod
    def view():
        con = sql.connect("studentdb.db")

        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('select * from course')

        studs = cur.fetchall();
        return studs

    def delete(self):
        con = sql.connect("studentdb.db")
        cur = con.cursor()
        cur.execute("DELETE from course where courseNum = ?", (self.courseNum,))
        con.commit()

