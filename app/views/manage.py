# -*- coding: utf-8 -*-
from os import path, remove
from datetime import datetime, timedelta

from flask import Blueprint
from flask import render_template
from flask import redirect, url_for

from app import db

from models import File

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_all_ctx():
    return File.query.all()


def get_file_by_idx(idx: str):
    return File.query.filter_by(
        idx=idx
    ).first()


@bp.route("/")
def index():
    return render_template(
        "manage/index.html",
        ctx=get_all_ctx()
    )


@bp.route("/run")
def run():
    for file in get_all_ctx():
        delete_time = file.upload + timedelta(days=1)
        now = datetime.now()

        if now >= delete_time:
            try:
                remove(path=path.join("upload", file.idx))
                db.session.delete(file)
                db.session.commit()
            except (FileNotFoundError, PermissionError, Exception):
                pass

    return redirect(url_for(".index"))
