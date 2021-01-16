# -*- coding: utf-8 -*-
from os import path, remove
from json import dumps
from datetime import datetime, timedelta

from flask import Blueprint
from flask import render_template
from flask import abort, Response
from sqlalchemy.exc import OperationalError

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


@bp.route("/<string:idx>/md5")
def md5(idx: str):
    try:
        ctx = get_file_by_idx(idx=idx)
    except OperationalError:
        return Response(
            status=500,
            mimetype="application/json",
            response=dumps({"error": "database connection error"})
        )

    if ctx is None:
        return Response(
            status=404,
            mimetype="application/json",
            response=dumps({"error": "file not found"})
        )

    return Response(
        status=200,
        mimetype="application/json",
        response=dumps({"md5": ctx.md5})
    )


@bp.route("/<string:idx>")
def ask(idx: str):
    ctx = get_file_by_idx(idx=idx)
    if ctx is None:
        abort(404)

    return render_template(
        "dl/ask.html",
        ctx=ctx
    )


@bp.route("/<string:idx>/<string:filename>")
def download(idx: str, filename: str):
    ctx = get_file_by_idx(idx=idx)
    if ctx is None:
        abort(404)

    delete_time = ctx.upload + timedelta(days=1)
    now = datetime.now()

    if now >= delete_time:
        try:
            remove(path=path.join("upload", idx))
            db.session.delete(ctx)
            db.session.commit()

            return render_template(
                "error/error.html",
                message="만료된 파일입니다"
            )
        except (FileNotFoundError, PermissionError, Exception):
            pass

    if path.exists(path.join("upload", idx)):
        try:
            with open(path.join("upload", idx), mode="rb") as fp:
                stream = fp.read()

            response = Response(
                response=stream,
                content_type="application/octet-stream",
            )

            response.headers["Content-Disposition"] = f"attachment; filename={ctx.filename}".encode("utf-8")
            return response
        except PermissionError:
            abort(403)
    else:
        abort(404)
