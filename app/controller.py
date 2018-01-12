from flask import Flask, render_template, request, flash, redirect, url_for, session
import models
from forms import Forms, iDnumForm, UpdateForm, courseForms, courseNumForm, courseUpdateForm
import sqlite3 as sql
from app import app
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


con = sql.connect("studentdb.db")
cur = con.cursor()

con.execute('CREATE TABLE IF NOT EXISTS students(idnum TEXT PRIMARY KEY, fname TEXT, mname TEXT, lname TEXT, sex TEXT, courseid TEXT, CHECK(length(courseid)>0), FOREIGN KEY(courseid) REFERENCES course(courseNum) ON DELETE CASCADE ON UPDATE CASCADE)')
con.execute('CREATE TABLE IF NOT EXISTS course(courseNum TEXT PRIMARY KEY, coursename TEXT, coursecode TEXT)')
con.execute('CREATE VIEW IF NOT EXISTS studcourses AS SELECT coursename, idnum, fname, mname, lname, sex  FROM course JOIN students WHERE course.courseNum = students.courseid')

@app.route('/')
def index():
   return render_template("studentDatabase.html")


@app.route('/adder', methods = ['POST', 'GET'])
def adder():

    form = Forms(request.form)
    if request.method == 'POST':
        con = sql.connect("studentdb.db")
        cur = con.cursor()

        idnumNew = form.idnumNew.data
        fnameNew = form.fnameNew.data
        mnameNew = form.mnameNew.data
        lnameNew = form.lnameNew.data
        sexNew = form.sexNew.data
        courseidNew = form.courseidNew.data

        cur.execute("SELECT * FROM students WHERE idnum = ?", (idnumNew,))

        if cur.fetchone() is not None:
            flash('Id number already taken', 'error')
            return render_template("add.html", form=form)
        elif not form.validate():
            flash("Please don't leave any blank and enter F or M on sex ", 'error')
            return render_template("add.html", form=form)

        elif form.validate():
            student = models.Student(idnum = idnumNew, fname = fnameNew, mname =  mnameNew, lname = lnameNew, sex = sexNew,courseid = courseidNew)
            student.add()
            flash('Student successfully added', 'success')
            return render_template("studentDatabase.html")
    else:
        return render_template("add.html", form=form)
    con.close()

@app.route('/addercourse', methods = ['POST', 'GET'])
def addercourse():

    form = courseForms(request.form)
    if request.method == 'POST':
        con = sql.connect("studentdb.db")
        cur = con.cursor()

        courseNumNew = form.courseNumNew.data
        coursenameNew = form.coursenameNew.data
        coursecodeNew = form.coursecodeNew.data

        cur.execute("SELECT * FROM course WHERE courseNum = ?", (courseNumNew,))

        if cur.fetchone() is not None:
            flash('Course id already taken', 'error')
            return render_template("addcourse.html", form=form)
        elif not form.validate():
            flash('Please fill up the whole form', 'error')
            return render_template("addcourse.html", form=form)

        elif form.validate():
            student = models.Course(courseNum = courseNumNew, coursename = coursenameNew, coursecode =  coursecodeNew)
            student.addcourse()
            flash('Course successfully added', 'success')
            return render_template("studentDatabase.html")
    else:
        return render_template("addcourse.html", form=form)
    con.close()


@app.route('/view')
def view():

    studs = models.Student.view()
    return render_template("print.html",studs = studs)

@app.route('/viewCourse')
def viewCourse():

    studs = models.Course.view()
    return render_template("printCourse.html",studs = studs)

@app.route('/studentCourse')
def studCourse():
    con = sql.connect("studentdb.db")

    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM studcoursess')

    studs = cur.fetchall()
    con.close()
    return render_template("studcourse.html",studs = studs)


@app.route('/updateGet', methods = ['POST', 'GET'])
def updateGet():
    form = iDnumForm(request.form)
    if request.method == 'POST':
        con = sql.connect("studentdb.db")
        cur = con.cursor()
        idnumNew = form.idnumNew.data


        cur.execute("SELECT * FROM students WHERE idnum = ?", (idnumNew,))

        if cur.fetchone() is None:
            flash('Student Not in record', 'error')
            return render_template("updateGet.html", form = form)

        else:
            session['idnumNew'] = request.form['idnumNew']
            return redirect(url_for('updateImp'))



    else:
        return render_template("updateGet.html", form=form)



@app.route('/updateImp', methods = ['POST', 'GET'])
def updateImp():
    form = UpdateForm(request.form)
    idnumNew = session['idnumNew']
    if request.method == 'POST':
        fnameNew = form.fnameNew.data
        mnameNew = form.mnameNew.data
        lnameNew = form.lnameNew.data
        sexNew = form.sexNew.data
        courseidNew = form.courseidNew.data


        if form.validate():
            update(idnumNew,fnameNew,mnameNew,lnameNew,sexNew,courseidNew)
            flash('Successfully Updated', 'success')
            return render_template("update.html", form = form)
        elif not form.validate():
                flash('Please fill up each of the following', 'error')
                return render_template("update.html", form = form)

        else:
            flash('error in update operation', 'error')
            return render_template("updateGet.html", form=form)


    else:
        return render_template("update.html", form=form)

