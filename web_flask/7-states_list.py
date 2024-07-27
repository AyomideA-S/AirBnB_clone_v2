#!/usr/bin/python3
"""
Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /states_list: HTML page with a list of all State objects in DBStorage.
"""
from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """ Displays an HTML page with a list of all State objects in DBStorage.
    States are sorted by name.
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy session.
    closes the storage on teardown
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
