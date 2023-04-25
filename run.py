from project import app

if __name__ == "__main__":
    app.run(debug=True)

# For å slette data i databasen, skriv dette i terminalen:
# python
# from project import app, db
# from project.models import User
# app.app_context().push()
# db.drop_all()
# db.create_all()