from flask import render_template, url_for, flash, redirect, request
from project import app, db, bcrypt
from project.forms import RegistrationForm, LoginForm, UpdateAccountForm
from project.models import User, Like
from flask_login import login_user, current_user, logout_user, login_required
import imdb, time, json, pickle


# Setter viktige variabler som zip setter flere iterable objekter sammen og hvor jeg henter filmer fra.
ia = imdb.Cinemagoer()


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    # API-en er ikke optimal så jeg valgte å laste inn forsiden ved å laste over filmene til en json så det ikke skulle ta så lang tid(15 sekunder)
    
    # Gir feil beskjed om den ikke klarer å åpne homepage.json
    try:
        with open('homepage.json', 'r') as f:
            data = json.load(f)
    except:
        flash('Unable to retrieve homepage images', 'error')

    return render_template('home.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
# Prøver å søke etter filmer, om det ikke går får vi feilmelding på siden og mer detaljer i terminalen.
    q = request.args.get('q')

    if q:
        try:
            results = ia.search_movie(q, results=20)
            return render_template('search.html', results=results, q=q)
        except Exception as e:
            print(e)
            flash("Sorry, an error ocurred while processing your request.", 'error')
            return redirect('home')
    
    return redirect('home')

# Bruker model funksjonen for å legge til likes, og lagrer url til bildene så det går raskere å laste dem inn senere :P
@app.route('/add-like', methods=['GET', 'POST'])
@login_required
def add_like():
    q = request.args.get('q')
    id = request.args.get('movie_id')
    title = request.args.get('title')
    image = request.args.get('image')
    current_user.add_like(id, title, image)
    return redirect(url_for('search', q=q, _anchor=id))

# Sletter like. Om bruker iden til Liken ikke er den samme som nåværende bruker så stopper den.
@app.route('/delete-like', methods=['GET', 'POST'])
@login_required
def delete_like():
    like_id = request.args.get('id')
    like = Like.query.get_or_404(like_id)
    if like.user_id != current_user.id:
        abort(403)
    db.session.delete(like)
    db.session.commit()
    return redirect(url_for("my_page"))

# Setter form = registrerings formen fra forms.py for å kunne bruke form.username.label, form.username etc i template.
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect("home")

# Da får vi den fine her som innholdet i formen er validert før koden under kjøres.
    if form.validate_on_submit():
        # Hasher passord
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        # Legger bruker til i databasen og commiter endringene.
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", 'success')
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect("home")

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Sjekker om det bcrypta passordet matcher med innholdet i form.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # For å redirecte til siden man hadde lyst å komme inn på, men ikke hadde tillatelse pga ikke logget inn.
            next_page = request.args.get("next")
            flash(f'Logged in as {current_user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Log in unsuccessful. Please check email and password", 'error')
            return redirect("login")

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
# Bestemmer at man må være logget inn for å komme inn.
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'error')
    return redirect("home")

@app.route("/my-page")
@login_required
def my_page():
    return render_template("mypage.html")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)

# Henter film fra get_movie for den hadde mer data en fra søker funksjonen.
@app.route("/title/<movie_id>", methods=["GET", "POST"])
def movie(movie_id):
    movie = ia.get_movie(movie_id)
    return render_template('movie.html', movie=movie, movie_id=movie_id)
