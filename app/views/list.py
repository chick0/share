# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template

from models import File

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_all_ctx():
    return File.query.all()


@bp.route("/")
def index():
    return render_template(
        "list/index.html",
        ctx=get_all_ctx()
    )
