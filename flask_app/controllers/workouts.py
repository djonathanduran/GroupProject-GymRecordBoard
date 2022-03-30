from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.workout import Workout
from flask_app.models.comment import Expense
from flask_app.models.user import User



# adding new workout

@app.route('/new')
def new_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_workout.html', user=User.get_by_id(data))

@app.route('/create_workout', methods = ['POST'])
def create_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout.validate_workout(request.form):
        return redirect('/new')
    data = {
        "cardio": request.form["cardio"],
        "arm_curl_max": request.form["arm_curl_max"],
        "squats_max_sets": request.form["squats_max_sets"],
        "situp_reps_max": request.form["situp_reps_max"],
        "leg_set_max": request.form["leg_set_max"],
        "triceps_sets_max": request.form["triceps_sets_max"]
    }
    # pic_filename = secure_filename("image".filename)
    Workout.add_workout(data)
    return redirect('/dashboard')