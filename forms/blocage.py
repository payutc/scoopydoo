#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import Form, TextField, SelectField, validators

class BlockForm(Form):
    user = TextField('Login', [validators.Length(min=1, max=8)])
    raison = TextField('Raison', [validators.Length(min=1, max=255)])
    start = TextField(u'Début')
    end = TextField('Fin')

class BlockChangeForm(Form):
    raison = TextField('Raison', [validators.Length(min=1, max=255)])
    end = TextField('Date de fin', [validators.Length(min=1, max=255)])
