#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, session, Blueprint
from helpers import user_required, check_right
from payutc import Payutc
import conf

bp = Blueprint('vente', __name__, url_prefix='/vente')

payutc = Payutc()

implemented = conf.IMPLEMENTED

@bp.route("/")
@user_required
@check_right("POSS3")
def index():
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    services = [implemented[service] for service in session["services"] if service in implemented]
    return render_template('vente/index.html', **locals())


