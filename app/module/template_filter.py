# -*- encoding: utf-8 -*-
import option


# 파일 사이즈 처리 필터
def size(value: int):
    return f"{value / 1024 / 2024:.2f}MB"


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
