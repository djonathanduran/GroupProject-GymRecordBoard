from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from .import user


class Workout:
    db_name = "workouts"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.cardio_max = db_data['cardio_max']
        self.arm_curl_max = db_data['arm_curl_max']
        self.squats_max_sets = db_data['squats_max_sets']
        self.situp_reps_max = db_data['situp_reps_max']
        self.leg_set_max = db_data['leg_set_max']
        self.triceps_sets_max = db_data['triceps_sets_max']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = []

    @classmethod
    def get_all_workouts(cls):
        query = "SELECT * FROM workouts;"
        workouts_from_db = connectToMySQL(cls.db_name).query_db(query)

        workouts = []
        for workout in workouts_from_db:
            workouts.append(cls(workout))
        return workouts

    @classmethod
    def add_workout(cls, db_data):
        query = "INSERT INTO workouts (cardio_max, arm_curl_max, squats_max_sets, situp_reps_max, leg_set_max, triceps_sets_max, `user_id`) VALUES (%(cardio_max)s, %(arm_curl_max)s, %(squats_max_sets)s, %(situp_reps_max)s, %(leg_set_max)s, %(triceps_sets_max)s, %(user_id)s ); "

        return connectToMySQL(cls.db_name).query_db(query, db_data)

    @staticmethod
    def validate_workout(workout):
        is_valid = True
        if len(workout['cardio_max']) < 0:
            is_valid = False
            flash("Must be more that 0", "error2")
        if len(workout['arm_curl_max']) < 0:
            is_valid = False
            flash("Must be more that 0", "error2")
        if len(workout['squats_max_sets']) < 0:
            is_valid = False
            flash("Must be more that 0", "error2")
        if len(workout['situp_reps_max']) < 0:
            is_valid = False
            flash("Must be more that 0", "error2")
        if len(workout['leg_set_max']) < 0:
            is_valid = False
            flash("Must be more that 0", "error2")
        if len(workout['triceps_sets_max']) < 0:
            is_valid = False
            flash("Must be more that 0", "error2")
        return is_valid

    @classmethod
    def update_workout(cls, data):
        query = "UPDATE workouts SET cardio_max = %(cardio_max)s, arm_curl_max = %(arm_curl_max)s, squats_max_sets = %(squats_max_sets)s, situp_reps_max = %(situp_reps_max)s, leg_set_max = %(leg_set_max)s, triceps_sets_max = %(triceps_sets_max)s WHERE id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy_workout(cls, data):
        query = "DELETE FROM workouts WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one_workout(cls, data):
        query = "SELECT * FROM workouts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])
