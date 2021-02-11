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

    if g.use_github:
        try:
            g.username = session['username']  # 세션에서 유저 이름 불러옴
        except KeyError:
            g.username = None                 # 세션에서 불러오기 실패 할 경우 비로그인 유저로 판단

    return render_template(
        "index/index.html",

        # 파일 업로드 용량
        MAX_FILE_SIZE=MAX_FILE_SIZE
    )


@bp.route("/login")
def login():
    # Github OAuth 로그인 설정이 안된경우 해당 요청을 아예 무시함
    if not g.use_github:
        return redirect(url_for("index.index"))

    g.description = "로그인"

    return render_template(
        "index/login.html",

        # Github OAuth 로그인 URL
        GITHUB_LOGIN_URL=f"https://github.com/login/oauth/authorize"
                         f"?client_id={g.client_id}"
                         f"&scope=user:email"
    )
