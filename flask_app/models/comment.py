from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from .import user, workout


class Expense:
    db_name2 = "workouts"

    def __init__(self, db_data2):
        self.id = db_data2['id']
        self.content = db_data2['content']
        self.created_at = db_data2['created_at']
        self.updated_at = db_data2['updated_at']
        self.user = []
        self.workout = []

    @classmethod
    def get_all_comments(cls):
        query = "SELECT * FROM comments WHERE id = %(`user_id`)s;"
        comments_from_db = connectToMySQL(cls.db_name2).query_db(query)

        comments = []
        for comment in comments_from_db:
            comments.append(cls(comment))
        return comments

    @classmethod
    def add_comment(cls, db_data2):
        query = "INSERT INTO comments (content, `user_id`) VALUES (%(content)s, %(user_id)s ); "

        return connectToMySQL(cls.db_name2).query_db(query, db_data2)

    @staticmethod
    def validate_comments(data):
        is_valid = True
        if len(data['content']) < 2:
            is_valid = False
            flash("Content must be more than 2 charcters", "error2")
        if len(data['content']) == 0:
            is_valid = False
            flash("Amount is required", "error2")
        return is_valid

    @classmethod
    def update_comment(cls, data):
        query = "UPDATE comments SET content = %(content)s WHERE id = %(id)s"
        return connectToMySQL(cls.db_name2).query_db(query, data)

    @classmethod
    def destroy_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name2).query_db(query, data)

    @classmethod
    def get_one_comment(cls, data):
        query = "SELECT * FROM comments WHERE id = %(user_id)s;"
        results = connectToMySQL(cls.db_name2).query_db(query, data)
        return cls(results[0])
