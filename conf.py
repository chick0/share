# -*- coding: utf-8 -*-
from os import path, listdir, mkdir
from configparser import ConfigParser

if not path.exists("conf"):
    mkdir("conf")

conf = ConfigParser()
for ini in [ini for ini in listdir("conf") if ini.endswith(".ini")]:
    conf.read(path.join("conf", ini))
