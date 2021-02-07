# -*- coding: utf-8 -*-
from os import path, listdir, remove
from datetime import datetime, timedelta

from app import db
from config import UPLOAD_FOLDER
from models import File


def db_remove():
    for file in File.query.all():
        if datetime.now() >= file.upload + timedelta(days=file.delete):
            db.session.delete(file)
    db.session.commit()


def file_remove():
    upload_idx = [ctx.idx for ctx in File.query.all()]
    for idx in listdir(UPLOAD_FOLDER):
        if idx not in upload_idx:
            remove(path.join(UPLOAD_FOLDER, idx))
