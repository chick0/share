# -*- coding: utf-8 -*-

from flask import Blueprint, g
from flask import session
from flask import render_template
from flask import redirect, url_for

from config import MAX_FILE_SIZE


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/ok")
def ok():
    # 서버 생존 확인 용
    return "OK", 200


@bp.route("/")
def index():
    g.description = "쉽고 빠르게 파일을 공유해보세요"

    try:
        g.username = session['username']  # 세션에서 유저 이름 불러옴
    except KeyError:
        g.username = None                 # 세션에서 불러오기 실패 할 경우 비로그인 유저로 판단

    return render_template(
        "index/index.html",

        # 파일 업로드 용량
        MAX_FILE_SIZE=MAX_FILE_SIZE
    )
