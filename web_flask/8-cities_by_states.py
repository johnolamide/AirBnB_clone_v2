#!/usr/bin/python3
""" Script starts a flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """ prints the list of states in the storage
    """
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html',
                           states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """ teardown the db
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
