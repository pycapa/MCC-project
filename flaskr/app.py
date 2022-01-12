from flask import  ( 
    Flask,
    g,
    redirect,
    render_template,
    request, 
    session,
    url_for,
    flash
)

from dotenv import load_dotenv
import secrets



class User:
    def __init__(self, user_id, username, password ):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'{self.username}'



# Here the conecction to database.
# Sentence below is a Data simulation.

users = []
users.append(User(user_id=1, username='Carlos', password='password'))
users.append(User(user_id=2, username='Luisa', password='secret'))

#


app = Flask(__name__)
app.secret_key = secrets.token_hex()

# Main route
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    session.pop('username' , None)
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        ### here I have to do the DB users quiery./

        user = [x for x in users if str(x.username).upper() == str(username).upper()][0]

        if user and user.password == password:
            #cokie with the user_id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            error='Invalid Credentials'
            flash(error)

    return render_template('login.html', error=error)


#Equipments Route
@app.route("/equipment")
def equipment():
    return render_template('equipments.html')


#login route
@app.route("/dashboard")
def dashboard():
    if not inSession():
        return redirect(url_for("login"))

    return render_template('dashboard.html')





##### Functions

def inSession():
    return ('username' in session)