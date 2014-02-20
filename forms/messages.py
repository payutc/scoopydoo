#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import Form, TextField, validators

class MessageChangeForm(Form):
    message = TextField('Message', [validators.Length(min=1, max=255)])
