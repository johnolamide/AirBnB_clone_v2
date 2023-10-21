#!/usr/bin/python3
""" Script starts a flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/states', strict_slashes=False)
def states():
    """ prints the list of states in the storage
    """
    states = storage.all(State).values()
    return render_template('9-states.html',
                           states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """ display specific state from id
    """
    states = storage.all(State).values()
    return render_template('9-states.html',
                           states=states, id=id)


@app.teardown_appcontext
def teardown_db(exception):
    """ teardown the db
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
