#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from helpers import register_blueprints
import conf

def create_app():

    app = Flask(__name__)
    register_blueprints(app)
    register_blueprints(app, "modules", ["modules"])
    app.secret_key = conf.SECRET

    @app.errorhandler(403)
    def unauthorized(error):
        return render_template("errors/403.html")

    return app
