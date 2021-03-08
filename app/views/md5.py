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


@bp.route("/report/<string:md5>", methods=['GET', 'POST'])
def report(md5: str):
    g.description = "파일 신고페이지"

    if request.method == "GET":   # 요청 방식이 `GET` 이면 신고 페이지 보여줌
        ctx = File.query.filter_by(
            md5=md5
        ).first()

        if ctx is None:
            return render_template(
                "md5/cancel.html",
                why="해당 파일은 업로드 된 파일이 아닙니다."
            )

        return render_template(
            "md5/report.html"
        )
    if request.method == "POST":  # 요청 방식이 `POST` 이면 신고 요청 접수
        if request.referrer is None:
            abort(400)
        try:
            ctx = Report()
            ctx.md5 = md5
            ctx.text = request.form.get("text", "신고 내용이 등록되지 않음")

            db.session.add(ctx)  # 데이터베이스에 추가하고
            db.session.commit()  # 변경사항 데이터베이스에 적용함

            return redirect(url_for("index.index"))
        except KeyError:         # 신고 내용이 없는 경우
            return redirect(url_for(".report", md5=md5))
        except IntegrityError:   # 파일이 이미 신고된 경우
            return render_template(
                "md5/cancel.html",
                why="이미 신고된 파일입니다."
            )
