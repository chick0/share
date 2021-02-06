# -*- coding: utf-8 -*-
from os import path
from datetime import datetime, timedelta

from flask import Blueprint, g
from flask import request, session
from flask import render_template
from flask import abort, send_file
from flask import redirect, url_for

from app import db
from config import UPLOAD_FOLDER
from models import File, Report

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_file_by_idx(idx: str):
    return File.query.filter_by(
        idx=idx
    ).first()


def get_report_by_hash(md5: str):
    return Report.query.filter_by(
        md5=md5
    ).first()


@bp.route("/<string:idx>")
def ask(idx: str):
    ctx = get_file_by_idx(idx=idx)
    if ctx is None:
        abort(404)

    report = get_report_by_hash(md5=ctx.md5)
    if report is not None:
        try:
            session[ctx.md5]
        except KeyError:
            session[ctx.md5] = False  # True: download, False: Cancel

        if session[ctx.md5] is False:
            g.description = "경고! 해당 파일은 신고된 파일입니다"
            return render_template(
                "dl/warn.html",
                ctx=ctx,
                report=report
            )

    g.description = "누군가가 공유한 파일입니다"
    return render_template(
        "dl/ask.html",
        ctx=ctx
    )


@bp.route("/warn_off/<string:idx>/<string:md5>")
def warn_off(idx: str, md5: str):
    if request.referrer is None:
        abort(400)
    session[md5] = True

    return redirect(url_for(".ask", idx=idx))


@bp.route("/<string:idx>/<string:filename>")
def download(idx: str, filename: str):
    ctx = get_file_by_idx(idx=idx)
    if ctx is None:
        abort(404)

    delete_time = ctx.upload + timedelta(days=ctx.delete)
    now = datetime.now()

    if now >= delete_time:
        db.session.delete(ctx)
        db.session.commit()

        g.description = "해당 파일은 만료된 파일입니다"
        return render_template(
            "error/error.html",
            message="만료된 파일입니다"
        )

    report = get_report_by_hash(md5=ctx.md5)
    if report is not None:
        if report.ban is True:
            g.description = "해당 파일은 다운로드가 불가능한 차단된 파일입니다"
            return render_template(
                "error/error.html",
                message="이 파일은 차단된 파일입니다"
            ), 400

    if path.exists(path.join(UPLOAD_FOLDER, idx)):
        return send_file(
            filename_or_fp=path.join(UPLOAD_FOLDER, idx),
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename=ctx.filename
        )
    else:
        abort(404)