@app.route('/updateGetCourse', methods = ['POST', 'GET'])
def updateGetCourse():
    form = courseNumForm(request.form)
    if request.method == 'POST':
        con = sql.connect("studentdb.db")
        cur = con.cursor()
        courseNumNew = form.courseNumNew.data


        cur.execute("SELECT * FROM course WHERE courseNum = ?", (courseNumNew,))

        if cur.fetchone() is None:
            flash('Course Not in record', 'error')
            return render_template("updateGetCourse.html", form = form)

        else:
            session['courseNumNew'] = request.form['courseNumNew']
            return redirect(url_for('updateImpCourse'))



    else:
        return render_template("updateGetCourse.html", form=form)



@app.route('/updateImpCourse', methods = ['POST', 'GET'])
def updateImpCourse():
    form = courseUpdateForm(request.form)
    courseNumNew = session['courseNumNew']
    if request.method == 'POST':
        coursenameNew = form.coursenameNew.data
        coursecodeNew = form.coursecodeNew.data


        if form.validate():
            updateCourse(courseNumNew,coursenameNew,coursecodeNew)
            flash('Successfully Updated', 'success')
            return render_template("updateCourse.html", form = form)
        elif not form.validate():
                flash('Please fill up each of the following', 'error')
                return render_template("updateCourse.html", form = form)

        else:
            flash('error in update operation', 'error')
            return render_template("updateGetCourse.html", form=form)


    else:
        return render_template("updateCourse.html", form=form)



@app.route('/deletepage', methods = ['POST', 'GET'])
def deletepage():
    form = iDnumForm(request.form)
    con = sql.connect("studentdb.db")
    cur = con.cursor()
    if request.method == 'POST':
        idnumNew = form.idnumNew.data

        cur.execute("SELECT * FROM students WHERE idnum = ?", (idnumNew,))

        if cur.fetchone() is None and form.validate():
            flash('Student not found', 'error')
            return render_template("delete.html", form=form)

        elif form.validate() and cur.fetchone is not None:

            student = models.Student(idnum = idnumNew, fname = "", mname = "", lname = "", sex ="", courseid = "")
            student.delete()
            flash('Student Successfully deleted', 'success')
            return render_template("delete.html", form=form)
        elif not form.validate():
            flash('error in delete operation', 'error')
            return render_template("delete.html", form=form)


    else:
        return render_template("delete.html", form=form)


@app.route('/deleteCourse', methods = ['POST', 'GET'])
def deleteCourse():
    form = courseNumForm(request.form)
    con = sql.connect("studentdb.db")
    cur = con.cursor()
    if request.method == 'POST':
        courseNumNew = form.courseNumNew.data

        cur.execute("SELECT * FROM course WHERE courseNum = ?", (courseNumNew,))

        if cur.fetchone() is None and form.validate():
            flash('Course not found', 'error')
            return render_template("deleteCourse.html", form=form)

        elif form.validate() and cur.fetchone is not None:

            student = models.Course(courseNum = courseNumNew, coursename = "", coursecode = "")
            student.delete()
            flash('Course Successfully deleted', 'success')
            return render_template("deleteCourse.html", form=form)
        elif not form.validate():
            flash('error in delete operation', 'error')
            return render_template("deleteCourse.html", form=form)


    else:
        return render_template("deleteCourse.html", form=form)


@app.route('/searchGet', methods = ['POST', 'GET'])
def searchGet():
    search = request.form['search']
    if request.method == 'POST':
        con = sql.connect("studentdb.db")
        cur = con.cursor()


        cur.execute("SELECT * FROM students where idnum = ? or fname = ? or mname = ? or lname = ? or sex=? or courseid = ?", (search,search,search,search,search,search))


        if cur.fetchone() is None:
            flash('Student Not in record or Letter capitalization incorrect', 'error')
            return render_template("studentDatabase.html")

        else:
            student = models.Student(idnum = search, fname = search, mname =  search, lname = search, sex = search, courseid = search)
            studs = student.search()
            return render_template("print.html", studs=studs)


    else:
        return render_template("studentDatabase.html")




def update(idnum,fname,mname,lname,sex,courseid):
        con = sql.connect("studentdb.db")

        con.execute("UPDATE students set fname = ? where idnum = ?", (fname,idnum))
        con.commit()

        con.execute("UPDATE students set mname = ? where idnum = ?", (mname,idnum))
        con.commit()

        con.execute("UPDATE students set lname = ? where idnum = ?", (lname,idnum))
        con.commit()

        con.execute("UPDATE students set sex = ? where idnum = ?", (sex,idnum))
        con.commit()

        con.execute("UPDATE students set courseid = ? where idnum = ?", (courseid,idnum))
        con.commit()

def updateCourse(courseNum,coursename,coursecode):
    con = sql.connect("studentdb.db")

    con.execute("UPDATE course set coursename = ? where courseNum = ?", (coursename,courseNum))
    con.commit()

    con.execute("UPDATE course set coursecode = ? where courseNum = ?", (coursecode,courseNum))
    con.commit()




