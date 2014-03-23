#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from payutc import Payutc
from payutc_json_client import PayutcJsonClientError
from forms.droits import AddUserForm
from helpers import user_required, check_right

bp = Blueprint('droits', __name__, url_prefix='/droits')

payutc = Payutc("ADMINRIGHT")
     
@bp.route('/')
@user_required
@check_right("ADMINRIGHT")
def index():
    """ Index de la gestion des droits, permet la sélection de la fundation sur laquelle on veut agir """
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    funs = payutc.get_funs()
    
    if (len(funs) == 1):
        return redirect(url_for("droits.fundation", fun=funs[0]["fun_id"]))
    return render_template('droits/index.html', **locals())

@bp.route('/<int:fun>')
@user_required
@check_right("ADMINRIGHT")
def fundation(fun):
    """ Page de gestion des droits sur une fundation

    Arguments :
    fun -- id de la fundation concernée
    
    """
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    fundation = [f for f in payutc.get_funs() if f["fun_id"] == fun][0]
    users = payutc.call("getUserRights", fun_id=fun)
    services = [s for s in payutc.call("getServices") if s["user"] and s["service"]]
    form = AddUserForm()
    
    return render_template('droits/fundation.html', **locals())

@bp.route('/<int:fun>/<int:usr>')
@user_required
@check_right("ADMINRIGHT")
def user(fun, usr):
    """ Page de gestion des droits pour un utilisateur dans un fun

    Arguments :
    fun -- id de la fundation concernée
    usr -- id de l'utilisateur
    
    """
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    fundation = [f for f in payutc.get_funs() if f["fun_id"] == fun][0]
    user = [u for k, u in payutc.call("getUserRights", fun_id=fun).items() if u["usr_id"] == str(usr)]

    #Si on a supprimé le dernier droit d’un user, on a rien en retour de getUserRights
    if len(user) == 0:
        return redirect(url_for("droits.fundation", fun=fun))
        
    user = user[0]
    authorized = [s["service"] for s in user["service"]]
    services = [s for s in payutc.call("getServices") if s["user"] and s["service"]]
    
    return render_template('droits/user.html', **locals())

@bp.route('/add/<int:fun>/<int:usr>/<string:service>')
@user_required
@check_right("ADMINRIGHT")
def add(fun, usr, service):
    """ Ajoute un droit (service) sur un utilisateur dans une fun qui a déja des droits (!)

    Arguments :
    fun -- id de la fundation concernée
    usr -- id de l'utilisateur concerné
    service -- droit a donner
    
    """
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    try:
        payutc.call("setUserRight", usr_id=usr, fun_id=fun, service=service)
        session["services"] = payutc.call("getEnabledServices")
        flash(u"Droit ajouté", "success")
    except PayutcJsonClientError:
        flash("Erreur dans la création du droit", "danger")
    return redirect(url_for("droits.user", fun=fun, usr=usr))

@bp.route('/del/<int:fun>/<int:usr>/<string:service>')
@user_required
@check_right("ADMINRIGHT")
def delete(fun, usr, service):
    """ Supprime un droit (service) sur un utilisateur dans une fun

    Arguments :
    fun -- id de la fundation concernée
    usr -- id de l'utilisateur concerné
    service -- droit a donner
    
    """
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    try:
        payutc.call("removeUserRight", usr_id=usr, fun_id=fun, service=service)
        session["services"] = payutc.call("getEnabledServices")
        flash(u"Droit supprimé", "info")
    except PayutcJsonClientError:
        flash("Erreur dans la création du droit", "danger")
    return redirect(url_for("droits.user", fun=fun, usr=usr))

@bp.route('/create/<int:fun>/', methods=["POST"])
@user_required
@check_right("ADMINRIGHT")
def create(fun):
    """ Crée un droit (service) sur un utilisateur dans une fun qui n'a aucun droit sur la fun

    Arguments :
    fun -- id de la fundation concernée
    usr -- id de l'utilisateur concerné
    service -- droit a donner
    
    """
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]

    form = AddUserForm(request.form)

    usr_id = None
        
    try:
        usr_id = payutc.call("getUserId", login=form.user.data)
    except PayutcJsonClientError:
        flash(u"Utilisateur inconnu", "danger")
        return redirect(url_for("droits.fundation", fun=fun))
            
    if form.validate():
        try:
            payutc.call("setUserRight", usr_id=usr_id, fun_id=fun, service=form.service.data)
            flash(u"Droit ajouté", "success")
        except PayutcJsonClientError:
            flash(u"Échec dans la création du droit", "danger")

    else:
        flash(u"Formulaire incorrect", "danger")

    return redirect(url_for("droits.fundation", fun=fun))




