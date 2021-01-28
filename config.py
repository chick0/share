# -*- coding: utf-8 -*-
from os import path, listdir, mkdir
from sys import exit
from configparser import ConfigParser

if not path.exists("conf"):
    mkdir("conf")

conf = ConfigParser()
for ini in listdir("conf"):
    if ini.endswith(".ini"):
        conf.read(path.join("conf", ini))


# 포트 설정
PORT = 5000


# 경로
BASE_DIR = path.dirname(__file__)
LOG_PATH = path.join(BASE_DIR, "log")
UPLOAD_FOLDER = path.join(BASE_DIR, "upload")


# 용량 단위
KB = 1024
MB = KB * 1024
GB = MB * 1024


# 총 업로드 용량 제한
MAX_UPLOAD_SIZE = 80 * GB

# 업로드 용량 제한
MAX_FILE_SIZE = 50 * MB

# 요청 크기 제한 | 업로드 용량 + HTTP 헤더 고려 8KB
MAX_CONTENT_LENGTH = MAX_FILE_SIZE + (8 * KB)


del KB, MB, GB


# DB 접속 정보 & 설정
try:
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


del path, listdir, mkdir
del exit
del ConfigParser, conf
