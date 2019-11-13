# import flask class Flask which contatins all of the internal 
# web server logic
from flask import Flask, render_template, url_for, request
from .db import db

# Instantiate a copy of the Flask class called app
app = Flask(__name__)

# Our base domain page, @app.route creates a webpage at
# www.ourdomain.com/<routename> which anyone can access
@app.route('/')
def default(): # Function linked to the routed webpaged
    # Return the html file to be displayed on the routed page
    return render_template('home.html', nearby = db.getXElements(5), recent = db.getXElements(3))

# Routes /about as a webpage, returns the about.html template
@app.route('/about')
def about():
    return render_template('about.html')

from .daycare import daycare
app.register_blueprint(daycare, url_prefix="/daycare")



