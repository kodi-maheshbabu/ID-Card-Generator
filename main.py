from flask import Flask, render_template, request, redirect,session
from flask_mysqldb import MySQL

app = Flask(__name__)

host = app.config['MYSQL_HOST'] = "localhost"
user = app.config['MYSQL_USER'] = "root"
pswd = app.config['MYSQL_PASSWORD'] = ""
database = app.config['MYSQL_DB'] = "project"
app.config['SECRET_KEY'] = 'kodimaheshbabu'

mysql = MySQL(app)

username = ""
password = ""
items=[]

@app.route("/")
def home():
    return render_template("Homepage.html")

@app.route("/idadmin")
def idadmin():
    return render_template("idcardadmin.html")

@app.route("/login",methods = ["GET","POST"])
def login():  
    global username,password
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #session["username"] = username
        #session["password"] = password
        submit = request.form["submit_button"]
        if submit:
            cursor = mysql.connection.cursor()
            cursor.execute("select * from teammates where username=%s and password=%s",(username,password))   
            user = cursor.fetchone()
            if user:
                return redirect("/successu")
            else:
                return redirect("/failure")
    return render_template("login.html")

@app.route("/adminidg",methods = ["GET","POST"])
def adminidg():
   global items
   global username
   if request.method == "POST":
        username = request.form["username"]
        #session["username"] = username
        conn = mysql.connection.cursor()
        conn.execute("select * from teammates where username = %s" ,{username})
        user = conn.fetchall()
        user = list(user)
        user = user[0][2:]
        user = tuple(user)
        return render_template("dataaa.html",items = user)
   
@app.route("/editu")
def editu():
    return render_template("editu.html")

@app.route("/edituu",methods = ["GET","POST"])
def edituu():
    global username,password,items
    if request.method == "POST":
       usernamen = request.form["username"]
       passwordn = request.form["password"]
       studentname = request.form["studentname"]
       rollnumber = request.form["rollnumber"]
       year = request.form["year"]
       branch = request.form["branch"]
       phonenumber = request.form["phonenumber"]
       submit = request.form["submit_button"]
       if submit:
        conn = mysql.connection.cursor()
        conn.execute("delete from teammates where username = %s and password = %s",(username,password))
        conn.execute("insert into teammates values(%s, %s, %s, %s, %s, %s, %s);",(usernamen,passwordn,studentname,rollnumber,year,branch,phonenumber))
        mysql.connection.commit()
        conn = mysql.connection.cursor()
        conn.execute("select student_name,roll_no,year,branch,phone_no from teammates where username = %s and password = %s",(username,password))
        items = conn.fetchall()
        return render_template("data.html",items = items)
    return redirect("/failure")

@app.route("/edituuu",methods = ["GET","POST"])
def edituuu():
    global username,password
    if request.method == "POST":
        password = request.form["password"]
        username = request.form["username"]
        conn = mysql.connection.cursor()
        conn.execute("select * from teammates where username=%s and password=%s",(username,password))
        user = conn.fetchall()
        if user:
            return render_template("edituuu.html")
    return redirect("/failure")

@app.route("/contact")
def contact():
    return render_template("contactus.html")

@app.route("/idh",methods = ["GET","POST"])
def idh():
    global items
    global username,password
    conn = mysql.connection.cursor()
    conn.execute("select student_name,roll_no,year,branch,phone_no from teammates where username = %s",{username})
    items = conn.fetchall()
    return render_template('idcardh.html',items = items)

@app.route("/idv",methods = ["GET","POST"])
def idv():
    global items
    global username,password
    conn = mysql.connection.cursor()
    conn.execute("select student_name,roll_no,year,branch,phone_no from teammates where username = %s" ,{username})
    items = conn.fetchall()
    return render_template('idcardv.html',items = items)

@app.route("/successu")
def successu():
    global items
    global username,password
    conn = mysql.connection.cursor()
    conn.execute("select student_name,roll_no,year,branch,phone_no from teammates where username = %s and password = %s",(username,password))
    items = conn.fetchall()
    return render_template('data.html',items = items)

@app.route("/homea")
def homea():
    return render_template('homea.html')

@app.route("/failure")
def failure():
    return render_template('error.html')

@app.route("/loginadmin",methods = ["GET","POST"])
def loginadmin():
    global username,password
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #session["username"] = username
        #session["password"] = password
        submit = request.form["submit_button"]
        if submit:
            cursor = mysql.connection.cursor()
            cursor.execute("select * from admins where username=%s and password=%s",(username,password))   
            admina = cursor.fetchone()
            if admina:
                return redirect("/successaa")
            else:
                return redirect("/failure")
            
@app.route("/successaa")
def successaa():
    return render_template('homea.html')

@app.route("/successa")
def successa():
    global items,username,password
    conn = mysql.connection.cursor()
    conn.execute("select username,student_name,roll_no,year,branch,phone_no from teammates")
    items = conn.fetchall()
    return render_template('admindata.html',items= items)

@app.route("/registrationform",methods = ["GET","POST"])
def registrationform():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        studentname = request.form["studentname"]
        rollnumber = request.form["rollnumber"]
        year = request.form["year"]
        branch = request.form["branch"]
        phonenumber = request.form["phonenumber"]
        submit = request.form["submit_button"]
        if submit:
            conn = mysql.connection.cursor()
            conn.execute("insert into teammates values(%s,%s,%s,%s,%s,%s,%s);",(username,password,studentname,rollnumber,year,branch,phonenumber))
            mysql.connection.commit()
    return redirect('/successa')

@app.route("/registrationformt")
def registrationformt():
    return render_template("registerform.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template('adminlogin.html')

@app.route("/logout")
def logout():
    return redirect('/')

if __name__=='__main__':
    app.run(debug = True,use_reloader = True)
