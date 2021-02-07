# -*- coding: utf-8 -*-
from hashlib import sha384

from flask import Blueprint
from flask import request

from app.module.clean import db_remove, file_remove


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("")
def clean():
    with open(".SECRET_KEY", mode="rb") as fp:
        if request.headers.get("Secret-Key") != sha384(fp.read()).hexdigest():
            return "Invalid Secret-Key", 403

    db_remove()
    file_remove()

    return "OK"
