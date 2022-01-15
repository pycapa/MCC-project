
from flask import  ( 
    Flask,
    redirect,
    render_template,
    request, 
    session,
    url_for,
    flash,
    jsonify
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
    user_db.close()
    return render_template('login.html', error=error)


######################## equipment ######################## 

@app.route("/equipment", methods=['GET', 'POST'])
def equipment():
    myjson = databases_conf(app.static_folder)
    equip_db = mysql.connector.connect(**myjson['MCC'])
    cursor = equip_db.cursor()
    result = []

    if request.method == 'POST':
        description = request.form['desc']
        sql = f"INSERT INTO EQUIPMENTS (Description) VALUES ('{description}')"
        cursor.execute(sql)
        equip_db.commit()
        return redirect(url_for('equipment'))

    sql = "SELECT Equipment_ID, Description FROM EQUIPMENTS ORDER BY Description"
    cursor.execute(sql)
    equipments = cursor.fetchall()
    result = [{"EqpId" : equip[0], "Description":equip[1]} for equip in equipments]
    equip_db.close()
    return render_template('equipments.html', list=result) 



######################## NEMA ######################## 
@app.route("/nema", methods=['GET', 'POST'])
def nema():
    myjson = databases_conf(app.static_folder)
    equip_db = mysql.connector.connect(**myjson['MCC'])
    cursor = equip_db.cursor()
    result = []

    if request.method == 'POST':
        description = request.form['desc']
        sql = f"INSERT INTO NEMA (Description) VALUES ('{description}')"
        cursor.execute(sql)
        equip_db.commit()

        return redirect(url_for('nema'))

    sql = "SELECT Nema_Id, Description FROM NEMA ORDER BY Description"
    cursor.execute(sql)
    nemas = cursor.fetchall()
    result = [{"NemaId":nema[0], "Description":nema[1]} for nema in nemas]
    equip_db.close()

    return render_template('nema.html', data=result )

######################## COMPONENTS ######################## 
@app.route("/components", methods=['GET', 'POST'])
def components():
    myjson = databases_conf(app.static_folder)
    equip_db = mysql.connector.connect(**myjson['MCC'])
    cursor = equip_db.cursor()
    result = []

    if request.method == 'POST':
        code = request.form['code']
        description = request.form['desc']
        sql = f"INSERT INTO components (description, code) VALUES ('{description}','{code}')"
        
        try:
            cursor.execute(sql)
            equip_db.commit()
        except mysql.connector.Error as err:
            flash(f'Code Error: {err.errno}, {err.msg}' )
            pass

        return redirect(url_for('components'))

    sql = "SELECT component_id, description, code FROM components ORDER BY description"
    cursor.execute(sql)
    componentss = cursor.fetchall()
    result = [{"component_id":components[0], 
                "description":components[1],
                "code":components[2]} for components in componentss]
    equip_db.close()

    return render_template('components.html', data=result )
######################## DASHBOARD ######################## 
@app.route("/dashboard")
def dashboard():
    if not ('username' in session):
        return redirect(url_for("login"))

    return render_template('dashboard.html')

######################## delete  ######################## 
@app.route("/delete", methods=['POST'])
def delete():

    
    data = request.get_json()

    myjson = databases_conf(app.static_folder)
    equip_db = mysql.connector.connect(**myjson['MCC'])
    cursor = equip_db.cursor()
    sql = f"DELETE FROM {data['table']} WHERE {data['field_id']} = {data['id']} "
    
    try:
        cursor.execute(sql)
        equip_db.commit()
        flash("record deleted")
        return redirect(url_for(data['url_return']))
    except:
        flash("error deleting item")

    return redirect(url_for(data['url_return']))

######### FUNCTIONS

@app.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        data = request.get_json() 
        print(data["id"])
    return data