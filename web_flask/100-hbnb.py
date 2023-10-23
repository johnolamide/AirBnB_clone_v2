#!/usr/bin/python3
""" Script starts a flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ prints the list of states in the storage
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template('100-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places)


@app.teardown_appcontext
def teardown_db(exception):
    """ teardown the db
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
