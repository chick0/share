# -*- coding: utf-8 -*-
from sys import exit
from configparser import ConfigParser


# 요청 용량 제한 | 50MB + 요청 헤더 고려 1MB
MAX_CONTENT_LENGTH = 51 * 1024 * 1024


# DB 접속 정보 & 설정
try:
    conf = ConfigParser()
    conf.read("database.ini")

    SQLALCHEMY_DATABASE_URI = f"mysql://{conf['account']['user']}:{conf['account']['password']}" \
                              f"@{conf['database']['host']}/{conf['database']['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
except KeyError as e:
    print("데이터베이스 접속 정보를 불러오지 못함\n"
          "- 'database.ini' 파일을 수정하세요")
    with open("database.ini", mode="w") as fp:
        fp.write("[account]\n")
        fp.write("user=\n")
        fp.write("password=\n\n")
        fp.write("[database]\n")
        fp.write("host=\n")
        fp.write("database=")
    exit(-1)


# 세션 용 시크릿 키
try:
    SECRET_KEY = open("SECRET_KEY", mode="rb").read()
except FileNotFoundError:
    print("'SECRET_KEY' 파일을 찾지 못함\n"
          "- 'SECRET_KEY.py' 스크립트를 실행하세요")
    exit(-2)


# 세션 쿠키 설정
SESSION_COOKIE_NAME = "s"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"


del exit, ConfigParser, conf
