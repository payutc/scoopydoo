#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import Form, TextField, SelectField, validators

class AddUserForm(Form):
    user = TextField('Login', [validators.Length(min=1, max=8)])
    service = TextField('Service', [validators.Length(min=1, max=20)])
