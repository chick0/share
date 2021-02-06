# -*- coding: utf-8 -*-

from sqlalchemy import func

from app import db


class File(db.Model):
    idx = db.Column(
        db.String(8),
        unique=True,
        primary_key=True,
        nullable=False
    )

    filename = db.Column(
        db.String(255),
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

    email = db.Column(
        db.String(96)
    )

    delete = db.Column(
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
    md5 = db.Column(
        db.String(32),
        unique=True,
        primary_key=True,
        nullable=False
    )

    upload = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    ban = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    def __init__(self, md5: str, text: str):
        self.md5 = md5
        self.text = text

    def __repr__(self):
        return f"<Report md5={self.md5!r}>"
