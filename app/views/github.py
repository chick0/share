# -*- coding: utf-8 -*-
from hashlib import sha384
from urllib.error import HTTPError

from flask import Blueprint, g
from flask import request, session
from flask import redirect, url_for
from flask import render_template

from app import db
from models import File
from app.module import github
from app.module.clean import file_remove
from app.module.secure import secure_filename


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/callback")
def callback():
    # Github OAuth 로그인 설정이 안된경우 해당 요청을 아예 무시함
    if "github" not in g.use_login:
        return redirect(url_for("index.index"))

    # `access_token` 발급할 때 사용하는 코드를 불러옴
    code = request.args.get("code")
    if code is None:
        # 코드가 없다면 로그인 화면으로 보내기
        return redirect(url_for("index.login"))

    try:
        # 코드를 이용해서 `access_token` 가져오기
        token = github.get_access_token(code=code)

        # 가져온 토큰을 세션에 저장하기
        session['access_token'] = token['access_token']

        # 세션에 저장 되어있는 토큰으로 사용자 정보 가져오기
        user_data = github.get_user_data(
            access_token=session['access_token']
        )

        # 로그인 서비스 정보 저장
        session['service'] = "github"

        # 사용자 정보중 이메일과 닉네임을 세션에 저장함
        session['email'] = sha384(user_data['email'].encode()).hexdigest()
        session['username'] = user_data['name']

        # 로그인 성공, 메인 화면으로 이동
        return redirect(url_for("index.index"))
    except (HTTPError, KeyError):
        # - 올바르지 않은 코드로 로그인을 시도해 Github 에서 오류를 리턴함
        # - Github 에서 전달받은 JSON 에서 토큰을 가져오지 못함
        # --> 로그인 화면으로 보내기
        return redirect(url_for("index.login"))


@bp.route("/dashboard")
def dashboard():
    # Github OAuth 로그인 설정이 안된경우 해당 요청을 아예 무시함
    if "github" not in g.use_login:
        return redirect(url_for("index.index"))

    try:
        if session['service'] != "github":
            # 로그인한 서비스가 Github 이 아닌 경우 메인 페이지로 이동
            return redirect(url_for("index.index"))
    except KeyError:
        # 세션에 로그인 서비스 정보가 없는 경우 로그인 페이지로 이동
        return redirect(url_for("index.login"))

    try:
        # 닉네임과 이메일을 세션에서 가져옴
        username = session['username']
        email = session['email']
    except KeyError:
        # 세션에서 찾지 못했다면 로그인 화면으로 이동
        return redirect(url_for("index.login"))

    # 로그인한 사용자의 이메일 주소와 일치하는 파일들을 가져옴
    ctx = File.query.filter_by(
        service="github",
        email=email
    ).all()

    return render_template(
        "github/dashboard.html",
        username=username,
        ctx=ctx
    )


@bp.route("/detail/<string:idx>")
def detail(idx: str):
    # Github OAuth 로그인 설정이 안된경우 해당 요청을 아예 무시함
    if "github" not in g.use_login:
        return redirect(url_for("index.index"))

    try:
        if session['service'] != "github":
            # 로그인한 서비스가 Github 이 아닌 경우 메인 페이지로 이동
            return redirect(url_for("index.index"))
    except KeyError:
        # 세션에 로그인 서비스 정보가 없는 경우 로그인 페이지로 이동
        return redirect(url_for("index.login"))

    try:
        # 닉네임과 이메일을 세션에서 가져옴
        username = session['username']
        email = session['email']
    except KeyError:
        # 세션에서 찾지 못했다면 로그인 화면으로 이동
        return redirect(url_for("index.login"))

    # 파일 아이디와 로그인한 사용자의 이메일 주소와 일치하는 파일을 가져옴
    ctx = File.query.filter_by(
        idx=idx,
        service="github",
        email=email
    ).first()

    if ctx is None:  # 해당 되는 파일이 없는 경우 대시보드로 돌아감
        return redirect(url_for(".dashboard"))

    return render_template(
        "github/detail.html",
        username=username,
        ctx=ctx
    )


