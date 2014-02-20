#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from payutc import Payutc
from payutc_json_client import PayutcJsonClientError
from forms.blocage import BlockForm, BlockChangeForm
from helpers import user_required, check_right

bp = Blueprint('blocage', __name__, url_prefix='/blocage')

payutc = Payutc("BLOCKED")
     
@bp.route('/')
@user_required
@check_right("BLOCKED")
def index():
     payutc.set_cookie(session["cookie"])
     username=session["username"]
     funs = payutc.get_funs()
     
     for fun in range(len(funs)):
          funs[fun]["blocked"] = payutc.call("getAll", fun_id=funs[fun]["fun_id"])
     form = BlockForm()

     start_placeholder = u"Dès maintenant"
     end_placeholder = u"À tout jamais"

     return render_template('blocage/index.html', **locals())

@bp.route('/block/<int:fun>', methods=['POST'])
@user_required
@check_right("BLOCKED")
def block(fun):
     payutc.set_cookie(session["cookie"])
     username = session["username"]
     form = BlockForm(request.form)

     if form.validate():
          usr_id = None
          
          try:
               usr_id = payutc.call("getUserId", login=form.user.data)
          except PayutcJsonClientError:
               flash(u'Utilisateur inexistant', 'danger')
               return redirect(url_for('blocage.index'))

          try:
               payutc.call("block", usr_id=usr_id, fun_id=fun, raison=form.raison.data)
               flash(u'Utilisateur bloqué', 'success')
          except PayutcJsonClientError:
               flash(u'Échec dans le blocage', 'danger')
     else:
          flash(u'Formulaire mal rempli', 'danger')
     return redirect(url_for('blocage.index'))


@bp.route('/change/<int:fun>/<int:blo>', methods=["GET", "POST"])
@user_required
@check_right("BLOCKED")
def change(fun, blo):
     username = session["username"]
     payutc.set_cookie(session["cookie"])

     form = BlockChangeForm(request.form)

     if request.method == 'POST' and form.validate():
          
          try:
               date = datetime.strptime(form.end.data, '%Y-%m-%d %H:%M:%S')
          except ValueError:
               flash(u"Format de date de fin incorrecte", "danger")
               return redirect(url_for('blocage.change', fun=fun, blo=blo))
          try:
               payutc.call("edit", blo_id=blo, fun_id=fun, raison=form.raison.data, date_fin=form.end.data)
          except PayutcJsonClientError:
               flash(u'Échec dans le changement du blocage', 'danger')

          return redirect(url_for('blocage.index'))
          
     elif request.method == 'POST':
          flash(u"Formulaire non valide", "danger")
          return redirect(url_for('blocage.change', fun=fun, blo=blo))
     else:
          blocage = ""
          try:
               blocage = payutc.call("getAll", fun_id=fun)[str(blo)]
          except PayutcJsonClientError:
               flash(u'Insuffisance de droits', 'danger')
               return redirect(url_for('blocage.index'))
          except KeyError:
               flash(u'Blocage inexistant', 'danger')
               return redirect(url_for('blocage.index'))
               
          if blocage["blo_removed"]:
               form = BlockChangeForm(raison=blocage["blo_raison"], end=blocage["blo_removed"])
          else:
               form = BlockChangeForm(raison=blocage["blo_raison"])
               
          return render_template('blocage/change.html', **locals())

@bp.route('/remove/<int:fun>/<int:blo>')
@user_required
@check_right("BLOCKED")
def remove(fun, blo):
     payutc.set_cookie(session["cookie"])
     try:
          payutc.call("remove", fun_id=fun, blo_id=blo)
          flash(u'Débloqué avec avec succès', 'success')
     except PayutcJsonClientError:
          flash(u'Échec dans le déblocage', 'danger')
     return redirect(url_for('blocage.index'))



