# -*- coding: utf-8 -*-
from os import path
from datetime import datetime, timedelta

from flask import Blueprint, g
from flask import request, session
from flask import render_template
from flask import abort, send_file
from flask import redirect, url_for

from app import db
from models import File, Report
from config import UPLOAD_FOLDER
from app.module.clean import file_remove


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/<string:idx>")
def ask(idx: str):
    # 파일 아이디로 파일 검색
    ctx = File.query.filter_by(
        idx=idx
    ).first()

    if ctx is None:  # 해당 아이디의 파일이 없다면
        abort(404)   # 404 오류 리턴

    # 파일 비밀번호 검사
    if ctx.password is not None:
        session_key = f"password_{idx}"

        # 비밀번호 인증을 하지 않았다면, 인증 필요로 상태 변경
        if session.get(session_key, None) is None:
            session[session_key] = False

        # 파일 비밀번호 인증을 통과 했으면 지나가기
        if not session[session_key]:
            return redirect(url_for("password.ask", idx=idx))

    # 해당 파일의 MD5로 파일이 신고되었는지 검색
    report = Report.query.filter_by(
        md5=ctx.md5
    ).first()

    # 신고 정보가 있는 경우
    if report is not None:
        def warn():
            g.description = "경고! 해당 파일은 신고된 파일입니다"
            return render_template(
                "dl/warn.html",
                ctx=ctx,
                report=report
            )

        try:
            # 다운로드 경고가 비활성화 상태가 아니라면
            if session[ctx.md5] is False:
                # 경고 끄기 화면으로 이동
                return warn()
        except KeyError:
            # 다운로드 경고가 설정되지 않았다면
            session[ctx.md5] = False  # True: download, False: Cancel

            # 경고 끄기 화면으로 이동
            return warn()

    # 파일 다운로드 물어보기
    g.description = "누군가가 공유한 파일입니다"
    return render_template(
        "dl/ask.html",
        ctx=ctx
    )


@bp.route("/warn_off/<string:idx>/<string:md5>")
def warn_off(idx: str, md5: str):
    if request.referrer is None:
        abort(400)

    # 다운로드 경고 비활성화 하기
    session[md5] = True

    # 파일 다운로드 물어보러 가기
    return redirect(url_for(".ask", idx=idx))


@bp.route("/<string:idx>/<string:filename>")
def download(idx: str, filename: str):
    # 파일 아이디로 파일 검색
    ctx = File.query.filter_by(
        idx=idx
    ).first()

    if ctx is None:  # 해당 되는 파일이 없다면
        abort(404)   # 404 오류 리턴

    # 파일 만료일 계산
    delete_time = ctx.upload + timedelta(days=ctx.delete)

    if datetime.now() >= delete_time:
        db.session.delete(ctx)  # 데이터베이스에서 해당 파일 삭제
        db.session.commit()     # 변경사항 데이터베이스에 적용함

        try:
            # 데이터베이스에 없는 파일들 업로드 풀더에서 삭제하기
            file_remove()
        except (FileNotFoundError, Exception):
            pass

        g.description = "해당 파일은 만료된 파일입니다"
        return render_template(
            "error/error.html",
            message="만료된 파일입니다"
        )

    # 해당 파일의 MD5로 파일이 신고되었는지 검색
    report = Report.query.filter_by(
        md5=ctx.md5
    ).first()

    if report is not None:
        if report.ban is True:  # 해당 파일이 차단 되었다면
            g.description = "해당 파일은 다운로드가 불가능한 차단된 파일입니다"
            return render_template(
                "error/error.html",
                message="이 파일은 차단된 파일입니다"
            ), 400

    # 파일 비밀번호 검사
    if ctx.password is not None:
        session_key = f"password_{idx}"

        # 비밀번호 인증을 하지 않았다면, 인증 필요로 상태 변경
        if session.get(session_key, None) is None:
            session[session_key] = False

        # 파일 비밀번호 인증을 통과 했으면 지나가기
        if not session[session_key]:
            return redirect(url_for("password.ask", idx=idx))

    # 파일이 업로드 풀더에 있다면
    if path.exists(path.join(UPLOAD_FOLDER, idx)):
        # 파일 전송하기
        return send_file(
            filename_or_fp=path.join(UPLOAD_FOLDER, idx),
            mimetype="application/octet-stream",  # 모든 종류의 이진 데이터 (다른 모든 경우를 위한 기본 값)
            as_attachment=True,                   # 첨부파일 형태로 지정 (강제 다운로드)
            attachment_filename=ctx.filename      # 파일명 데이터베이스에 저장된 파일명 불러옴
        )
    else:
        # 아니면 404 리턴
        abort(404)
