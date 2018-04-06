# Spoken-Tutorial
Every contributor is assigned one FOSS series for translation and dubbing process. Each FOSS has 10 tutorials. Admin has already decided deadlines for submission, which are stored in tutorial_detail table.

# Requirements
Python 3.6
Django==2.0.3

# How to run it?
Install virtualenv $ sudo apt install python-virtualenv
Create a virtual environment $ virtualenv env -p python3
Activate the env: $ source env/bin/activate
Change directory to spokentut $ cd spokentut
Make migrations $ python manage.py makemigrations
Migrate the changes to the database $ python manage.py migrate
Run the server $ python manage.py runserver
