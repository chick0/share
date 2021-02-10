# -*- coding: utf-8 -*-
from json import loads
from urllib.request import Request, urlopen

from flask import g


def get_access_token(code: str):
    req = Request(
        method="POST",

        # `access_token`을 발급 받는 API URL 만들기
        url=f"https://github.com/login/oauth/access_token"
            f"?client_id={g.client_id}"
            f"&client_secret={g.client_secret}"
            f"&code={code}",

        # Github API 서버에 JSON 타입으로 리턴해달라고 요청
        headers={
            "Accept": "application/json"
        }
    )

    resp = urlopen(req)        # 만든 요청 보내기
    return loads(resp.read())  # 응답 해석해서 리턴


def get_user_data(access_token: str):
    req = Request(
        method="GET",

        # 사용자 정보를 불러오는 API URL
        url="https://api.github.com/user",

        # - Github API 서버에 JSON 타입으로 리턴해달라고 요청
        # - 발급받은 `access_token` 인증
        headers={
            "Accept": "application/json",
            "Authorization": f"bearer {access_token}"
        }
    )

    resp = urlopen(req)        # 만든 요청 보내기
    return loads(resp.read())  # 응답 해석해서 리턴
