from project import app, db
from project.models import User, Like

app.app_context().push()
db.drop_all()
db.create_all()