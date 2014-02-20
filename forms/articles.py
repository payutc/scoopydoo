#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import Form, TextField, SelectField, IntegerField, BooleanField, validators

class AddCategoryForm(Form):
    name = TextField('Nom', [validators.Length(min=1, max=8)])
    parent = SelectField(u'Catégorie parente')

class AddArticleForm(Form):
    name = TextField('Nom', [validators.Length(min=1, max=8)])
    parent = SelectField(u'Catégorie parente')
    price = IntegerField(u'Prix (en cts)')
    stock = IntegerField(u'Nombre en stock')
