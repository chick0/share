# -*- coding: utf-8 -*-
from os import path, remove
from uuid import uuid4
from hashlib import md5
from datetime import datetime, timedelta

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


def get_all_size():
    size = 0
    for ctx in File.query.all():
        size += ctx.size

    return size


def get_file_by_idx(idx: str):
    return File.query.filter_by(
        idx=idx
    ).first()


def upload_file_by_data(stream: bytes, filename: str, size: int):
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
                size=size
            )

            db.session.add(ctx)  # DB 세션에 추가
            db.session.commit()  # 변경 사항 저장

            return idx
        except IntegrityError:
            return run()

    return run()


@bp.route("/able")
def able():
    if get_all_size() > 80 * 1024 * 1024 * 1024:
        return "false"
    else:
        return "true"


@bp.route("/status")
def status():
    return f"{get_all_size() / 1024 / 1024:.2f}MB"


@bp.route("/clean")
def clean():
    for file in File.query.all():
        delete_time = file.upload + timedelta(days=1)
        now = datetime.now()

        if now >= delete_time:
            try:
                if path.exists(path.join("upload", file.idx)):
                    remove(path=path.join("upload", file.idx))
                    db.session.delete(file)
                    db.session.commit()
            except (FileNotFoundError, PermissionError, Exception):
                pass

    return "OK"


@bp.route("/", methods=['POST'])
def upload():
    if request.referrer is None:
        abort(400)

    if get_all_size() > 80 * 1024 * 1024 * 1024:
        return render_template(
            "upload/cancel.html",
            why="지금은 업로드 할 수 없습니다"
        )

    file = request.files['upload']
    stream = file.read()
    size = len(stream)

    if len(file.filename) >= 100:
        return render_template(
            "upload/cancel.html",
            why="파일명이 너무 길어요 (100자 이하)"
        )
    if size == 0:
        return render_template(
            "upload/cancel.html",
            why="파일이 없음"
        )
    if size > 50 * 1024 * 1024:
        return render_template(
            "upload/cancel.html",
            why="파일의 용량이 너무 큼"
        )

    idx = upload_file_by_data(
        stream=stream,
        filename=file.filename,
        size=size
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
