# -*- coding: utf-8 -*-

from flask import Blueprint, send_file


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/robots.txt")
def robots():
    # 로봇 텍스트 파일 리턴
    return send_file(
        "static/robots.txt",
        mimetype="text/plain"
    )


@bp.route("/favicon.ico")
def favicon():
    # 웹사이트 아이콘 리턴
    return send_file(
        "static/img/favicon.ico",
        mimetype="image/x-icon"
    )
