# -*- coding: utf-8 -*-
from hashlib import sha384

from flask import Blueprint
from flask import abort
from flask import request
from flask import session
from flask import render_template
from flask import redirect, url_for

from app import db
from models import File


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/p/<string:idx>", methods=['GET', 'POST'])
def private(idx: str):
    idx_ = session.get(idx, None)
    if idx_ is None:
        return abort(401)

    ctx = File.query.filter_by(
        idx=idx_
    ).first()

    if ctx is None:
        return abort(404)

    if request.method == "GET":
        return render_template(
            "password/private.html",
            idx=ctx.idx,
        )
    elif request.method == "POST":
        password = request.form.get("password", None)

        if password is None or len(password) == 0:
            ctx.password = None
        else:
            ctx.password = sha384(password.encode()).hexdigest()

        db.session.commit()

        return redirect(url_for("upload.private", idx=idx))


@bp.route("/<string:idx>", methods=['GET', 'POST'])
def ask(idx: str):
    ctx = File.query.filter_by(
        idx=idx
    ).first()

    if ctx is None:
        return abort(404)

    session_key = f"password_{idx}"
    if session.get(session_key, None) is True:
        return redirect(url_for("dl.ask", idx=idx))

    if request.method == "GET":
        password_alert = session.get("password_alert", None)

        # 비밀번호 관련 안내 매시지가 설정된 경우
        # 2번 나오지 않도록 삭제하기
        if password_alert is not None:
            del session['password_alert']

        return render_template(
            "password/ask.html",
            idx=idx,

            password_alert=password_alert
        )

    elif request.method == "POST":
        password = sha384(request.form.get("password", "").encode()).hexdigest()

        if ctx.password == password:
            session[session_key] = True
            return redirect(url_for("dl.ask", idx=idx))

        session['password_alert'] = "비밀번호가 일치하지 않습니다"
        return redirect(url_for(".ask", idx=idx))
