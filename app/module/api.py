# -*- coding: utf-8 -*-
from json import loads
from urllib.request import Request, urlopen

from flask import g


def get_access_token(code: str):
    req = Request(
        method="POST",
        url=f"https://github.com/login/oauth/access_token"
            f"?client_id={g.client_id}"
            f"&client_secret={g.client_secret}"
            f"&code={code}",
        headers={
            "Accept": "application/json"
        }
    )

    resp = urlopen(req)
    return loads(resp.read())


def get_user_data(access_token: str):
    req = Request(
        method="GET",
        url="https://api.github.com/user",
        headers={
            "Authorization": f"bearer {access_token}"
        }
    )

    resp = urlopen(req)
    return loads(resp.read())
