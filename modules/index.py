#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, session, Blueprint
from helpers import user_required
from payutc import Payutc
import conf

bp = Blueprint('base', __name__, url_prefix='/')

payutc = Payutc()

implemented = conf.IMPLEMENTED

@bp.route("/")
@user_required
def index():

    """ Page d'accueil de scoopydoo """
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    services = [implemented[service] for service in session["services"] if service in implemented]
    return render_template('index.html', **locals())


