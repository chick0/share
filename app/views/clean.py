# -*- coding: utf-8 -*-
from os import path, listdir, remove
from datetime import datetime, timedelta

from flask import Blueprint

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
