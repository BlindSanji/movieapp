from flask import render_template, url_for, flash, redirect, request
from project import app, db, bcrypt
from project.forms import RegistrationForm, LoginForm, UpdateAccountForm, SearchForm
from project.models import User, Product
from flask_login import login_user, current_user, logout_user, login_required
from project.mysecrets import apikey
import requests, json
import json

querystring={"q": "game"}

url = "https://imdb8.p.rapidapi.com/auto-complete"

headers = {
    "X-RapidAPI-Key": apikey,
    "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()

    if form.validate_on_submit():
        search_query = form.search.data
        return redirect(url_for("search", search_query=search_query))

    return render_template('home.html', title="Home", form=form)

@app.route('/search/<search_query>', methods=['GET', 'POST'])
def search(search_query):
    form = SearchForm()

    if form.validate_on_submit():
        search_query = form.search.data
        return redirect(url_for('search', search_query=search_query))

    if search_query:
        search_query = search_query.strip()
        q = {"q": search_query}
        response = requests.request("GET", url, headers=headers, params=q)
        result = response.json()

    return render_template('search.html', title=search_query, form=form, search_query=search_query, result=result)



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("home")
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("home")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Log in unsuccessful. Please check email and password", "class")
        return redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("home")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "class")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form = form)

from flask_login import current_user, login_required

# @app.route('/<username>/likes')
# @login_required
# def show_likes(username):
#     if current_user.username != username:
#         abort(403)

#     likes = current_user.get_variables_list()
#     return render_template('likes.html', likes=likes)