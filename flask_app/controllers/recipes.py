from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


# CREATE
@app.route('/recipes/create', methods  = ['POST','GET'])
def create_recipe():
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('create_recipe.html')
        if Recipe.create_recipe(request.form):
            return redirect('/users/profile')
        else:
            return redirect('/recipes/create')
    return redirect('/')


# READ 
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('edit_recipe.html', recipe = Recipe.recipe_info(id))

@app.route('/recipes/view/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.recipe_info(id)
    user = User.get_user_by_id(id)
    return render_template('view_recipe.html', recipe = recipe, user = user)

# UPDATE 
@app.route('/recipes/update', methods = ['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/create')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'date': request.form['date'],
        'under_30_min': request.form['under_30_min'],
        'instructions' : request.form['instructions'],
        'id': session['user_id']
    }
    Recipe.edit_recipe(data)
    return redirect('/users/profile')

# DELETE
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    Recipe.delete_recipe(id)
    return redirect('/users/profile')