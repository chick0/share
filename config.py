# -*- coding: utf-8 -*-
from os import urandom

from option import Database

# 용량제한 | 50MB + 요청 헤더 고려 1MB
MAX_CONTENT_LENGTH = 51 * 1024 * 1024

# DB ORM 접속 정보 & 설정
SQLALCHEMY_DATABASE_URI = f"mysql://{Database.username}:{Database.password}@{Database.host}/{Database.database}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 세션용 시크릿 키
try:
    SECRET_KEY = open("SECRET_KEY", mode="rb").read()
except FileNotFoundError:
    SECRET_KEY = urandom(32)
    with open("SECRET_KEY", mode="wb") as fp:
        fp.write(SECRET_KEY)

# 세션 쿠키 관련 설정
SESSION_COOKIE_NAME = "s"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
