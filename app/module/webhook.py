# -*- coding: utf-8 -*-
from json import dumps
from urllib.request import Request, urlopen

from config import conf


def send(message: str):
    payload = {
        "content": f"```\n{message}\n```"
    }

    req = Request(url=f"https://discord.com/api/webhooks/{conf['discord']['id']}/{conf['discord']['token']}",
                  data=dumps(payload).encode("utf-8"),
                  method="POST")

    req.add_header("User-Agent", "curl")
    req.add_header("Content-Type", "application/json")

    urlopen(req)
