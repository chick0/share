# -*- coding: utf-8 -*-

from flask import g
from flask import render_template


def render(error):
    g.title = "오류"

    return render_template(
        "error/error.html",
        message=g.description
    ), getattr(error, "code")  # `werkzeug`의 오류 클래스에 있는 응답 코드를 가져옴 (werkzeug.exceptions 참고)

# # # # # # # # # # # # # # # # # # # # # #


def bad_request(error):
    g.description = "잘못된 요청입니다"
    return render(error)


def forbidden(error):
    g.description = "해당 페이지를 볼 수 있는 권한이 없습니다"
    return render(error)


def page_not_found(error):
    g.description = "해당 페이지를 찾을 수 없습니다"
    return render(error)


def method_not_allowed(error):
    g.description = "잘못된 요청 방법 입니다"
    return render(error)


def request_entity_too_large(error):
    g.description = "업로드 하려는 파일의 크기가 허용 용량을 초과하고 있습니다"
    return render(error)


def internal_server_error(error):
    g.description = "내부 스크립트 오류가 발생하였습니다"
    return render(error)
