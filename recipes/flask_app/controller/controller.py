from flask import render_template, flash,request, redirect, session
from flask_app import app
from flask_app.model.users import Users
from flask_app.model.recipes import Recipes
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    recipes = Recipes.all_recipes()
    return render_template("dashboard.html", all_recipes = recipes)

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/create_recipe')
def new_recipe():
    return render_template("new_recipe.html")

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    if not Recipes.validate_recipe(request.form):
        return redirect('/create_recipe')
    data={
        "user_id" : session['user_id'],
        "name" : request.form['txt-name'],
        "description" :request.form['txt-description'],
        "instructions" : request.form['txt-instructions'],
        "date": request.form['txt-date'],
        "status" : request.form['txt-status'],
    }
    Recipes.add_recipe(data)
    return redirect('/dashboard')

@app.route('/register_user', methods=['POST'])
def register_user():
     if not Users.validate_user(request.form):
        return redirect('/')
     pw_hash = bcrypt.generate_password_hash(request.form["txt-pword"])
     data={
         "fname": request.form['txt-fname'],
         "lname": request.form['txt-lname'],
         "email": request.form['txt-email'],
         "pword": pw_hash
     }
     Users.add_users(data)
     flash("Successfully Registered!")
     return redirect('/')

@app.route('/login_user', methods=['POST'])
def login_user():
    data = {
        "email" : request.form["txt-email"]
    }
    user_in_db = Users.login_user(data)
    print(user_in_db)
    if not user_in_db:
        flash("Invalid Username or Password")
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.pword,  request.form["txt-pword"]):
        flash("Invalid Username or Password")
        return redirect('/')

    session['user_id'] = user_in_db.id
    session['user_fname'] = user_in_db.fname
    Users.login_user(data)
    return redirect('/dashboard')
