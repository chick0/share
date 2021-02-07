# -*- coding: utf-8 -*-

from flask import Blueprint, g
from flask import request
from flask import redirect, url_for
from flask import abort, render_template
from sqlalchemy.exc import IntegrityError

from app import db
from models import File, Report

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/", methods=['GET', 'POST'])
def index():
    g.description = "업로드 한 파일을 검색할 수 있습니다"

    if request.method == "GET":
        return render_template(
            "md5/search.html"
        )
    if request.method == "POST":
        if request.referrer is None:
            abort(400)

        try:
            if len(request.form['md5']) < 2:
                abort(400)

            ctx = [file for file in File.query.all() if file.md5.startswith(request.form['md5'][:32])]

            return render_template(
                "md5/result.html",
                ctx=ctx
            )
        except KeyError:
            pass

        abort(400)


@bp.route("/report/<string:md5>", methods=['GET', 'POST'])
def report(md5: str):
    g.description = "파일 신고페이지"

    if request.method == "GET":
        return render_template(
            "md5/report.html"
        )
    if request.method == "POST":
        if request.referrer is None:
            abort(400)
        try:
            ctx = Report(
                md5=md5,
                text=request.form['text']
            )
            db.session.add(ctx)
            db.session.commit()

            return redirect(url_for("index.index"))
        except KeyError:
            pass
        except IntegrityError:
            return render_template(
                "error/error.html",
                message="이미 신고된 파일입니다"
            )

        abort(400)
