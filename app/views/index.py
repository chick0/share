# -*- coding: utf-8 -*-

from flask import Blueprint, g, session
from flask import render_template

from config import MAX_FILE_SIZE


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/ok")
def ok():
    return "OK", 200


@bp.route("/")
def index():
    g.description = "쉽고 빠르게 파일을 공유해보세요"

    if not g.use_github:
        return render_template(
            "index/index.html",
            MAX_FILE_SIZE=MAX_FILE_SIZE
        )

    try:
        g.username = session['username']
    except KeyError:
        g.username = None

    return render_template(
        "index/index.html",
        MAX_FILE_SIZE=MAX_FILE_SIZE,
        LOGIN_URL=f"https://github.com/login/oauth/authorize"
                  f"?client_id={g.client_id}"
                  f"&scope=user:email",
    )
