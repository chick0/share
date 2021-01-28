# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template

from config import MAX_FILE_SIZE

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/")
def index():
    return render_template(
        "index/index.html",
        MAX_FILE_SIZE=MAX_FILE_SIZE
    )
