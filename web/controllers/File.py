# @Time    : 2024/1/16 2:12
# @Author  : kai huang
# @File    : File.py
# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, request, jsonify, Blueprint

from application import db
from web.controllers.FileUpload import FileUpload
from web.controllers.client.Client import Client
from web.controllers.client.Nurse import Nurse
from web.controllers.client.Student import Student

route_file = Blueprint('file', __name__)

from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
import time




def update_field_status(model, user_id, field_name):
    record = model.query.get(user_id)
    if not record:
        return False, "Record not found"

    if hasattr(record, field_name):
        setattr(record, field_name, 1)
        db.session.commit()
        return True, "Field updated successfully"
    else:
        return False, "Field does not exist"


@route_file.route('/upload/<int:user_id>/<string:field_name>/<int:type>', methods=['POST'])
def upload_file(user_id, field_name, type):
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    filename = secure_filename(file.filename)
    filename = f"{int(time.time())}_{filename}"

    # 根据 type 参数设置文件存储路径
    type_folder = {1: 'client', 2: 'nurse', 3: 'student'}.get(type, 'uncategorized')
    upload_dir = os.path.join('file_storage', type_folder, str(user_id), field_name)

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)

    # 根据 type 确定模型
    model = {1: Client, 2: Nurse, 3: Student}.get(type)
    if not model:
        return jsonify({'message': 'Invalid type'}), 400

    # 更新字段状态
    success, message = update_field_status(model, user_id,field_name)

    # 构建文件记录并保存到数据库
    new_file_record = FileUpload(
        user_id=user_id,
        field_name=field_name,
        file_path=file_path,
        type=type,
        upload_time=datetime.now()  # 记录上传时间
    )
    db.session.add(new_file_record)
    db.session.commit()
    if not success:
        return jsonify({'message': message}), 400
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 201


@route_file.route('/delete_files/<int:user_id>', methods=['POST'])
def delete_files(user_id):
    # 查找所有与用户相关的文件记录
    file_records = FileUpload.query.filter_by(user_id=user_id).all()

    for file_record in file_records:
        # 尝试删除物理文件
        try:
            if os.path.exists(file_record.file_path):
                os.remove(file_record.file_path)
        except Exception as e:
            # 如果物理文件删除失败，返回错误信息
            return jsonify({'message': f'Error deleting file: {e}'}), 500

        # 从数据库中删除文件记录
        db.session.delete(file_record)

    # 提交更改
    try:
        db.session.commit()
        return jsonify({'message': 'All files deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
