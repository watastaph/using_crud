from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipes:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.status = data['status']
        self.instructions = data['instructions']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['txt-name']) <2:
            flash("Recipe name must be at least 3 characters long!")
            is_valid = False
        if len(recipe['txt-description']) <2:
            flash("Recipe description must be at least 3 characters long!")
            is_valid = False
        if len(recipe['txt-instructions']) <2:
            flash("Recipe instructions must be at least 3 characters long!")
            is_valid = False
        return is_valid
    
    @classmethod
    def add_recipe(cls, data):
        query = "INSERT INTO recipes (user_id, name, description,  status, instructions, date, created_at, updated_at) VALUES (%(user_id)s, %(name)s, %(description)s, %(status)s, %(instructions)s, %(date)s, NOW(), NOW());"
        print(query)
        return connectToMySQL("recipes").query_db(query, data)
    
    @classmethod
    def all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL("recipes").query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        print(results)
        return posts