# -*- coding: utf-8 -*-

from flask import render_template


def bad_request(error):
    return render_template(
        "error/error.html",
        message="잘못된 요청입니다"
    ), getattr(error, "code")


def forbidden(error):
    return render_template(
        "error/error.html",
        message="오류: 권한 부족"
    ), getattr(error, "code")


def page_not_found(error):
    return render_template(
        "error/error.html",
        message="해당 페이지를 찾을 수 없습니다"
    ), getattr(error, "code")


def method_not_allowed(error):
    return render_template(
        "error/error.html",
        message="잘못된 요청 방법 입니다"
    ), getattr(error, "code")


def request_entity_too_large(error):
    return render_template(
        "error/error.html",
        message="업로드 가능한 가장 큰 파일의 크기는 50MB 입니다"
    ), getattr(error, "code")


def internal_server_error(error):
    return render_template(
        "error/error.html",
        message="내부 스크립트 오류가 발생하였습니다"
    ), getattr(error, "code")
