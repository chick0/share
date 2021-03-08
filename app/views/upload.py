# -*- coding: utf-8 -*-
from re import compile
from os import path, urandom
from hashlib import md5

from flask import Blueprint
from flask import abort, request, session
from flask import redirect, url_for
from flask import render_template
from sqlalchemy.exc import IntegrityError

from app import db
from models import File
from config import UPLOAD_FOLDER, MAX_FILE_SIZE, MAX_UPLOAD_SIZE


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def secure_filename(filename: str):
    pattern = compile(r"[^A-Za-z0-9가-힣_.-]")
    return str(pattern.sub("", "_".join(filename.split())).strip("._"))


def get_all_size(size: int = 0):
    # 파일의 용량을 데이터베이스에 저장함
    # 그래서 데이터베이스에서 전체 파일의 정보를 불러와서 계산함
    for ctx in File.query.all():
        size += ctx.size

    return size


def upload_file():
    try:
        ctx = File()
        ctx.idx = urandom(4).hex()  # 파일 아이디를 생성함 (8자)

        db.session.add(ctx)
        db.session.commit()

        return ctx
    except IntegrityError:   # 데이터베이스 적용 실패: 이미 사용중인 파일 아이디
        return upload_file()


@bp.route("/", methods=['POST'])
def upload():
    if request.referrer is None:
        abort(400)

    if get_all_size() > MAX_UPLOAD_SIZE:
        return render_template(
            "upload/cancel.html",
            why="업로드 서버의 용량이 꽉 찼습니다"
        )

    file = request.files['upload']

    filename = secure_filename(file.filename)
    stream = file.read()
    size = len(stream)

    if not len(filename) <= 256:
        return render_template(
            "upload/cancel.html",
            why="파일명이 너무 길어요 (256자 이하)"
        )
    if size == 0:
        return render_template(
            "upload/cancel.html",
            why="파일이 없음"
        )
    if not size <= MAX_FILE_SIZE:
        return render_template(
            "upload/cancel.html",
            why="파일의 용량이 너무 큽니다"
        )

    ctx = upload_file()
    ctx.filename = filename            # 파일명 저장
    ctx.md5 = md5(stream).hexdigest()  # MD5 해시 저장
    ctx.size = size                    # 파일 크키 저장

    try:
        # 파일 보관 날짜 가져오기
        timeout = int(request.form.get("timeout", 1))

        if 1 <= timeout <= 14:   # 1일 이상 14일 이하이면 저장
            ctx.delete = timeout
        else:                    # 아니면 1일로 저장
            ctx.delete = 1
    except ValueError:           # 숫자가 아니면 1일로 저장
        ctx.delete = 1

    db.session.commit()

    with open(path.join(UPLOAD_FOLDER, ctx.idx), mode="wb") as fp:
        fp.write(stream)    # 파일 저장

    idx = urandom(2).hex()  # `업로드 성공` 페이지용 아이디 생성 (4자)
    session[idx] = ctx.idx  # 세션에 파일 아이디도 저장

    return redirect(url_for(".private", idx=idx))


@bp.route("/private/<string:idx>")
def private(idx: str):
    # 파일 아이디가 4자가 아니면,
    # - 403 오류 리턴
    if len(session[idx]) != 4:
        abort(403)

    try:
        # `업로드 성공` 페이지용 아이디로 파일 아이디 불러오고
        # 그 파일 아이디로 파일 정보를 불러옴
        ctx = File.query.filter_by(
            idx=session[idx]
        ).first()

        # 만약 불러온 파일 정보가 없다면,
        # - 404 오류 리턴
        if ctx is None:
            abort(404)

        return render_template(
            "upload/private.html",
            idx=ctx.idx,
            filename=ctx.filename
        )
    except KeyError:
        # `업로드 성공` 페이지용 아이디로 파일 아이디를 찾을수 없다면,
        # - 403 오류 리턴
        abort(403)
