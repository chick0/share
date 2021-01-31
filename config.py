# -*- coding: utf-8 -*-
from os import path
from sys import exit

from conf import conf


# # # # # # # # # # # # # # # # # # # # # #

# 경로 설정
BASE_DIR = path.dirname(__file__)
LOG_PATH = path.join(BASE_DIR, "log")
UPLOAD_FOLDER = path.join(BASE_DIR, "upload")

# # # # # # # # # # # # # # # # # # # # # #

KB = 1024
MB = KB * 1024
GB = MB * 1024

# 총 업로드 용량 제한
MAX_UPLOAD_SIZE = 50 * GB

# 업로드 용량 제한
MAX_FILE_SIZE = 50 * MB

# 요청 크기 제한 | 업로드 용량 + HTTP 헤더 고려 8KB
MAX_CONTENT_LENGTH = MAX_FILE_SIZE + (8 * KB)

# # # # # # # # # # # # # # # # # # # # # #

# DB 접속 정보 & 설정
try:
    SQLALCHEMY_DATABASE_URI = f"mysql://{conf['account']['user']}:{conf['account']['password']}" \
                              f"@{conf['database']['host']}/{conf['database']['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
except KeyError:
    print("데이터베이스 접속 정보를 불러오지 못함")
    exit(-1)

# # # # # # # # # # # # # # # # # # # # # #

# 세션 용 시크릿 키
try:
    SECRET_KEY = open(path.join("conf", "SECRET_KEY"), mode="rb").read()
except FileNotFoundError:
    SECRET_KEY = getattr(__import__("SECRET_KEY"), "KEY")

# 세션 쿠키 설정
SESSION_COOKIE_NAME = "s"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"

# # # # # # # # # # # # # # # # # # # # # #
