#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path, remove
from datetime import datetime, timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import File


def get_all_ctx():
    return File.query.all()


def get_all_size():
    size = 0
    for ctx in get_all_ctx():
        size += ctx.size

    return size


if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_object(obj=__import__("config"))

    db = SQLAlchemy()
    db.init_app(app)

    with app.app_context() as app:
        print(f"File Count: {len(get_all_ctx())}")
        print(f"File Size: {get_all_size() / 1024 / 1024:.2f}MB")

        for file in get_all_ctx():
            delete_time = file.upload + timedelta(days=1)
            now = datetime.now()

            if now >= delete_time:
                try:
                    remove(path=path.join("upload", file.idx))
                    db.session.delete(file)
                    db.session.commit()
                except (FileNotFoundError, PermissionError, Exception) as e:
                    print(f"Fail to remove '{file.idx}' : '{file.filename}'")
                    print(f" --> {e.__class__.__name__}: {e}")

        print("-- Task completed --")
        print(f"File Count: {len(get_all_ctx())}")
        print(f"File Size: {get_all_size() / 1024 / 1024:.2f}MB")
