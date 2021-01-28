#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import request

from config import PORT

if __name__ == "__main__":
    with request.urlopen(f"http://localhost:{PORT}/clean", timeout=1) as resp:
        print(resp.read().decode())
