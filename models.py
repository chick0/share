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
        db.String(256),
        nullable=False,
        default="undefined"
    )

    upload = db.Column(      # 파일 업로드 시간
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    md5 = db.Column(         # 파일 MD5 해시
        db.String(32),
        nullable=False,
        default="undefined"
    )

    size = db.Column(        # 파일 크기
        db.Integer,
        nullable=False,
        default=0
    )

    delete = db.Column(      # 파일 보관 날짜 (기본 값: 1일, 최대 값 14일)
        db.Integer,
        nullable=False,
        default=0
    )

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

    def __repr__(self):
        return f"<Report md5={self.md5!r}>"
