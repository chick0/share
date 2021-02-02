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
    req = Request(method="GET", url=f"http://localhost:{PORT}/clean")
    req.add_header("User-Agent", "CleanUP")
    with open(path.join(path.dirname(__file__), ".SECRET_KEY"), mode="rb") as fp:
        req.add_header("Secret-Key", sha384(fp.read()).hexdigest())

    with urlopen(req) as resp:
        print(resp.read().decode())
