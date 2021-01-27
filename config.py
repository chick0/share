# -*- coding: utf-8 -*-
from os import path, mkdir
from sys import exit
from configparser import ConfigParser

if not path.exists("conf"):
    mkdir("conf")


# 업로드 풀더
BASE_DIR = path.dirname(__file__)
UPLOAD_FOLDER = path.join(BASE_DIR, "upload")
print(f"UPLOAD_FOLDER={UPLOAD_FOLDER}")

MB = 1024 * 1024
GB = MB * 1024

# 업로드 용량 제한 50MB + 요청 헤더 고려 1MB
MAX_FILE_SIZE = 50 * MB
MAX_CONTENT_LENGTH = MAX_FILE_SIZE + 1 * MB

# 총 업로드 용량 제한
MAX_UPLOAD_SIZE = 80 * GB


del MB, GB


# DB 접속 정보 & 설정
try:
    conf = ConfigParser()
    conf.read(path.join("conf", "database.ini"))

    SQLALCHEMY_DATABASE_URI = f"mysql://{conf['account']['user']}:{conf['account']['password']}" \
                              f"@{conf['database']['host']}/{conf['database']['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
except KeyError:
    print("데이터베이스 접속 정보를 불러오지 못함\n"
          "- 'conf/database.ini' 파일을 수정하세요")
    with open(path.join("conf", "database.ini"), mode="w") as fp:
        fp.write("[account]\n")
        fp.write("user=\n")
        fp.write("password=\n\n")
        fp.write("[database]\n")
        fp.write("host=\n")
        fp.write("database=")
    exit(-1)


# 세션 용 시크릿 키
try:
    SECRET_KEY = open(path.join("conf", "SECRET_KEY"), mode="rb").read()
except FileNotFoundError:
    print("'SECRET_KEY' 파일을 찾지 못함\n"
          "- 'SECRET_KEY.py' 스크립트를 실행하세요")
    exit(-2)


# 세션 쿠키 설정
SESSION_COOKIE_NAME = "s"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"


del path, mkdir, exit, ConfigParser, conf
