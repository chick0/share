# -*- coding: utf-8 -*-
from hashlib import sha384
from urllib.error import HTTPError

from flask import Blueprint, g
from flask import request, session
from flask import redirect, url_for
from flask import render_template

from app import db
from models import File
from app.module import api

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/callback")
def callback():
    if not g.use_github:
        return redirect(url_for("index.index"))

    code = request.args.get("code")
    if code is None:
        return redirect(url_for("index.index"))

    try:
        token = api.get_access_token(code=code)
        session['access_token'] = token['access_token']
        user_data = api.get_user_data(access_token=session['access_token'])

        session['login'] = user_data['login']
        session['email'] = sha384(user_data['email'].encode()).hexdigest()
        session['username'] = user_data['name']

        return redirect(url_for("index.index"))
    except (HTTPError, KeyError):
        return redirect(url_for("index.index"))


@bp.route("/dashboard")
def dashboard():
    if not g.use_github:
        return redirect(url_for("index.index"))

    try:
        username = session['username']
        email = session['email']
        print(email)
    except KeyError:
        return redirect(url_for("index.index"))

    ctx = File.query.filter_by(
        email=email
    ).all()

    return render_template(
        "github/dashboard.html",
        username=username,
        ctx=ctx
    )


@bp.route("/detail/<string:idx>")
def detail(idx: str):
    if not g.use_github:
        return redirect(url_for("index.index"))

    try:
        username = session['username']
        email = session['email']
    except KeyError:
        return redirect(url_for("index.index"))

    ctx = File.query.filter_by(
        idx=idx,
        email=email
    ).first()

    if ctx is None:
        return redirect(url_for(".dashboard"))

    return render_template(
        "github/detail.html",
        username=username,
        ctx=ctx
    )


@bp.route("/delete/<string:idx>")
def delete(idx: str):
    if not g.use_github:
        return redirect(url_for("index.index"))

    try:
        email = session['email']
    except KeyError:
        return redirect(url_for("index.index"))

    File.query.filter_by(
        idx=idx,
        email=email
    ).delete()
    db.session.commit()

    return redirect(url_for(".dashboard"))


@bp.route("/renew/<string:idx>")
def renew(idx: str):
    if not g.use_github:
        return redirect(url_for("index.index"))

    try:
        email = session['email']
    except KeyError:
        return redirect(url_for("index.index"))

    ctx = File.query.filter_by(
        idx=idx,
        email=email
    ).first()

    if ctx is None:
        return redirect(url_for(".dashboard"))

    if ctx.delete < 14:
        ctx.delete = ctx.delete + 1
    db.session.commit()

    return redirect(url_for(".detail", idx=idx))
