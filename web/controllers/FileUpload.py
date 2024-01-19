# @Time    : 2024/1/18 1:24
# @Author  : kai huang
# @File    : FileUpload.py
# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, request, jsonify, Blueprint

from application import db

route_file = Blueprint('file', __name__)
class FileUpload(db.Model):
    __tablename__ = 'file_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    field_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'field_name': self.field_name,
            'file_path': self.file_path,
            'type': self.type,
            'upload_time': self.upload_time.isoformat() if self.upload_time else None
        }