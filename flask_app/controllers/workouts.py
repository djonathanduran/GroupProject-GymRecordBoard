from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.workout import Workout
from flask_app.models.comment import Expense
from flask_app.models.user import User
# from flask_app.controllers import users



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
        "cardio_max": request.form["cardio_max"],
        "arm_curl_max": request.form["arm_curl_max"],
        "squats_max_sets": request.form["squats_max_sets"],
        "situp_reps_max": request.form["situp_reps_max"],
        "legs_set_max": request.form["legs_set_max"],
        "triceps_sets_max": request.form["triceps_sets_max"],
        "user_id": session["user_id"]
    }
    Workout.add_workout(data)
    return redirect('/dashboard')


# reading a workout

@app.route('/one_workout/<int:workout_id>')
def one_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': workout_id,
    }
    one_workout = Workout.get_one_workout(data)
    print(one_workout)
    return render_template('one_workout.html', one_workout = one_workout)

# Update a workout

@app.route('/edit/<int:workout_id>')
def edit_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data_workout = {
        'id': workout_id
    }
    user_data = {
        "id":session['user_id']
    }
    this_user = User.get_by_id(user_data)
    one_workout = Workout.get_one_workout(data_workout)
    return render_template('edit_workout.html', one_workout = one_workout, this_user = this_user)

@app.route('/update_workout/<int:workout_id>', methods = ['POST'])
def update_one_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout.validate_workout(request.form):
        return redirect(f'/edit/{workout_id}')
    data = {
        'id': workout_id,
        "cardio": request.form["cardio"],
        "arm_curl_max": request.form["arm_curl_max"],
        "squats_max_sets": request.form["squats_max_sets"],
        "situp_reps_max": request.form["situp_reps_max"],
        "legs_set_max": request.form["legs_set_max"],
        "triceps_sets_max": request.form["triceps_sets_max"]
    }
    Workout.update_workout(data)
    return redirect('/dashboard')


# Destroy a workouts

@app.route('/destroy_workout/<int:workout_id>')
def delete_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': workout_id
    }

    Workout.destroy_workout(data)
    return redirect('/dashboard')
