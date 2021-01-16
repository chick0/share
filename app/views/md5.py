# -*- coding: utf-8 -*-
from secrets import token_bytes

from flask import Blueprint
from flask import request, session
from flask import redirect, url_for
from flask import abort, render_template
from sqlalchemy.exc import IntegrityError

from app import db
from models import File, Report
from app.module import webhook

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        session['csrf_md5_search'] = token_bytes(64).hex()
        return render_template(
            "md5/search.html",
            csrf=session['csrf_md5_search']
        )
    if request.method == "POST":
        if request.referrer is None:
            abort(400)

        try:
            if len(request.form['md5']) < 2:
                abort(400)

            if request.form['csrf_token'] == session['csrf_md5_search']:
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
    if request.method == "GET":
        session['csrf_md5_report'] = token_bytes(64).hex()
        return render_template(
            "md5/report.html",
            csrf=session['csrf_md5_report']
        )
    if request.method == "POST":
        if request.referrer is None:
            abort(400)
        try:
            if request.form['csrf_token'] == session['csrf_md5_report']:
                ctx = Report(
                    md5=md5,
                    text=request.form['text']
                )
                db.session.add(ctx)
                db.session.commit()

                webhook.send(f"{md5}에 대한 신고가 등록됨")
                return redirect(url_for("index.index"))
        except KeyError:
            pass
        except IntegrityError:
            return render_template(
                "error/error.html",
                message="이미 신고된 파일입니다"
            )

        abort(400)
