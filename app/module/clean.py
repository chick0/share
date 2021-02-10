# -*- coding: utf-8 -*-
from os import path, listdir, remove
from datetime import datetime, timedelta

from app import db
from config import UPLOAD_FOLDER
from models import File


def db_remove():
    for file in File.query.all():                                        # 모든 파일정보 데이터베이스에서 불러오기
        if datetime.now() >= file.upload + timedelta(days=file.delete):  # 파일의 보관 날짜가 지난 경우
            db.session.delete(file)                                      # 데이터베이스에서 파일 삭제하기
    db.session.commit()                                                  # 변경사항 데이터베이스에 적용함


def file_remove():
    # 데이터베이스에 저장되어있는 파일 아이디 불러오기
    upload_idx = [ctx.idx for ctx in File.query.all()]

    for idx in listdir(UPLOAD_FOLDER):  # 업로드 풀더에 저장된 파일 목록 불러오기
        if idx not in upload_idx:       # 해당 파일이 데이터베이스에 없다면
            remove(path.join(UPLOAD_FOLDER, idx))  # 해당 파일 삭제하기
