# -*- coding: utf-8 -*-
from hashlib import sha384
from datetime import datetime

from flask import Blueprint
from flask import request

from app.module.clean import db_remove, file_remove


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("")
def clean():
    time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    with open(".SECRET_KEY", mode="rb") as fp:
        # 내부 인증 용도
        # - `SECRET_KEY` 가져오고 sha384로 해싱하기
        if request.headers.get("Secret-Key") != sha384(fp.read()).hexdigest():
            return f"{time} - Invalid Secret-Key", 403

    db_remove()    # 보관 날짜가 지난 파일들 데이터베이스에서 삭제하기
    file_remove()  # 데이터베이스에 없는 파일들 업로드 풀더에서 삭제하기

    return f"{time} - OK"    # 아무 오류가 없었다면 `OK`
