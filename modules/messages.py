#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from payutc import Payutc
from payutc_json_client import PayutcJsonClientError
from forms.messages import MessageChangeForm
from helpers import user_required, check_right

bp = Blueprint('messages', __name__, url_prefix='/messages')

@bp.route('/')
@user_required
@check_right("MESSAGES")
def index():

     """ Index de la gestion des messages """
    
     username=session["username"]
     payutc = Payutc("MESSAGES")
     payutc.set_cookie(session["cookie"])
     funs = payutc.get_funs()
     for i, fun in enumerate(funs):
          funs[i]["message"] = payutc.call("getMsg", usr_id=None, fun_id=fun["fun_id"])
     return render_template('messages/index.html', **locals())

@bp.route('/change/<int:fun>', methods=['GET', 'POST'])
@user_required
@check_right("MESSAGES")
def change(fun):

     """ Change le message d'une fundation

    Arguments :
    fun -- id de la fundation concernée
    (nécessite un MessageChangeForm valide)
    
    """
     payutc = Payutc("MESSAGES")
     payutc.set_cookie(session["cookie"])
     funs = payutc.get_funs()
     fundation = [f for f in funs if f["fun_id"] == fun][0]
     username = session["username"]
     form = MessageChangeForm(request.form)
     if request.method == 'POST' and form.validate():
          try:
               payutc.call("changeMsg", usr_id="", fun_id=fun, message=form.message.data)
               flash(u'Message changé', 'success')
          except PayutcJsonClientError:
               flash(u'Échec dans le changement du message', 'danger')
          return redirect(url_for('messages.index'))
     return render_template('messages/change.html', **locals())


