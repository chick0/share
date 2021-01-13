# -*- coding: utf-8 -*-
from os import path
from uuid import uuid4
from hashlib import md5

from flask import Blueprint
from flask import abort, request
from flask import redirect, url_for
from flask import render_template
from sqlalchemy.exc import IntegrityError

from app import db
from models import File

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_file_by_idx(idx: str):
    return File.query.filter_by(
        idx=idx
    ).first()


def upload_file_by_data(stream: bytes, filename: str):
    stream_hash = md5(stream).hexdigest()

    def run():
        using_uuid = [ctx.idx for ctx in File.query.all()]
        idx = str(uuid4())
        while True:
            if idx in using_uuid:
                idx = uuid4()
            if idx not in using_uuid:
                break

        try:
            ctx = File(
                idx=idx,
                md5=stream_hash,
                filename=filename,
            )

            db.session.add(ctx)  # DB 세션에 추가
            db.session.commit()  # 변경 사항 저장

            return idx
        except IntegrityError:
            return run()

    return run()


@bp.route("/", methods=['GET', 'POST'])
def upload():
    if request.referrer is None:
        abort(400)

    if request.method != "POST":
        abort(405)

    file = request.files['upload']
    stream = file.read()

    if len(file.filename) >= 100:
        return render_template(
            "upload/cancel.html",
            why="파일명이 너무 길어요 (100자 이하)"
        )
    if len(stream) == 0:
        return render_template(
            "upload/cancel.html",
            why="파일이 없음"
        )
    if len(stream) > 50 * 1024 * 1024:
        return render_template(
            "upload/cancel.html",
            why="파일의 용량이 너무 큼"
        )

    idx = upload_file_by_data(
        stream=stream,
        filename=file.filename
    )

    with open(path.join("upload", idx), mode="wb") as fp:
        fp.write(stream)

    return redirect(url_for(".success", idx=idx))


@bp.route("/success/<string:idx>")
def success(idx: str):
    ctx = get_file_by_idx(idx=idx)
    if ctx is None:
        abort(404)

    return render_template(
        "upload/success.html",
        idx=idx, filename=ctx.filename
    )
