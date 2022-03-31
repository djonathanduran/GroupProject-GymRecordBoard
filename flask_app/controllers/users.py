from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.workout import Workout
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

# Create a user / register

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')


# login a user

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# dashboard

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    users = User.get_by_id(data)
    all_users = User.get_all_users()
    return render_template("dashboard.html", users = users, all_users = all_users )



# Read a user

@app.route('/one_user/<int:usr_id>')
def display_one_user(usr_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': usr_id
    }
    users_and_workouts = User.get_one_with_workouts(data)
    return render_template('one_user.html', users_and_workouts = users_and_workouts)

# logout

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
