# @Time    : 2024/1/15 21:01
# @Author  : kai huang
# @File    : Nurse.py
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

from web.controllers.FileUpload import FileUpload

route_nurse = Blueprint('nurse_page', __name__)

from application import db
class Nurse(db.Model):
    __tablename__ = 'nurse'

    def check_all_fields_have_files(self, field_names):
        """检查给定字段是否都有文件上传记录"""
        for field_name in field_names:
            file_upload = FileUpload.query.filter_by(
                user_id=self.id, field_name=field_name).order_by(FileUpload.upload_time.desc()).first()
            if not file_upload:
                return False
        return True

    def check_all_fields_have_files2(self, field_names):
        """检查给定字段是否都有文件上传记录"""
        # 一次性获取该用户的所有文件上传记录
        uploads = FileUpload.query.filter_by(user_id=self.id).all()
        upload_field_names = {upload.field_name for upload in uploads}

        # 检查每个字段是否都在上传记录中
        for field_name in field_names:
            if field_name not in upload_field_names:
                return False
        return True

    id = db.Column(db.Integer, primary_key=True)
    barmer = db.Column(db.Integer, default=0)
    b2_course = db.Column(db.DateTime)
    b2_score = db.Column(db.Integer, default=0)
    visa_valide_until = db.Column(db.DateTime)
    extra_nurse_course = db.Column(db.DateTime)
    nurse_exam = db.Column(db.DateTime)
    Führungszeugniss = db.Column(db.DateTime)
    aapply_for_diploma = db.Column(db.DateTime)
    payment = db.Column(db.TEXT, default='[]')
    note = db.Column(db.String(255))
    email_address = db.Column(db.String(255))
    apartment_address = db.Column(db.String(255))
    german_phone_number = db.Column(db.String(255))
    china_document = db.Column(db.Integer, default=0)
    university_college_diploma_china = db.Column(db.Integer, default=0)
    nursing_major_course_list_china = db.Column(db.Integer, default=0)
    internship_work_experience_china = db.Column(db.Integer, default=0)
    nursing_certificate_china = db.Column(db.Integer, default=0)
    state_specific_application_form_china = db.Column(db.Integer, default=0)
    cv_lebenslauf_china = db.Column(db.Integer, default=0)
    vollmacht_china = db.Column(db.Integer, default=0)
    vormlose_absichtserklärung_china = db.Column(db.Integer, default=0)
    language_level_scan_china = db.Column(db.Integer, default=0)
    passport_china = db.Column(db.Integer, default=0)
    motivation_scheiben_china = db.Column(db.Integer, default=0)
    write_translator = db.Column(db.Integer, default=0)
    university_college_diploma_wt = db.Column(db.Integer, default=0)
    nursing_major_course_list_wt = db.Column(db.Integer, default=0)
    internship_work_experience_wt = db.Column(db.Integer, default=0)
    nursing_certificate_wt = db.Column(db.Integer, default=0)
    ds = db.Column(db.Integer, default=0)
    interview_date = db.Column(db.DateTime, default=None)
    offer = db.Column(db.Integer, default=0)
    contract = db.Column(db.Integer, default=0)
    erklärung_zum_beschäftigungsverhältnis = db.Column(db.Integer, default=0)
    zusatzbkatt_a = db.Column(db.Integer, default=0)
    language_enrollment_document = db.Column(db.Integer, default=0)
    nursing_school_enrollment_document = db.Column(db.Integer, default=0)
    zav = db.Column(db.Integer, default=0)
    client_id = db.Column(db.Integer, default=0)
    name = db.Column(db.String(255), default="")
    nachname = db.Column(db.String(255), default="")
    type = db.Column(db.String(255), default="")
    channel = db.Column(db.String(255), default="")
    german_level = db.Column(db.String(255), default="")
    chinese_interview_training = db.Column(db.Integer, default=0)
    interview = db.Column(db.Integer, default=0)
    german_interview_training = db.Column(db.Integer, default=0)
    employer = db.Column(db.String(255), default="")
    visa = db.Column(db.Integer, nullable=False, default=0)
    birthday = db.Column(db.DateTime, default=None)
    additional1 = db.Column(db.String(255), default="")
    additional2 = db.Column(db.String(255), default="")
    additional3 = db.Column(db.String(255), default="")
    additional4 = db.Column(db.String(255), default="")
    additional5 = db.Column(db.String(255), default="")
    additional6 = db.Column(db.String(255), default="")
    additional7 = db.Column(db.String(255), default="")
    additional8 = db.Column(db.String(255), default="")
    additional9 = db.Column(db.String(255), default="")
    additional10 = db.Column(db.String(255), default="")
    ProcessID = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self, include_file_data=True):
        nurse_dict =  {
            "id": self.id,
        "barmer": self.barmer,
        "b2_course": self.b2_course.isoformat() if self.b2_course else None,
        "b2_score": self.b2_score,
        "visa_valide_until": self.visa_valide_until.isoformat() if self.visa_valide_until else None,
        "extra_nurse_course": self.extra_nurse_course.isoformat() if self.extra_nurse_course else None,
        "nurse_exam": self.nurse_exam.isoformat() if self.nurse_exam else None,
        "Führungszeugniss": self.Führungszeugniss.isoformat() if self.Führungszeugniss else None,
        "aapply_for_diploma": self.aapply_for_diploma.isoformat() if self.aapply_for_diploma else None,
        'payment': json.loads(self.payment) if self.payment else [],
        "note": self.note,
        "email_address": self.email_address,
        "apartment_address": self.apartment_address,
        "german_phone_number": self.german_phone_number,
        "china_document": self.china_document,
        "university_college_diploma_china": self.university_college_diploma_china,
        "nursing_major_course_list_china": self.nursing_major_course_list_china,
        "internship_work_experience_china": self.internship_work_experience_china,
        "nursing_certificate_china": self.nursing_certificate_china,
        "state_specific_application_form_china": self.state_specific_application_form_china,
        "cv_lebenslauf_china": self.cv_lebenslauf_china,
        "vollmacht_china": self.vollmacht_china,
        "vormlose_absichtserklärung_china": self.vormlose_absichtserklärung_china,
        "language_level_scan_china": self.language_level_scan_china,
        "passport_china": self.passport_china,
        "motivation_scheiben_china": self.motivation_scheiben_china,
        "write_translator": self.write_translator,
        "university_college_diploma_wt": self.university_college_diploma_wt,
        "nursing_major_course_list_wt": self.nursing_major_course_list_wt,
        "internship_work_experience_wt": self.internship_work_experience_wt,
        "nursing_certificate_wt": self.nursing_certificate_wt,
        "ds": self.ds,
        "interview_date": self.interview_date.isoformat() if self.interview_date else None,
        "offer": self.offer,
        "contract": self.contract,
        "erklärung_zum_beschäftigungsverhältnis": self.erklärung_zum_beschäftigungsverhältnis,
        "zusatzbkatt_a": self.zusatzbkatt_a,
        "language_enrollment_document": self.language_enrollment_document,
        "nursing_school_enrollment_document": self.nursing_school_enrollment_document,
        "zav": self.zav,
        "client_id": self.client_id,
        "name": self.name,
        "nachname": self.nachname,
        "type": self.type,
        "channel": self.channel,
        "german_level": self.german_level,
        "chinese_interview_training": self.chinese_interview_training,
        "interview": self.interview,
        "german_interview_training": self.german_interview_training,
        "employer": self.employer,
        "visa": self.visa,
        "birthday": self.birthday.isoformat() if self.birthday else None,
        "additional1": self.additional1,
        "additional2": self.additional2,
        "additional3": self.additional3,
        "additional4": self.additional4,
        "additional5": self.additional5,
        "additional6": self.additional6,
        "additional7": self.additional7,
        "additional8": self.additional8,
        "additional9": self.additional9,
        "additional10": self.additional10,
        "ProcessID": self.ProcessID
        }

        if include_file_data:
            # 检查每个整数型字段是否有文件上传
            for field in self.__table__.columns:
                if isinstance(field.type, db.Integer):
                    field_name = field.name
                    file_upload = FileUpload.query.filter_by(
                        user_id=self.id, field_name=field_name).order_by(FileUpload.upload_time.desc()).first()
                    if file_upload:
                        nurse_dict[f"{field_name}_file_data"] = {
                            'file_path': file_upload.file_path,
                            'filename': os.path.basename(file_upload.file_path)
                        }
                    else:
                        nurse_dict[f"{field_name}_file_data"] = None

        groups = {
            'china_document': [
                'university_college_diploma_china',
                'nursing_major_course_list_china',
                'internship_work_experience_china',
                'nursing_certificate_china',
                'state_specific_application_form_china',
                'cv_lebenslauf_china',
                'vollmacht_china',
                'vormlose_absichtserklärung_china',
                'language_level_scan_china',
                'passport_china',
                'motivation_scheiben_china'
            ],
            'write_translator': [
                'university_college_diploma_wt',
                'nursing_major_course_list_wt',
                'internship_work_experience_wt',
                'nursing_certificate_wt'
            ]

        }

        for group_name, field_names in groups.items():
            nurse_dict[group_name] = 1 if self.check_all_fields_have_files(field_names) else 0

        ds_field_names = [
            'state_specific_application_form_china',
            'university_college_diploma_wt',
            'nursing_major_course_list_wt',
            'internship_work_experience_wt',
            'nursing_certificate_wt',
            'passport_china',
            'cv_lebenslauf_china',
            'vollmacht_china'
        ]
        nurse_dict['ds'] = 1 if self.check_all_fields_have_files2(ds_field_names) else 0

        zav_field_names = [
            'erklärung_zum_beschäftigungsverhältnis',
            'zusatzbkatt_a',
            'nursing_school_enrollment_document',
            'language_enrollment_document',
            'contract',
            'passport_china'
        ]
        nurse_dict['zav'] = 1 if self.check_all_fields_have_files(zav_field_names) else 0

        return nurse_dict

