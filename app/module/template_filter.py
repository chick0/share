# -*- encoding: utf-8 -*-
import option


# 옵션 로딩 필터
def load(name: str):
    try:
        return getattr(  # 변수 불러오기
            getattr(     # 클래스 불러오기
                option,
                name.split(".")[0]
            ),
            name.split(".")[-1],
        )
    except (AttributeError, TypeError, Exception):
        # 없으면은
        return "#"
