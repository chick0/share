# -*- coding: utf-8 -*-
from io import StringIO
from os import path, mkdir

from flask import Flask, g
from flask import send_file
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.module import error
from config import UPLOAD_FOLDER
from conf import conf


db = SQLAlchemy()
migrate = Migrate()


def create_app():          # Flask 앱
    app = Flask(__name__)  # 앱 만들기
    app.config.from_object(obj=__import__("config"))

    @app.route("/ok")
    def ok():
        return "200 OK", 200

    @app.route("/favicon.ico")
    def favicon():
        return send_file(
            "static/img/favicon.ico",
            mimetype="image/x-icon"
        )

    @app.route("/robots.txt")
    def robots():
        return send_file(
            StringIO("\n".join([
                "User-agent: *",
                "Allow: /$",
                "Allow: /static",
                "Disallow: /",
                "Disallow: /dl",
                "Disallow: /md5",
                "Disallow: /upload"
            ])),
            mimetype="text/plain"
        )

    @app.before_request
    def set_global():
        # http 프로트콜을 포함한 도메인
        g.host = conf['app']['host']

        # 웹 사이트 타이틀
        g.title = conf['app']['title']

        # 웹 사이트 설명창
        g.description = conf['app']['description']

    @app.after_request
    def set_header(response):
        response.headers['X-Frame-Options'] = "deny"  # Clickjacking
        response.headers['X-Powered-By'] = "chick_0"
        return response

    # DB 모델 등록
    __import__("models")

    # 템플릿 필터 등록
    app.add_template_filter(f=lambda x: f"{int(x) / 1024 / 1024:.2f}MB",   # 소수점 포한
                            name="size")
    app.add_template_filter(f=lambda x: f"{int(int(x) / 1024 / 1024)}MB",  # 소수점 제외
                            name="size_int")

    # ORM 등록 & 초기화
    db.init_app(app)
    migrate.init_app(app, db)

    from app import views
    for view_point in views.__all__:
        try:
            app.register_blueprint(   # 블루프린트 등록시도
                blueprint=getattr(getattr(views, view_point), "bp")
            )
        except AttributeError:        # 블루프린트 객체가 없다면
            print(f"[!] '{view_point}' 는 뷰 포인트가 아닙니다")

    # 오류 핸들러
    app.register_error_handler(400, error.bad_request)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(404, error.page_not_found)
    app.register_error_handler(405, error.method_not_allowed)
    app.register_error_handler(413, error.request_entity_too_large)

    app.register_error_handler(500, error.internal_server_error)

    # 업로드 파일 경로
    if not path.exists(UPLOAD_FOLDER):
        mkdir(UPLOAD_FOLDER)

    return app
