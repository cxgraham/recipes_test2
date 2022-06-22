from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Recipe:
    db = 'recipes_schema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_30_min = data['under_30_min']
        self.date = data['date']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    

    # CREATE 
    @classmethod 
    def create_recipe(cls, data):
        if not cls.validate_recipe(data):
            return False
        query = """
        INSERT INTO recipes (name, description, under_30_min, date, instructions, user_id)
        VALUES (%(name)s, %(description)s, %(under_30_min)s, %(date)s, %(instructions)s, %(user_id)s)
        ;"""
        recipe_id = connectToMySQL(cls.db).query_db(query, data)
        return recipe_id


    # READ 
    @classmethod
    def recipe_info(cls, id):
        data = {'id':id}
        query = """
        SELECT * FROM recipes
        WHERE id = %(id)s
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    # UPDATE 
    @classmethod
    def edit_recipe(cls, data):
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, under_30_min = %(under_30_min)s,
        date = %(date)s, instructions = %(instructions)s
        WHERE recipes.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # DELETE
    @classmethod
    def delete_recipe(cls, id):
        data = {'id': id}
        query = """
        DELETE FROM recipes
        WHERE id=%(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # VALIDATE
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Recipe name must be at least three characters long')
            is_valid = False
        if len(data['description']) < 3:
            flash('Recipe description must be at least three characters long')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Recipe instructions  must be at least three characters long')
            is_valid = False
        if data['date'] == "":
            flash('Please enter valid date')
            is_valid = False
        if data['under_30_min'] == "":
            flash('Must add a timeframe for the recipe')
            is_valid = False
        return is_valid