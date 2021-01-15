#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import request

if __name__ == "__main__":
    with request.urlopen("http://localhost:5555/upload/clean", timeout=1) as resp:
        print(resp.read().decode())
