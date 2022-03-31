from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.workout import Workout
from flask_app.models.comment import Expense
from flask_app.models.user import User

# adding new workout

@app.route('/one_workout/<int:user_id>')
def new_comment():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('.html', user=User.get_by_id(data))