#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkgutil
import importlib

from flask import Blueprint, redirect, url_for, session, abort
from functools import wraps

def user_required(f):
    """ Décorateur qui vérifie si un utilisateur est loggé et sinon redirige vers le CAS """

    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            assert(session["logged_in"] == True)
        except AssertionError:
            return redirect(url_for("cas.login"))
        except KeyError:
            return redirect(url_for("cas.login"))
        return f(*args, **kwargs)
    return decorator

def check_right(service):
    """ Décorateur qui vérifie si l'utilisateur a les droits sur le service et sinon renvoie un code 403

    Arguments :
    service -- service dont il faut vérifier les droits
    
    """
    def decorator(f):
        @wraps(f)
        def wrapping(*args, **kwargs):
            if service not in session["services"]:
                return abort(403)
            return f(*args, **kwargs)
        return wrapping
    return decorator
        
# Inspiré de https://github.com/mattupstate/overholt/blob/master/overholt/helpers.py (MIT license)
def register_blueprints(app, package_name=None, package_path="."):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    
    """
    
    for _, name, _ in pkgutil.iter_modules(package_path):
        import_string = '%s.%s' % (package_name, name) if package_name else name
        m = importlib.import_module(import_string)
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
