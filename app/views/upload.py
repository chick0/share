# -*- coding: utf-8 -*-
from os import path, urandom
from hashlib import md5

from flask import Blueprint, g
from flask import abort, request, session
from flask import redirect, url_for
from flask import render_template
from sqlalchemy.exc import IntegrityError

from app import db
from models import File
from app.module.secure import secure_filename
from config import UPLOAD_FOLDER, MAX_FILE_SIZE, MAX_UPLOAD_SIZE


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_all_size(size: int = 0):
    # 파일의 용량을 데이터베이스에 저장함
    # 그래서 데이터베이스에서 전체 파일의 정보를 불러와서 계산함
    for ctx in File.query.all():
        size += ctx.size

    return size


def upload_file():
    g.idx = urandom(4).hex()  # 파일 아이디를 생성함 (8자)

    try:
        ctx = File(
            idx=g.idx,
            md5=g.md5,
            filename=g.filename,
            size=g.size
        )

        if g.use_github:  # 만약 Github OAuth 설정이 되어있는 경우
            try:
                # 세션에서 이메일을 가져온다
                email = session['email']
                ctx.email = email
            except KeyError:
                # 로그인 상태가 아니라서 이메일 정보가 없으면 넘긴다
                pass

        db.session.add(ctx)  # 데이터베이스에 추가하고
        db.session.commit()  # 변경사항 데이터베이스에 적용함

    except IntegrityError:   # 데이터베이스 적용 실패: 이미 사용중인 파일 아이디
        upload_file()


@bp.route("/", methods=['POST'])
def upload():
    if request.referrer is None:
        abort(400)

    if get_all_size() > MAX_UPLOAD_SIZE:
        return render_template(
            "upload/cancel.html",
            why="지금은 업로드 할 수 없습니다"
        )

    file = request.files['upload']

    g.filename = secure_filename(file.filename)  # 파일 이름 검사
    g.stream = file.read()                       # 파일
    g.size = len(g.stream)                       # 파일의 크기 확인

    if len(g.filename) > 255:
        return render_template(
            "upload/cancel.html",
            why="파일명이 너무 길어요 (255자 이하)"
        )
    if g.size == 0:
        return render_template(
            "upload/cancel.html",
            why="파일이 없음"
        )
    if g.size > MAX_FILE_SIZE:
        return render_template(
            "upload/cancel.html",
            why="파일의 용량이 너무 큼"
        )

    g.md5 = md5(g.stream).hexdigest()            # 파일의 MD5 해시 구하기
    upload_file()                                # 데이터베이스에 파일 정보 추가하기

    with open(path.join(UPLOAD_FOLDER, g.idx), mode="wb") as fp:
        fp.write(g.stream)                       # 파일 저장

    idx = urandom(2).hex()  # `업로드 성공` 페이지용 아이디 생성 (4자)
    session[idx] = g.idx    # 세션에 파일 아이디도 저장

    return redirect(url_for(".private", idx=idx))


@bp.route("/private/<string:idx>")
def private(idx: str):
    g.description = "해당 페이지는 업로더만 확인이 가능합니다"

    try:
        # `업로드 성공` 페이지용 아이디로 파일 아이디 불러오고
        # 그 파일 아이디로 파일 정보를 불러옴
        ctx = File.query.filter_by(
            idx=session[idx]
        ).first()

        # 만약 불러온 파일 정보가 없다면, 403 오류 리턴
        if ctx is None:
            abort(404)

        return render_template(
            "upload/private.html",
            idx=ctx.idx,
            filename=ctx.filename
        )
    except KeyError:
        # `업로드 성공` 페이지용 아이디로 파일 아이디를 찾을수 없다면, 403 오류 리턴
        abort(403)
