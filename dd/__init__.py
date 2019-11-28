# import flask class Flask which contatins all of the internal 
# web server logic
from flask import Flask, render_template, url_for, request
from dd.db import db
from dd.daycare.daycare import daycare
import requests

app = Flask(__name__) # Instantiate a copy of the Flask class called app
app.register_blueprint(daycare) # Register the daycare blueprint into the app

def getUserGeoData():
    if request.remote_addr == '127.0.0.1':
        remote_ip = requests.get('https://get.geojs.io/v1/ip.json').json()['ip']
    else:
        remote_ip = request.remote_addr
    return requests.get('https://get.geojs.io/v1/ip/geo/' + remote_ip + '.json').json()

# Our base domain page, @app.route creates a webpage at
# www.ourdomain.com/<routename> which anyone can access
@app.route('/')
# The home route
@app.route('/home')
def home():
    nearby = db.getByDistance(25, 15, getUserGeoData())
    return render_template('home.html', nearby = nearby)
    # Return the html file to be displayed on the routed page
    # nearby variable will be availble to access inside the html file

# The map route
@app.route('/map', methods = ["POST", "GET"])
def map():
    filters = {}
    if (request.form.get('county') != "noSelection" and request.form.get('county') != None ):
        filters['county'] = request.form.get('county')
    if (request.form.get('city') != "noSelection" and request.form.get('city') != None):
        filters['city'] = request.form.get('city')
    if (request.form.get('min_capacity') != "" and request.form.get('min_capacity') != None ):
        filters['min_capacity'] = int(request.form.get('min_capacity'))
    if (request.form.get('max_capacity') != "" and request.form.get('max_capacity') != None ):
        filters['max_capacity'] = int(request.form.get('max_capacity'))
    if (request.form.get('age_infant') == "on"):
        filters['age_infant'] = "Yes"
    if (request.form.get('age_toddler') == "on"):
        filters['age_toddler'] = "Yes"
    if (request.form.get('age_preschool') == "on"):
        filters['age_preschool'] = "Yes"
    if (request.form.get('age_school_age') == "on"):
        filters['age_school_age'] = "Yes"
    if (request.form.get('prog_full_day') == "on"):
        filters['prog_full_day'] = "Yes"
    if (request.form.get('prog_part_day') == "on"):
        filters['prog_part_day'] = "Yes"
    if (request.form.get('annualInspection') == "on"):
        filters['annual_inspection'] = "Yes"
    if (request.form.get('unannouncedInspection') == "on"):
        filters['annual_unannounced_inspection'] = "Yes"

    # return filters

    if not filters:
        indexes = db.getDatabase()
    else:
        indexes = db.filterDaycares(filters)

    return render_template("map.html", database = indexes)
    # database variable will be accessable from within map.html

@app.route('/directory', methods = ["POST", "GET"])
def directory():
    filters = {}
    if (request.form.get('county') != "noSelection" and request.form.get('county') != None ):
        filters['county'] = request.form.get('county')
    if (request.form.get('city') != "noSelection" and request.form.get('city') != None):
        filters['city'] = request.form.get('city')
    if (request.form.get('min_capacity') != "" and request.form.get('min_capacity') != None ):
        filters['min_capacity'] = int(request.form.get('min_capacity'))
    if (request.form.get('max_capacity') != "" and request.form.get('max_capacity') != None ):
        filters['max_capacity'] = int(request.form.get('max_capacity'))
    if (request.form.get('age_infant') == "on"):
        filters['age_infant'] = "Yes"
    if (request.form.get('age_toddler') == "on"):
        filters['age_toddler'] = "Yes"
    if (request.form.get('age_preschool') == "on"):
        filters['age_preschool'] = "Yes"
    if (request.form.get('age_school_age') == "on"):
        filters['age_school_age'] = "Yes"
    if (request.form.get('prog_full_day') == "on"):
        filters['prog_full_day'] = "Yes"
    if (request.form.get('prog_part_day') == "on"):
        filters['prog_part_day'] = "Yes"
    if (request.form.get('annualInspection') == "on"):
        filters['annual_inspection'] = "Yes"
    if (request.form.get('unannouncedInspection') == "on"):
        filters['annual_unannounced_inspection'] = "Yes"

    # return filters

    if not filters:
        indexes = db.getDatabase()
    else:
        indexes = db.filterDaycares(filters)

    return render_template("directory.html", database = indexes)

# The about route
@app.route('/about')
def about():
    return render_template('about.html')
