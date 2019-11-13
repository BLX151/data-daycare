# All of the imports required for blueprint pages
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from .db import db

daycare = Blueprint('daycare', __name__)

allDaycares = db.getDatabase()

@daycare.url_value_preprocessor

@daycare.route("/<daycare_index>")
def info(daycare_index):
    return render_template("daycare.html", daycare_info=allDaycares[daycare_index])