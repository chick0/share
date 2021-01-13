# -*- coding: utf-8 -*-
from os import urandom

SECRET_KEY = urandom(32)
with open("SECRET_KEY", mode="wb") as fp:
    fp.write(SECRET_KEY)

print("New SECRET_KEY is :", SECRET_KEY)
