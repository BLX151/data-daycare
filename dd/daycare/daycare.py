# All of the imports required for blueprint pages
from flask import Blueprint, render_template
from dd.db import db

daycare = Blueprint('daycare', 'daycare', url_prefix='/daycare')

@daycare.route("/")
def base():
    return render_template("daycare.html")

@daycare.route("/<daycare_index>")
def info(daycare_index):
    daycare_info = db.getDaycare( int(daycare_index) )
    return render_template("daycare.html", daycare_info=daycare_info, index=daycare_index)