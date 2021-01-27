# -*- coding: utf-8 -*-
from os import path
from uuid import uuid4
from hashlib import md5
from functools import reduce

from flask import Blueprint
from flask import abort, request, g
from flask import redirect, url_for
from flask import render_template
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

from app import db
from config import UPLOAD_FOLDER, MAX_FILE_SIZE, MAX_UPLOAD_SIZE
from models import File

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_all_size():
    return reduce(lambda old, now: old + now, [ctx.size for ctx in File.query.all()])


def upload_file():
    g.idx = str(uuid4())

    if g.idx not in [ctx.idx for ctx in File.query.all()]:
        try:
            ctx = File(
                idx=g.idx,
                md5=g.md5,
                filename=g.filename,
                size=g.size
            )

            db.session.add(ctx)
            db.session.commit()
        except (IntegrityError, Exception):
            upload_file()


@bp.route("/", methods=['POST'])
def upload():
    if request.referrer is None:
        abort(400)

    if get_all_size() > MAX_UPLOAD_SIZE:
        return render_template(
            "upload/cancel.html",
            why="지금은 업로드 할 수 없습니다"
        )

    file = request.files['upload']

    g.filename = secure_filename(file.filename)
    g.stream = file.read()
    g.size = len(g.stream)

    if len(g.filename) >= 255:
        return render_template(
            "upload/cancel.html",
            why="파일명이 너무 길어요 (255자 이하)"
        )
    if g.size == 0:
        return render_template(
            "upload/cancel.html",
            why="파일이 없음"
        )
    if g.size > MAX_FILE_SIZE:
        return render_template(
            "upload/cancel.html",
            why="파일의 용량이 너무 큼"
        )

    g.md5 = md5(g.stream).hexdigest()
    upload_file()

    file.save(path.join(UPLOAD_FOLDER, g.idx))
    return redirect(url_for(".success", idx=g.idx))


@bp.route("/success/<string:idx>")
def success(idx: str):
    ctx = File.query.filter_by(
        idx=idx
    ).first()

    if ctx is None:
        abort(404)

    return render_template(
        "upload/success.html",
        idx=idx, filename=ctx.filename
    )
