from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email = data['email']
        self.pword = data['pword']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['txt-fname']) <1:
            flash("First name must be at least 2 characters long!")
            is_valid = False
        if len(user['txt-lname']) <1:
            flash("Last name must be at least 2 characters long!")
            is_valid = False
        if not EMAIL_REGEX.match(user['txt-email']):
            flash("Invalid Email!")
            is_valid = False
        if user['txt-pword'] != user['txt-cpword']:
            flash("Password and confirm password not match!")
            is_valid = False
        return is_valid

    @classmethod
    def add_users(cls, data):
        query = "INSERT INTO users (fname, lname, email, pword, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, %(pword)s, NOW(), NOW());"
        return connectToMySQL("recipes").query_db(query, data)
    
    @classmethod
    def login_user(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("recipes").query_db(query, data)
        if len(results)<1:
            return False
        return cls(results[0])