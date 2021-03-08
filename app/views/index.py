# -*- coding: utf-8 -*-

from flask import Blueprint, g
from flask import render_template

from config import MAX_FILE_SIZE


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/")
def index():
    g.description = "쉽고 빠르게 파일을 공유해보세요"
    return render_template(
        "index/index.html",

        # 파일 업로드 용량
        MAX_FILE_SIZE=MAX_FILE_SIZE
    )
