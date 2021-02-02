# -*- coding: utf-8 -*-
from os import path, listdir, remove
from hashlib import sha384
from datetime import datetime, timedelta

from flask import Blueprint
from flask import request

from app import db
from config import UPLOAD_FOLDER
from models import File

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

    for file in File.query.all():
        delete_time = file.upload + timedelta(days=1)
        now = datetime.now()

        if now >= delete_time:
            db.session.delete(file)
    db.session.commit()

    upload_idx = [ctx.idx for ctx in File.query.all()]
    for idx in listdir(UPLOAD_FOLDER):
        if idx not in upload_idx:
            remove(path.join(UPLOAD_FOLDER, idx))

    return "OK"
