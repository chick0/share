#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from hashlib import sha384
from urllib.request import Request, urlopen

# # # # # # # # # # # # # # # # # # # # # #

# 포트 설정
PORT = 5000

# # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":
    req = Request(method="GET", url=f"http://localhost:{PORT}/clean")  # 보관 기간이 지난 파일들을 정리하는 뷰 포인트
    req.add_header("User-Agent", "CleanUP")

    with open(path.join(path.dirname(__file__), ".SECRET_KEY"), mode="rb") as fp:
        # 내부 인증 용도
        # - `SECRET_KEY` 가져오고 sha384로 해싱하기
        req.add_header("Secret-Key", sha384(fp.read()).hexdigest())

    with urlopen(req) as resp:
        print(resp.read().decode())  # 요청 성공시 `OK` 출력 됨
