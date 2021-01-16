# -*- coding: utf-8 -*-
from json import dumps
from urllib.request import Request, urlopen

_id = "799874053916721162"
_token = "UqBPPOnkL1_FiGOPDuRY8ui_h9s9WviMSsKmZhmHUKvBVVNS4U-FDA7C6I0ym314l-0R"
url = f"https://discord.com/api/webhooks/{_id}/{_token}"


def send(message: str):
    payload = {
        "content": f"```\n{message}\n```"
    }

    req = Request(url=url, method="POST",
                  data=dumps(payload).encode("utf-8"))

    req.add_header("User-Agent", "curl")
    req.add_header("Content-Type", "application/json")

    urlopen(req)
