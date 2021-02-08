# -*- coding: utf-8 -*-
from re import compile


def secure_filename(filename: str):
    pattern = compile(r"[^A-Za-z0-9가-힣_.-]")
    return str(pattern.sub("", "_".join(filename.split())).strip("._"))