@route_nurse.route('', methods=['POST'])
def create_nurse():
    data = request.get_json()

    # 如果payment字段在请求数据中，将其序列化为JSON字符串
    if 'payment' in data:
        data['payment'] = json.dumps(data['payment'])

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

    # 特殊处理payment字段
    if 'payment' in data:
        data['payment'] = json.dumps(data['payment'])

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
    # 获取分页和过滤参数
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    name_search = request.args.get('name', '', type=str)
    order = request.args.get('order', 'desc', type=str)

    # 构建基础查询
    query = Nurse.query

    # 应用名称过滤
    if name_search:
        query = query.filter(Nurse.name.ilike(f"%{name_search}%"))

    # 应用排序
    if order.lower() == 'asc':
        query = query.order_by(Nurse.id.asc())
    else:
        query = query.order_by(Nurse.id.desc())

    # 执行分页查询
    paginated_nurses = query.paginate(page=page, per_page=size, error_out=False)
    nurses_data = [nurse.to_dict(include_file_data=False) for nurse in paginated_nurses.items]

    # 准备分页信息
    pagination_data = {
        'total_pages': paginated_nurses.pages,
        'total_items': paginated_nurses.total,
        'current_page': page,
        'size': size,
        'items': nurses_data
    }

    return jsonify(pagination_data), 200