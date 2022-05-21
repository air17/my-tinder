# myTinder
Backend for a Tinder-like app.

## Install

1. Install `python3`

2. Install dependencies: `pip install -r requirements.txt`

3. Create `my.cnf` file and add your MySQL DB credentials. (or just rename `my.cnf.example` to `my.cnf` for test db)

4. Run `python manage.py makemigrations`

5. Run `python manage.py migrate`

6. Start the server: `python manage.py runserver`

## API Endpoints

1. Register a new user: `POST /api/clients/create`
2. Like user and check for match `POST /api/clients/{id}/match`
3. List of users `GET /api/list`
4. User info `GET api/clients/{id}`
5. Change user location `PUT clients/{id}/location/`
6. Retrieve JWT `GET api/token` (you can use basic auth as well)
7. Refresh JWT `GET api/token`
