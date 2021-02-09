# -*- coding: utf-8 -*-
from os import path, urandom
from hashlib import md5

from flask import Blueprint, g
from flask import abort, request, session
from flask import redirect, url_for
from flask import render_template
from sqlalchemy.exc import IntegrityError

from app import db
from models import File
from app.module.secure import secure_filename
from config import UPLOAD_FOLDER, MAX_FILE_SIZE, MAX_UPLOAD_SIZE


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_all_size(size: int = 0):
    for ctx in File.query.all():
        size += ctx.size

    return size


def upload_file():
    g.idx = urandom(4).hex()

    try:
        ctx = File(
            idx=g.idx,
            md5=g.md5,
            filename=g.filename,
            size=g.size
        )

        if g.use_github:
            try:
                email = session['email']
                ctx.email = email
            except KeyError:
                pass

        db.session.add(ctx)
        db.session.commit()
    except IntegrityError:
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

    if len(g.filename) > 255:
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

    with open(path.join(UPLOAD_FOLDER, g.idx), mode="wb") as fp:
        fp.write(g.stream)

    idx = urandom(2).hex()
    session[idx] = g.idx

    return redirect(url_for(".private", idx=idx))


@bp.route("/private/<string:idx>")
def private(idx: str):
    g.description = "해당 페이지는 업로더만 확인이 가능합니다"

    try:
        ctx = File.query.filter_by(
            idx=session[idx]
        ).first()

        if ctx is None:
            abort(404)

        return render_template(
            "upload/private.html",
            idx=ctx.idx,
            filename=ctx.filename
        )
    except KeyError:
        abort(403)
