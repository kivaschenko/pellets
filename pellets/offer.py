# import built-in libraries

from datetime import datetime

# third party imports
import psycopg2
from flask import (
    request,
    render_template,
    redirect,
    jsonify,
    flash,
    g,
    url_for,
    Blueprint
)
from werkzeug.exceptions import abort 

# import from the app
from . import config


#======================
# CONSTANTS
INCOMING_DATE_FMT ='%Y-%m-%d %H:%M:%S'

bp = Blueprint('offer', __name__)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@bp.route('/')
def home():
    return render_template('offer/home.html')


@bp.route('/map')
def map(request):
    return render_template('offer/map.html')


@bp.route('/offer-list')
def offer_list():
    return render_template('offer/table.html')


