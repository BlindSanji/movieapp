from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "Secret-key"

# Setter sqlite som database og kaller filen project.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# Henter database fra app som db
db = SQLAlchemy(app)

# Henter Bcrypt fra app som bcrypt
bcrypt = Bcrypt(app)

# Henter LoginManager fra app
login_manager = LoginManager(app)

# Setter log in vindu. 
# Hvis en rute har @LoginRequired og det ikke er en current_user vil man bli sendt hit til ruten 'login'
login_manager.login_view = 'login'

#Setter kategori for login meldinger.
login_manager.login_message_category = 'error'

from project import routes