@bp.route("/edit/<string:idx>", methods=['GET', 'POST'])
def edit(idx: str):
    # Github OAuth 로그인 설정이 안된경우 해당 요청을 아예 무시함
    if "github" not in g.use_login:
        return redirect(url_for("index.index"))

    try:
        if session['service'] != "github":
            # 로그인한 서비스가 Github 이 아닌 경우 메인 페이지로 이동
            return redirect(url_for("index.index"))
    except KeyError:
        # 세션에 로그인 서비스 정보가 없는 경우 로그인 페이지로 이동
        return redirect(url_for("index.login"))

    try:
        # 닉네임과 이메일을 세션에서 가져옴
        username = session['username']
        email = session['email']
    except KeyError:
        # 세션에서 찾지 못했다면 로그인 화면으로 이동
        return redirect(url_for("index.login"))

    # 파일 아이디와 로그인한 사용자의 이메일 주소와 일치하는 파일을 가져옴
    ctx = File.query.filter_by(
        idx=idx,
        service="github",
        email=email
    ).first()

    if ctx is None:  # 해당 되는 파일이 없는 경우 대시보드로 돌아감
        return redirect(url_for(".dashboard"))

    if request.method == "GET":     # 요청 방식이 `GET` 이면 수정 페이지 보여줌
        return render_template(
            "github/edit.html",
            username=username,
            ctx=ctx
        )

    elif request.method == "POST":  # 요청 방식이 `POST` 이면 수정 요청 처리
        # 파일 이름 검사
        filename = secure_filename(
            filename=request.form.get("filename")
        )

        # 파일명이 `None`이 아니고 길이가 0이 아니라면
        if filename is not None and len(filename) != 0:
            ctx.filename = filename  # 파일명 바꾸고
            db.session.commit()      # 변경사항 데이터베이스에 적용함

        return redirect(url_for(".edit", idx=idx))


@bp.route("/delete/<string:idx>")
def delete(idx: str):
    # Github OAuth 로그인 설정이 안된경우 해당 요청을 아예 무시함
    if "github" not in g.use_login:
        return redirect(url_for("index.index"))

    try:
        if session['service'] != "github":
            # 로그인한 서비스가 Github 이 아닌 경우 메인 페이지로 이동
            return redirect(url_for("index.index"))
    except KeyError:
        # 세션에 로그인 서비스 정보가 없는 경우 로그인 페이지로 이동
        return redirect(url_for("index.login"))

    try:
        # 이메일을 세션에서 가져옴
        email = session['email']
    except KeyError:
        # 세션에서 찾지 못했다면 로그인 화면으로 이동
        return redirect(url_for("index.login"))

    # 파일 아이디와 로그인한 사용자의 이메일 주소와 일치하는 파일을 찾고 삭제 함
    # 해당되는 파일이 없는 경우 아무일도 일어나지 않음
    File.query.filter_by(
        idx=idx,
        service="github",
        email=email
    ).delete()
    db.session.commit()  # 변경사항 데이터베이스에 적용함

    try:
        # 데이터베이스에 없는 파일 삭제하기
        file_remove()
    except (FileNotFoundError, Exception):
        pass

    if request.args.get("go") == "index":  # `index`로 가라고 지정한 경우
        return redirect(url_for("index.index"))

    return redirect(url_for(".dashboard"))


@bp.route("/renew/<string:idx>")
def renew(idx: str):
    # Github OAuth 로그인 설정이 안된경우 해당 요청을 아예 무시함
    if "github" not in g.use_login:
        return redirect(url_for("index.index"))

    try:
        if session['service'] != "github":
            # 로그인한 서비스가 Github 이 아닌 경우 메인 페이지로 이동
            return redirect(url_for("index.index"))
    except KeyError:
        # 세션에 로그인 서비스 정보가 없는 경우 로그인 페이지로 이동
        return redirect(url_for("index.login"))

    try:
        # 이메일을 세션에서 가져옴
        email = session['email']
    except KeyError:
        # 세션에서 찾지 못했다면 로그인 화면으로 이동
        return redirect(url_for("index.login"))

    # 파일 아이디와 로그인한 사용자의 이메일 주소와 일치하는 파일을 가져옴
    ctx = File.query.filter_by(
        idx=idx,
        service="github",
        email=email
    ).first()

    if ctx is None:  # 해당 되는 파일이 없는 경우 대시보드로 돌아감
        return redirect(url_for(".dashboard"))

    if ctx.delete < 14:  # 보관일이 14일 보다 작은 경우
        # 하루 늘리기
        ctx.delete = ctx.delete + 1

    db.session.commit()  # 변경사항 데이터베이스에 적용함

    return redirect(url_for(".detail", idx=idx))
