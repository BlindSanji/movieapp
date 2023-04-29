# movieapp

Once downloaded create a virtual enviorement in the folder:
    py -m venv venv

Iniziate it the venv:

cmd:
    venv\Scripts\activate.bat

Powershell:
    venv\Scripts\activate.ps1
    
Then download requirements:
    pip install -r requirements.txt
    
Now you can run the run.py file!
    
If you want to delete the database and start with a clean database type this in terminal:
    py
    from project import db, app
    from project.models import User, Like
    with app_context().push()
    db.drop_all()
    db.create_all()
    
