# -*- coding: utf-8 -*-
from os import path, urandom

with open(path.join("conf", "SECRET_KEY"), mode="wb") as fp:
    fp.write(urandom(32))

print("생성 완료")
