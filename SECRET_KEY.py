# -*- coding: utf-8 -*-
from secrets import token_bytes

SECRET_KEY = token_bytes(32)

with open(".SECRET_KEY", mode="wb") as fp:
    fp.write(SECRET_KEY)
