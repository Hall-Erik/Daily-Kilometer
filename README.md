# Daily-Kilometer

[![Build Status](https://travis-ci.org/Hall-Erik/Daily-Kilometer.svg?branch=master)](https://travis-ci.org/Hall-Erik/Daily-Kilometer)
[![Coverage Status](https://coveralls.io/repos/github/Hall-Erik/Daily-Kilometer/badge.svg?branch=master)](https://coveralls.io/github/Hall-Erik/Daily-Kilometer?branch=master)

A Django app for tracking my run mileage and times.

This is deployed on Heroku [here](https://dailykm.herokuapp.com/).

## Development server

### Backend

Open a terminal in the project root and run `pip install -r requirements.txt` to download dependencies.

Run `python manage.py migrate` to build a SQLite database.

You will need a Sendgrid account to get the email backend working. Follow directons on their website to get an api key for sending mail via SMTP and set environment variables for `SENDGRID_USER` and `SENDGRID_PASS`.

Run `python manage.py runserver` for a dev server. The app will automatically reload if you change any of the source files.

### Frontend

Open a terminal in the ng-frontend directory and run `npm install`

Run `npm start` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Docker Compose

Alternatively, you could just run the project in Docker.

Open a terminal in the project root and run `docker-compose build` to set up your containers.

Run `docker-compose up` to run the images.

Go to `http://localhost:1337/` in your browser.

## Running unit tests

Run `python manage.py test` to execute the tests.

## What I learned

* Django for web development
* Unit testing in Django
* CI/CD with Travis-ci, Heroku and GitHub
* Test coverage reporting with Coverage<span>.</span>py and Coveralls