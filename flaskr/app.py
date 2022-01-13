from flask import  ( 
    Flask,
    redirect,
    render_template,
    request, 
    session,
    url_for,
    flash
)

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
import secrets

# Own function library
from functions import databases_conf


app = Flask(__name__)
app.secret_key = secrets.token_hex()


######################## login ######################## 
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    session.pop('username' , None)
    myjson = databases_conf(app.static_folder)
    user_db = mysql.connector.connect(**myjson['user'])
    cursor = user_db.cursor()
 
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        sql = f'SELECT username, password FROM USERS WHERE username="{username}"'
        cursor.execute(sql)
        user =  cursor.fetchall()

        if len(user) > 0:
            if user[0][0] and user[0][1] == password:
                #cokie with the user_id
                session['username'] = user[0][0]
                user_db.close()
                return redirect(url_for('dashboard'))

            else:
                error='Invalid Credentials'
                flash(error)
        else:
            error='User does not exists'
            flash(error)

    return render_template('login.html', error=error)


######################## NEMA ######################## 
@app.route("/equipment", methods=['GET', 'POST'])
def equipment():

    myjson = databases_conf(app.static_folder)
    equip_db = mysql.connector.connect(**myjson['MCC'])
    cursor = equip_db.cursor()

    if request.method == 'POST':
        description = request.form['desc']
        sql = f"INSERT INTO EQUIPMENTS (Description) VALUES ('{description}')"
        cursor.execute(sql)
        equip_db.commit()
        redirect(url_for('equipment'), code=200, Response=None)

    sql = "SELECT Equipment_ID, Description FROM EQUIPMENTS ORDER BY Description"
    cursor.execute(sql)
    result = cursor.fetchall()
    equip_db.close()
    return render_template('equipments.html', data=result )

######################## NEMA ######################## 
@app.route("/nema", methods=['GET', 'POST'])
def nema():
    myjson = databases_conf(app.static_folder)
    equip_db = mysql.connector.connect(**myjson['MCC'])
    cursor = equip_db.cursor()


    if request.method == 'POST':
        description = request.form['desc']
        sql = f"INSERT INTO NEMA (Description) VALUES ('{description}')"
        cursor.execute(sql)
        equip_db.commit()
        redirect(url_for('nema'), code=200, Response=None)

    sql = "SELECT Nema_Id, Description FROM NEMA ORDER BY Description"
    cursor.execute(sql)
    result = cursor.fetchall()
    equip_db.close()
    return render_template('nema.html', data=result )

######################## DASHBOARD ######################## 
@app.route("/dashboard")
def dashboard():
    if not ('username' in session):
        return redirect(url_for("login"))

    return render_template('dashboard.html')

######################## delete  ######################## 
@app.route("/delete/<int:id>,<table>,<field_id>,<url_return>")
def delete(id, table, field_id, url_return):
    myjson = databases_conf(app.static_folder)
    equip_db = mysql.connector.connect(**myjson['MCC'])
    cursor = equip_db.cursor()
    sql = f"DELETE FROM {table} WHERE {field_id} = {id} "
    cursor.execute(sql)
    equip_db.commit()
    flash("record deleted")
    return redirect(url_for(url_return))




######### FUNCTIONS

