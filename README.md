# Warbler

## Setup
Create the Python virtual environment:

`$ python3 -m venv venv`

Activate virtual environment:
`$ source venv/bin/activate`

Install dependencies:
`(venv) $ pip install -r requirements.txt`


## Set up the database:

`(venv) $ createdb warbler`
`(venv) $ python seed.py`


## Start the server:

Activate virtual environment:
`$ source venv/bin/activate`
`(venv) $ flask run`

## View site:

Browser URL: localhost:5000


## Tests

### Run model tests:

`FLASK_ENV=production python -m unittest <name-of-python-file>`

### Run route/view functions:

`python -m unittest test_user_model.py`
