#!/usr/bin/python3
""" Script starts a Flask web application
"""
from flask import Flask, render_template
from markupsafe import escape


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Return "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Return "HBNB"
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """ Return "C <text>"
    """
    text = text.replace('_', ' ')
    return f"C {escape(text)}"


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """ Return "Python <text>"
    """
    text = text.replace('_', ' ')
    return f"Python {escape(text)}"


@app.route('/number/<int:n>', strict_slashes=False)
def number_n(n):
    """ display 'n' if it is an integer
    """
    return f"{escape(n)} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ render a template with the number passed
    """
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """ checks if n is odd or even and renders the template
        accordingly
    """
    check = "odd"
    if (n % 2 == 0):
        check = "even"
    return render_template('6-number_odd_or_even.html', number=n, check=check)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
