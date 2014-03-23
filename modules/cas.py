#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, abort, request, session, flash, Blueprint
import conf
from helpers import user_required
from payutc import Payutc
from payutc_json_client import PayutcJsonClientError

bp = Blueprint('cas', __name__, url_prefix='/cas')

payutc = Payutc()

@bp.route('/login')
def login():
    """ Loggue un utilisateur sur le cas """
     
    if session.has_key('logged_in') and session["logged_in"]:
        return redirect(url_for("base.index"))

    payutc.set_cookie(None)
    if not request.args.get('ticket'):
        return redirect("%slogin?service=%s" % (payutc.get_cas_url(), conf.HOSTNAME + url_for('cas.login')))
    else:
        session['username'] = payutc.login(request.args.get('ticket'), conf.HOSTNAME + url_for('cas.login'))
        payutc.login_app()
        session['cookie'] = payutc.get_cookie()
        session['services'] = payutc.call("getEnabledServices")
        session['logged_in'] = True
        flash('Bienvenue', 'success')
        return redirect(url_for('base.index'))


@bp.route("/")
@user_required
def index():
    """ Page d'accueil """
    
    payutc.client.set_cookie(session["cookie"])
    username = session["username"]
    services = [implemented[service] for service in session["services"] if service in implemented]
    return render_template('index.html', **locals())


@bp.route("/logout")
@user_required
def logout():
    """ Déconnection du CAS """
    
    session["logged_in"] = False
    return redirect("%slogout/?url=%s" % (payutc.get_cas_url(), conf.HOSTNAME))
    

