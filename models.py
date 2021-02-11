# -*- coding: utf-8 -*-

from sqlalchemy import func

from app import db


class File(db.Model):
    idx = db.Column(         # 파일 고유 아이디
        db.String(8),
        unique=True,
        primary_key=True,
        nullable=False
    )

    filename = db.Column(    # 파일 이름
        db.String(255),
        nullable=False
    )

    upload = db.Column(      # 파일 업로드 시간
        db.DateTime,
        default=func.now(),
        nullable=False
    )

    md5 = db.Column(         # 파일 MD5 해시
        db.String(32),
        nullable=False
    )

    size = db.Column(        # 파일 크기
        db.Integer,
        nullable=False
    )

    service = db.Column(     # 로그인 서비스 이름
        db.String(10)
    )

    email = db.Column(       # 파일 업로더의 이메일, sha384 적용됨 (로그인시 저장됨)
        db.String(96)
    )

    delete = db.Column(      # 파일 보관 날짜 (기본값: 1일, 로그인시 최대 14일
        db.Integer,
        default=1,
        nullable=False
    )

    def __init__(self, idx: str, filename: str, md5: str, size: int):
        self.idx = idx
        self.filename = filename
        self.md5 = md5
        self.size = size

    def __repr__(self):
        return f"<File idx={self.idx!r}>"


class Report(db.Model):
    md5 = db.Column(         # 파일 MD5 해시
        db.String(32),
        unique=True,
        primary_key=True,
        nullable=False
    )

    upload = db.Column(      # 신고 등록 시간
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    text = db.Column(        # 신고 내용
        db.Text,
        nullable=False
    )

    ban = db.Column(         # 파일 차단 여부 (파일 차단시 다운로드가 불가능함)
        db.Boolean,
        nullable=False,
        default=False
    )

    def __init__(self, md5: str, text: str):
        self.md5 = md5
        self.text = text

    def __repr__(self):
        return f"<Report md5={self.md5!r}>"
