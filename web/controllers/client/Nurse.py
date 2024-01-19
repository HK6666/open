# @Time    : 2024/1/15 21:01
# @Author  : kai huang
# @File    : Nurse.py
# -*- coding: utf-8 -*-
import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

from web.controllers.FileUpload import FileUpload

route_nurse = Blueprint('nurse_page', __name__)

from application import db
class Nurse(db.Model):
    __tablename__ = 'nurse'

    id = db.Column(db.Integer, primary_key=True)
    barmer = db.Column(db.Integer, default=0)
    b2_course = db.Column(db.DateTime)
    b2_score = db.Column(db.Integer, default=0)
    visa_valide_until = db.Column(db.DateTime)
    extra_nurse_course = db.Column(db.DateTime)
    nurse_exam = db.Column(db.DateTime)
    Führungszeugniss = db.Column(db.DateTime)
    aapply_for_diploma = db.Column(db.DateTime)
    payment = db.Column(db.DateTime)
    note = db.Column(db.String(255))
    email_address = db.Column(db.String(255))
    apartment_address = db.Column(db.String(255))
    german_phone_number = db.Column(db.String(255))

    def to_dict(self, include_file_data=False):
        nurse_dict =  {
            'id': self.id,
            'barmer': self.barmer,
            'b2_course': self.b2_course.isoformat() if self.b2_course else None,
            'b2_score': self.b2_score,
            'visa_valide_until': self.visa_valide_until.isoformat() if self.visa_valide_until else None,
            'extra_nurse_course': self.extra_nurse_course.isoformat() if self.extra_nurse_course else None,
            'nurse_exam': self.nurse_exam.isoformat() if self.nurse_exam else None,
            'Führungszeugniss': self.Führungszeugniss.isoformat() if self.Führungszeugniss else None,
            'aapply_for_diploma': self.aapply_for_diploma.isoformat() if self.aapply_for_diploma else None,
            'payment': self.payment.isoformat() if self.payment else None,
            'note': self.note,
            'email_address': self.email_address,
            'apartment_address': self.apartment_address,
            'german_phone_number': self.german_phone_number
        }

        if include_file_data:
            # 检查每个整数型字段是否有文件上传
            for field in self.__table__.columns:
                if isinstance(field.type, db.Integer):
                    field_name = field.name
                    file_upload = FileUpload.query.filter_by(
                        user_id=self.id, field_name=field_name).first()
                    if file_upload:
                        nurse_dict[f"{field_name}_file_data"] = {
                            'file_path': file_upload.file_path,
                            'filename': os.path.basename(file_upload.file_path)
                        }
                    else:
                        nurse_dict[f"{field_name}_file_data"] = None

        return nurse_dict

@route_nurse.route('', methods=['POST'])
def create_nurse():
    data = request.get_json()
    nurse = Nurse(**data)
    db.session.add(nurse)
    db.session.commit()
    return jsonify(nurse.to_dict()), 201

@route_nurse.route('/<int:nurse_id>', methods=['GET'])
def get_nurse(nurse_id):
    nurse = Nurse.query.get(nurse_id)
    if nurse is None:
        return jsonify({'message': 'Nurse not found'}), 404
    return jsonify(nurse.to_dict()), 200

@route_nurse.route('/<int:nurse_id>', methods=['PUT'])
def update_nurse(nurse_id):
    nurse = Nurse.query.get(nurse_id)
    if not nurse:
        return jsonify({'message': 'Nurse not found'}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(nurse, key):
            setattr(nurse, key, value)

    try:
        db.session.commit()
        return jsonify(nurse.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@route_nurse.route('/<int:nurse_id>/delete', methods=['POST'])
def delete_nurse(nurse_id):
    nurse = Nurse.query.get(nurse_id)
    if not nurse:
        return jsonify({'message': 'Nurse not found'}), 404

    db.session.delete(nurse)
    db.session.commit()
    return jsonify({'message': 'Nurse deleted successfully'}), 200

@route_nurse.route('/nurses', methods=['GET'])
def get_nurses():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)  # 使用 'size' 作为每页大小的参数

    # 分页查询
    paginated_nurses = Nurse.query.order_by(Nurse.id.desc()).paginate(page=page, per_page=size, error_out=False)
    nurses_data = [nurse.to_dict(include_file_data=True) for nurse in paginated_nurses.items]

    # 准备分页信息
    pagination_data = {
        'total_pages': paginated_nurses.pages,
        'total_items': paginated_nurses.total,
        'current_page': page,
        'size': size,
        'items': nurses_data
    }

    return jsonify(pagination_data), 200
