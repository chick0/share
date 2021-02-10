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

    if request.method == "GET":   # 요청 방식이 `GET` 이면 검색 창 보여주기
        return render_template(
            "md5/search.html"
        )
    if request.method == "POST":  # 요청 방식이 `POST` 이면 검색 결과 보여주기
        if request.referrer is None:
            abort(400)

        try:
            if len(request.form['md5']) < 2:  # 검색에 사용되는 MD5는 2글자 보다 짧으면
                abort(400)                    # 400 에러 리턴

            # 파일 목록을 가져오고, 목록 중에서 MD5가 검색어로 시작해야 함
            ctx = [file for file in File.query.all() if file.md5.startswith(request.form['md5'][:32])]

            return render_template(
                "md5/result.html",
                ctx=ctx
            )
        except KeyError:   # 검색어 없이 검색한 경우
            return redirect(url_for(".index"))


@bp.route("/report/<string:md5>", methods=['GET', 'POST'])
def report(md5: str):
    g.description = "파일 신고페이지"

    if request.method == "GET":   # 요청 방식이 `GET` 이면 신고 페이지 보여줌
        return render_template(
            "md5/report.html"
        )
    if request.method == "POST":  # 요청 방식이 `POST` 이면 신고 요청 접수
        if request.referrer is None:
            abort(400)
        try:
            ctx = Report(
                md5=md5,
                text=request.form['text']
            )
            db.session.add(ctx)  # 데이터베이스에 추가하고
            db.session.commit()  # 변경사항 데이터베이스에 적용함

            return redirect(url_for("index.index"))
        except KeyError:         # 신고 내용이 없는 경우
            return redirect(url_for(".report", md5=md5))
        except IntegrityError:   # 파일이 이미 신고된 경우
            return render_template(
                "error/error.html",
                message="이미 신고된 파일입니다"
            )
