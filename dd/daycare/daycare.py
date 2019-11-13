# All of the imports required for blueprint pages
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from ..db import db

daycare = Blueprint('daycare', 'daycare', url_prefix='/daycare')

# daycare_info = db.getDaycare(0)
daycare_info = None

@daycare.route("/")
def base():
    print("daycare")
    return render_template("daycare.html")

@daycare.route("/<daycare_index>")
def info(daycare_index):
    # print(daycare_index)
    daycare_info = db.getDaycare(daycare_index)
    # return render_template("daycare.html", daycare_info=daycare_info, index=daycare_index)
    return daycare_info["facility_name"]