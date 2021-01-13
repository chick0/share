# -*- coding: utf-8 -*-

class App:                 # 앱 관련
    # 앱 이름
    name = "share"

    # 대표 도메인
    host = "https://share.ch1ck.xyz"

    # 연락용 이메일
    email = "chick_0@ch1ck.xyz"


class Server:              # 서버 관련
    # 포트 번호
    port = 5555


class Log:                 # 로그 관련
    # 시작시간
    from datetime import datetime
    now = datetime.today()

    # 파일명
    from os import path, mkdir

    if not path.isdir(path.join("log")):
        mkdir("log")

    name = f"{now.strftime('%Y-%m-%d %Hh %Mm %Ss')}.log"
    file = path.join("log", name)


class Database:            # 데이터베이스 접속 정보
    # MySQL 서버 유저 정보
    username = "share"
    password = "share_the_world"

    # MySQL 서버 IP
    host = "192.168.219.100"

    # 사용할 데이터베이스
    database = "share"
