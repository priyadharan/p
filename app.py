from collections import UserString
from flask import Flask, render_template,redirect,url_for,request,flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import sqlite3 as sql


app=Flask(__name__)

app.config['SECRET_KEY']='supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
   file= FileField("File", validators=[InputRequired()])
   submit= SubmitField("Upload File")

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  email=request.form['email']
  password=request.form['password']
  con=sql.connect("db_web.db")
  cur=con.cursor()
  cur.execute("insert into users(EMAIL,PASSWORD) values (?,?)",(email,password))
  con.commit()
  flash('User Added','success')
  return redirect(url_for("show"))
 return render_template('login.html')
    

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/show')
def show():
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select EMAIL from users")
    data=cur.fetchall()

    return render_template('show.html', datas=data)


@app.route('/show1')
def show1():
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select PROJECTNAME,PROJECTGUIDE from u1")
    data=cur.fetchall()

    return render_template('show1.html', datas=data)


@app.route('/pro',methods=['GET','POST'])
def pro():
 if request.method=='POST':
  projectname=request.form['projectname']
  projectguide=request.form['projectguide']
  projectdescrition=request.form['projectdescription']
  con=sql.connect("db_web.db")
  cur=con.cursor()
  cur.execute("insert into u1(PROJECTNAME,PROJECTGUIDE,PROJECTDESCRIPTION) values (?,?,?)",(projectname,projectguide,projectdescrition))
  con.commit()
  flash('User Added','success')
  return redirect(url_for("show1"))
 return render_template('pro.html')

@app.route('/p1',methods=['GET','POST'])
def p1():
    form= UploadFileForm()
    if form.validate_on_submit():
       file=form.file.data
       file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
       return "File has been uploaded"

    return render_template('p1.html', form=form)


if __name__ == '__main__':
    app.secret_key='admin123'
    
    app.run(debug=True)
   
    