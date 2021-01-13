# -*- coding: utf-8 -*-
from os import path, mkdir

from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.module import error, template_filter

db = SQLAlchemy()
migrate = Migrate()


def create_app():          # Flask 앱
    app = Flask(__name__)  # 앱 만들기
    app.config.from_object(obj=__import__("config"))

    @app.after_request
    def set_header(response):
        response.headers['X-Frame-Options'] = "deny"            # Clickjacking
        response.headers['X-XSS-Protection'] = "1"              # Cross-site scripting
        response.headers['X-Content-Type-Options'] = "nosniff"  # Check MIMETYPE

        if request.path.endswith(".css"):
            response.headers['Content-Type'] = "text/css; charset=utf-8"
        if request.path.endswith(".txt"):
            response.headers['Content-Type'] = "text/plain; charset=utf-8"

        if request.path.endswith(".json"):
            response.headers['Content-Type'] = "application/json; charset=utf-8"
        if request.path.endswith(".js"):
            response.headers['Content-Type'] = "application/javascript; charset=utf-8"

        response.headers['X-Powered-By'] = "chick_0"
        return response

    # DB 모델 등록
    __import__("models")

    # 템플릿 필터 등록
    app.add_template_filter(template_filter.load)

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
            print(f"[!] '{view_point}' is not view point")

    # 오류 핸들러
    app.register_error_handler(400, error.bad_request)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(404, error.page_not_found)
    app.register_error_handler(405, error.method_not_allowed)
    app.register_error_handler(413, error.request_entity_too_large)

    app.register_error_handler(500, error.internal_server_error)

    # 업로드 파일 경로
    if not path.exists("upload"):
        mkdir("upload")

    return app
