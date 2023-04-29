# movieapp

1. Når du har lastet ned filene, opprett et virtuelt miljø i mappen:

py -m venv venv

2. Aktiver det virtuelle miljøet:

Kommandovindu:
venv\Scripts\activate.bat

Powershell:
venv\Scripts\Activate.ps1

3. Deretter last ned kravene:

pip install -r requirements.txt

4. Nå kan du kjøre run.py-filen!

Hvis du vil slette databasen og starte med en ren database, skriv dette i terminalen:
`
        py``
        from project import db, app``
        from project.models import User, Like`` 
        with app.app_context().push():``
            db.drop_all()``
            db.create_all()``
`
