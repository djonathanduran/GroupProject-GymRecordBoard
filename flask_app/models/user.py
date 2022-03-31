from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
import re

from flask_app.models.workout import Workout
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db = "models"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.workouts = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        this_user = cls(results[0])
        return this_user

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def get_one_with_workouts(cls, data):
        query = "SELECT * FROM users LEFT JOIN workouts ON users.id = workouts.user_id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_user = cls(results[0])

        for row in results:

            workout_info = {
                'id': row['workouts.id'],
                'cardio_max': row['cardio_max'],
                'arm_curl_max': row['arm_curl_max'],
                'squats_max_sets': row['squats_max_sets'],
                'situp_reps_max': row['situp_reps_max'],
                'legs_set_max': row['legs_set_max'],
                'triceps_sets_max': row['triceps_sets_max'],
                'user_id': row['user_id'],
                'created_at': row['workouts.created_at'],
                'updated_at': row['workouts.updated_at']
            }

            this_workout = Workout(workout_info)
            this_user.workouts.append(this_workout)

        return this_user

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid
