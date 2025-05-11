# The Green Economics

a Django app for the Green Economics project

## Requirements

In development, you will need to have Python 3.11+ and Node.js 20+ installed.

## Settings



## Basic Commands

### Apply Migrations

In development, you will need to run migrations to create the database tables:

    $ python manage.py migrate

You can also update the migrations:

    $ python manage.py makemigrations

### Run the Server

After you have installed the requirements for local development, you can run the server:

    $ python manage.py runserver

Then go to http://127.0.0.1:8000/ in your browser.

### Collect Static Files

Collect static files:

    $ python manage.py collectstatic


### tailwind watch

To watch for changes in the tailwind.css file and compile it to static/css/main.css:

    $ python manage.py tailwind start

This will start the tailwind compiler in watch mode. Any changes to the tailwind.css file will trigger a recompile.

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.


## development

### linting
linting with ruff:

    $ ruff .

### Type checks

Running type checks with mypy:

    $ mypy the_green_economics

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

## Deployment

### Install dependencies

Install the dependencies for the production environment:

    $ pip install -r requirements/production.txt

### Create the database

Create the database:

    $ python manage.py migrate


### Collect static files
Collect static files:

    $ python manage.py collectstatic --noinput


### compress static files
Precompile assets:

    $ python manage.py compress


### run the server
Run the server:

    $ gunicorn config.wsgi --bind 0.0.0.0:8000 --workers=4 --threads=1 --timeout 100