# -*- coding: utf-8 -*-
from os import path
from secrets import token_bytes

KEY = token_bytes(32)

with open(path.join("conf", "SECRET_KEY"), mode="wb") as fp:
    fp.write(KEY)
