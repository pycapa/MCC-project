# MCC app
from re import S
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

import secrets
import json
import os

# Own function library
from functions import databases_conf
from sqlConnector import sql_conexion


confg = json.dumps

def databases_conf(url):
    filename = os.path.join(url, 'db.json')
    with open(filename) as json_file:
        data = json.load(json_file)
    return data





app = Flask(__name__)
app.secret_key = secrets.token_hex()



# Conexion a la base de datos
_HOST = 'us-cdbr-east-05.cleardb.net'
_USER = 'b09f93e7cfc688'
_PASSWORD = '63547657'
_DATABASE = 'heroku_4e8e417c8946624'

dbConecction = sql_conexion(_USER, _PASSWORD, _HOST, _DATABASE)



######################## login ######################## 
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    session.pop('username' , None)
    # metodo post toma del formulario los datos del usuario para validacion

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = f'SELECT user_name, user_password FROM USERS WHERE user_name="{username}"'
        dbConecction.connect()
        result = dbConecction.execute(sql)
        if len(result) > 0:
            if result[0][1] == password:
                #cokie with the user_id
                session['username'] = result[0][0]
                return redirect(url_for('dashboard'))
            else:
                error='Invalid Credentials'
                flash(error)
        else:
            error='User does not exists'
            flash(error)     

    return render_template('login.html', error=error) 


######################## equipment ######################## 

@app.route("/equipment", methods=['GET', 'POST'])
def equipment():

    if request.method == 'POST':
        description = request.form['desc']
        sql = f"INSERT INTO EQUIPMENTS (Description) VALUES ('{description}')"
        try:
            dbConecction.connect()
            dbConecction.execute(sql)
            flash('Record saved', 'info')
            return {'status':'Done'}
        except Exception as e:
            flash('Something has happend: ' + e['errno'])
            return {'status': 'Error'}


    sql = "SELECT Equipment_Id, Description FROM EQUIPMENTS ORDER BY Description"
    
    dbConecction.connect()
    qry = dbConecction.execute(sql)
    data = [{"Equipment_Id":result[0], "Description":result[1], 'table':'EQUIPMENTS', 'key':'Equipment_id'} for result in qry]
    dbConecction.close()
    return render_template('equipments.html', data=data)

######################## NEMA ######################## 
@app.route("/nema", methods=['GET', 'POST'])
def nema():


    if request.method == 'POST':
        description = request.form['desc']
        sql = f"INSERT INTO NEMA (Description) VALUES ('{description}')"
        try:
            dbConecction.connect()
            dbConecction.execute(sql)
            dbConecction.close()
            flash('Record saved', 'info')
            return {'status' : 'Done'}
        except Exception as e:
            flash('Something has happend: ' + e.args[1], 'error')
            return {'estatus' : 'Error'}
        

    sql = "SELECT Nema_Id, Description FROM NEMA ORDER BY Description"
    dbConecction.connect()
    qry = dbConecction.execute(sql)

    
    data = [{"Nema_id":nema[0], "Description":nema[1],'table':'NEMA', 'key':'Nema_id'} for nema in qry]
    dbConecction.close()
    return render_template('nema.html', data=data )

######################## COMPONENTS ######################## 
@app.route("/components", methods=['GET', 'POST'])
def components():
    if request.method == 'POST':
        code = request.form['code']
        description = request.form['desc']
        sql = f"INSERT INTO components (description, code) VALUES ('{description}','{code}')"
        try:
            dbConecction.connect()
            dbConecction.execute(sql)
            dbConecction.close()
            flash('Record saved', 'info')
            return {'status':'Done'}
        except Exception as e:
            flash('Something has happend: ' + e.args[1], 'error')
            return {'status':'Error'}

        

    sql = "SELECT component_id, description, code FROM components ORDER BY description"
    dbConecction.connect()
    qry = dbConecction.execute(sql)
    data = [{"component_id":components[0], 
                "description":components[1],
                "code":components[2], 'table':'COMPONENTS', 'key':'Component_id'} for components in qry]
    dbConecction.close()

    return render_template('components.html', data=data )
######################## DASHBOARD ######################## 
@app.route("/dashboard")
def dashboard():
    if not ('username' in session):
        return redirect(url_for("login"))

    return render_template('dashboard.html')

######################## delete  ######################## 
@app.route("/delete/<id>,<dataset>,<key>", methods=['POST'])
def delete(id,dataset,key):

    sql = f"DELETE FROM {dataset} WHERE {key} = {id} "
    
    dbConecction.connect()

    try:
        dbConecction.execute(sql)
        flash("Record deleted", 'info')
        return '{"status":"Done"}'
    except:
        flash("status", 'error')

    return "redirect(url_for(data['url_return']))"


###################### buckets ########################
@app.route("/buckets", methods=['GET', 'POST'])
def buckets():
    if request.method == 'POST':
   
        Type  = request.form['type']
        Hrs_Estimated = request.form['hrs_estimated']
            
        sql = f"INSERT INTO Bucket_Type (Type, Hrs_Estimated) VALUES ('{Type}',{Hrs_Estimated} )"
        try:
            dbConecction.connect()
            dbConecction.execute(sql)
            dbConecction.close()
            flash('Record saved', 'info')
            return {'status':'Done'}
        except Exception as e:
            flash('Something has happend: ' + e.args[1], 'error')
            return {'status':'Error'}
        

    sql = "SELECT Bucket_ID, Type, Hrs_Estimated FROM BUCKET_TYPE Bucket_Id"
    dbConecction.connect()
    qry = dbConecction.execute(sql)
    result = [{"Bucket_id":Bucket[0], "Type":Bucket[1], "Hrs_Estimated":Bucket[2], 'table':'BUCKET_TYPE', 'key':'Bucket_Id'} for Bucket in qry]
    dbConecction.close()

    return render_template('Buckets.html', data=result )


@app.route("/operators", methods=['GET', 'POST'])
def operators():


    if request.method == 'POST':
        name = request.form['name']
        sql = f"INSERT INTO Operators (name) VALUES ('{name}')"
        try:
            dbConecction.connect()
            dbConecction.execute(sql)
            dbConecction.close()
            flash('Record saved', 'info')
            return {'status' : 'Done'}
        except Exception as e:
            flash('Something has happend: ' + e.args[1], 'error')
            return {'estatus' : 'Error'}
        

    sql = "SELECT Operator_Id, name FROM operators ORDER BY name"
    dbConecction.connect()
    qry = dbConecction.execute(sql)

    
    data = [{"operator_id":nema[0], "name":nema[1],'table':'operators', 'key':'operator_id'} for nema in qry]
    dbConecction.close()
    return render_template('operators.html', data=data )

######### FUNCTIONS

@app.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        data = request.get_json() 
        print(data["id"])
    return data