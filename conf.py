# -*- coding: utf-8 -*-
from os import path, listdir, mkdir
from configparser import ConfigParser

if not path.exists("conf"):
    mkdir("conf")

conf = ConfigParser()
for ini in [ini for ini in listdir("conf") if ini.endswith(".ini")]:  # `conf` 풀더에 확장자가 `ini` 파일들을 불러옴
    conf.read(path.join("conf", ini))
