from flask import render_template,request,url_for,flash,redirect
from app import app
from flask_mysqldb import MySQL
app.secret_key="the grace of God"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="admindb"
mysql=MySQL(app)
@app.route('/')
def index():
    user={'username':'Álbert'}
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    results=cur.fetchall()
    cur.close()
    return render_template('index.html',students=results,user=user) 

#endpoint for inserting studentdata into the database   
@app.route('/insert',methods=['POST','GET']) 
def insert():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM student where email=%s',(email,))
        res=cur.fetchone()
        if res:
            flash("email already exist")
        else:
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO student(Name,email,phone) VALUES(%s,%s,%s)",(name,email,phone))
            mysql.connection.commit()
            cur.close()
            flash("Record Inserted Successfully")
    return redirect(url_for('index'))  

@app.route('/update/',methods=['GET','POST'])
def update():
    if request.method=='POST':
        id_data=request.form['id']
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cur=mysql.connection.cursor()
        cur.execute("UPDATE student set name=%s,email=%s,phone=%s WHERE id=%s",(name,email,phone,id_data))
        mysql.connection.commit()
        flash("Record Upadated Successfully")
    return redirect(url_for('index'))
@app.route('/delete/<string:id_data>',methods=['GET','POST']) 
def delete(id_data):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE id=%s",(id_data,))
    mysql.connection.commit()
    flash("Record Deleted Successfully")
    return redirect(url_for('index'))

@app.route('/blog')
def blog():
    user={'username':'Albert'}
    posts=[
        {
        'author':{'username':'Winnie'},
        'title':'How To Progam',
        'content':'i like coding with scripting.',
        'date_posted':'22/07/2019 2pm'
    },
    {
        'author':{'username':'Adam'},
        'title':'what to avoid',
        'content':'i hate copying other peoples code ',
        'date_posted':'22/07/2019 2pm'
    }
    ]
    return render_template('blog.html',user=user, posts=posts)