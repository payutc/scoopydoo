#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from payutc import Payutc
from payutc_json_client import PayutcJsonClientError
from forms.articles import AddCategoryForm, AddArticleForm
from helpers import user_required, check_right

bp = Blueprint('articles', __name__, url_prefix='/articles')

payutc = Payutc("GESARTICLE")
     
@bp.route('/')
@user_required
@check_right("GESARTICLE")
def index():
    """ Index de la gestion des articles, permet de choisir une fundation si l'utilisateur a le choix parmi plusieurs,
    sinon renvoie vers la gestion de la fundation directement
    
    """  
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    funs = payutc.get_funs()
    if (len(funs) == 1):
        return redirect(url_for("articles.fundation", fun=funs[0]["fun_id"]))
    return render_template('articles/index.html', **locals())

@bp.route('/<int:fun>')
@user_required
@check_right("GESARTICLE")
def fundation(fun):
    """ Gestion des articles d'une fundation, permet l'ajout de catégories et d'articles

    Arguments :
    fun -- id de la fundation concernée
    
    """  
    payutc.set_cookie(session["cookie"])
    username = session["username"]
    fundation = [f for f in payutc.get_funs() if f["fun_id"] == fun][0]
    categories = payutc.call("getCategories", fun_id=fun)
    products = payutc.call("getProducts", fun_id=fun)
    products_by_cat = {}

    for i, cat in enumerate(categories):
        products_by_cat[cat["id"]] = [p for p in products if p["categorie_id"] == cat["id"]]

    category_choices = []

    if len(categories) > 0:
        category_choices = [(c["id"], c["name"]) for c in categories]
        
    category_choices.append(("0", "Racine"))

    form_category = AddCategoryForm()
    form_article = AddArticleForm()

    form_category.parent.choices = form_article.parent.choices = category_choices

    return render_template('articles/fundation.html', **locals())

@bp.route('/<int:fun>/add/article/', methods=["POST"])
@user_required
@check_right("GESARTICLE")
def add_article(fun):
    """ Ajout d'un article, accessible suite a une requête POST 

    Arguments :
    fun -- id de la fundation concernée
    (nécessité d'un formulaire AddArticleForm bien rempli)
    
    """ 
    payutc.set_cookie(session["cookie"])
    username = session["username"]

    form = AddArticleForm(request.form)

    if form.validate:

        if form.stock.data is None:
            form.stock.data = "0"

        parent = ""
        
        if form.parent.data != "0":
            parent = form.parent.data

        res = {}
            
        try:
            res = payutc.call("setProduct", fun_id=fun, name=form.name.data, prix=form.price.data, stock=form.stock.data, image="", alcool=False, parent=form.parent.data)
            assert("success" in res.keys())
        except AssertionError:
            flash(res["error_msg"], "danger")
            return redirect(url_for("articles.fundation", fun=fun))
        except PayutcJsonClientError:
            flash(u"Échec dans la communication avec payutc", "danger")
            return redirect(url_for("articles.fundation", fun=fun))
        flash(u"Article ajouté", "success")
    else:
        flash(u"Formulaire invalide", "danger")

    return redirect(url_for("articles.fundation", fun=fun))
    
@bp.route('/<int:fun>/add/category/', methods=["POST"])
@user_required
@check_right("GESARTICLE")
def add_category(fun):
    """ Ajout d'une catégorie, accessible suite a une requête POST 

    Arguments :
    fun -- id de la fundation concernée
    (nécessité d'un formulaire AddCategoryForm bien rempli)
    
    """ 
    payutc.set_cookie(session["cookie"])
    username = session["username"]

    form = AddCategoryForm(request.form)

    if form.validate:
        parent = ""
        
        if form.parent.data != "0":
            parent = form.parent.data
            
        res = {}
            
        try:
            res = payutc.call("setCategory", fun_id=fun, name=form.name.data, parent_id=parent)
            assert("success" in res.keys())
        except AssertionError:
            flash(res["error_msg"], "danger")
            return redirect(url_for("articles.fundation", fun=fun))
        except PayutcJsonClientError:
            flash(u"Échec dans la communication avec payutc", "danger")
            return redirect(url_for("articles.fundation", fun=fun))
            
        flash(u"Catégorie ajouté", "success")
    else:
        flash(u"Formulaire invalide", "danger")

    return redirect(url_for("articles.fundation", fun=fun))

@bp.route('/<int:fun>/del/article/<int:art>')
@user_required
@check_right("GESARTICLE")
def del_article(fun, art):
    """ Suppression d'un article

    Arguments :
    fun -- id de la fundation concernée
    art -- id de l'article
    
    """
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]

    res = {}
    
    try:
        res = payutc.call("deleteProduct", fun_id=fun, obj_id=art)
        assert("success" in res.keys())
    except AssertionError:
        flash(res["error_msg"], "danger")
        return redirect(url_for("articles.fundation", fun=fun))
    except PayutcJsonClientError:
        flash(u"Échec dans la communication avec payutc", "danger")
        return redirect(url_for("articles.fundation", fun=fun))
    flash(u"Article supprimé", "success")

    return redirect(url_for('articles.fundation', fun=fun))

@bp.route('/<int:fun>/del/category/<int:cat>')
@user_required
@check_right("GESARTICLE")
def del_category(fun, cat):
    """ Suppression d'une catégorie

    Arguments :
    fun -- id de la fundation concernée
    cat -- id de la catégorie
    
    """
    
    payutc.set_cookie(session["cookie"])
    username = session["username"]

    res = {}
    
    try:
        res = payutc.call("deleteCategory", fun_id=fun, obj_id=cat)
        assert("success" in res.keys())
    except AssertionError:
        flash(res["error_msg"], "danger")
        return redirect(url_for("articles.fundation", fun=fun))
    except PayutcJsonClientError:
        flash(u"Échec dans la communication avec payutc", "danger")
        return redirect(url_for("articles.fundation", fun=fun))
    flash(u"Catégorie supprimé", "success")

    return redirect(url_for('articles.fundation', fun=fun))






