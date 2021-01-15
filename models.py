# -*- coding: utf-8 -*-

from sqlalchemy import func

from app import db


class File(db.Model):
    idx = db.Column(
        db.String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    filename = db.Column(
        db.String(100),
        nullable=False
    )

    upload = db.Column(
        db.DateTime,
        default=func.now(),
        nullable=False
    )

    md5 = db.Column(
        db.String(32),
        nullable=False
    )

    size = db.Column(
        db.Integer,
        nullable=False
    )

    def __init__(self, idx: str, filename: str, md5: str, size: int):
        self.idx = idx
        self.filename = filename
        self.md5 = md5
        self.size = size

    def __repr__(self):
        return f"<File idx={self.idx!r}, file_name={self.filename!r}, size={self.size}>"


class Report(db.Model):
    md5 = db.Column(
        db.String(32),
        unique=True,
        primary_key=True,
        nullable=False
    )

    upload = db.Column(
        db.DateTime,
        default=func.now(),
        nullable=False
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    def __init__(self, md5: str, text: str):
        self.md5 = md5
        self.text = text

    def __repr__(self):
        return f"<File idx={self.idx}, md5={self.md5!r}>"
