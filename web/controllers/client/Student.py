# @Time    : 2024/1/14 23:31
# @Author  : kai huang
# @File    : Student.py.py
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from sqlite3 import IntegrityError

from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

from application import db
from web.controllers.FileUpload import FileUpload

route_student = Blueprint('student_page', __name__)


class Student(db.Model):
    __tablename__ = 'student'

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

    def to_dict(self, include_file_data=False):
        student_dict =  {
            'id': self.id,
            'name': self.name,
            'nach_name': self.nach_name,
            'type': self.type,
            'channel': self.channel,
            'german_level': self.german_level,
            'chinese_interview_training': self.chinese_interview_training,
            'interview_q_and_a': self.interview_q_and_a,
            'german_interview_training': self.german_interview_training,
            'employer': self.employer,
            'visa':self.visa,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'china_document': self.china_document,
            'write_translator': self.write_translator,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None,
            'contract': self.contract,
            'Erklärung_zum_Beschäftigungsverhältnis': self.Erklärung_zum_Beschäftigungsverhältnis,
            'language_enrollment_document': self.language_enrollment_document,
            'nursing_school_enrollment_document': self.nursing_school_enrollment_document,
            'barmer': self.barmer,
            'b2_course': self.b2_course.isoformat() if self.b2_course else None,
            'b2_score': self.b2_score,
            'ausbildung_start': self.ausbildung_start.isoformat() if self.ausbildung_start else None,
            'visa_valide_until': self.visa_valide_until.isoformat() if self.visa_valide_until else None,
            'payment': json.loads(self.payment) if self.payment else [],
            'note': self.note,
            'Erweitertes_Führungszeugniss': self.Erweitertes_Führungszeugniss.isoformat() if self.Erweitertes_Führungszeugniss else None,
            'email_address': self.email_address,
            'apartment_address': self.apartment_address,
            'german_phone_number': self.german_phone_number,
            'additional1': self.additional1,
            'additional2': self.additional2,
            'additional3': self.additional3,
            'additional4': self.additional4,
            'additional5': self.additional5,
            'additional6': self.additional6,
            'additional7': self.additional7,
            'additional8': self.additional8,
            'additional9': self.additional9,
            'additional10': self.additional10,
            'abschlusszeugnis_oberstufe_china_document': self.abschlusszeugnis_oberstufe_china_document,
            'abschlusszeugnis_fachhochschule_china_document': self.abschlusszeugnis_fachhochschule_china_document,
            'leistungszeugni_oberstufe_china_document': self.leistungszeugni_oberstufe_china_document,
            'leistungszeugnis_fachhochschule_china_document': self.leistungszeugnis_fachhochschule_china_document,
            'passport_china_document': self.passport_china_document,
            'vollmacht_china_document': self.vollmacht_china_document,
            'cv_lebenslauf_china_document': self.cv_lebenslauf_china_document,
            'antrag_auf_bewertung_china_document': self.antrag_auf_bewertung_china_document,
            'vormlose_absichtserklärung_china_document': self.vormlose_absichtserklärung_china_document,
            'motivation_schreiben_china_document': self.motivation_schreiben_china_document,
            'language_level_scan_china_document': self.language_level_scan_china_document,
            'passport_write_translator': self.passport_write_translator,
            'abschlusszeugnis_oberstufe_write_translator': self.abschlusszeugnis_oberstufe_write_translator,
            'leistungszeugnis_oberstufe_write_translator': self.leistungszeugnis_oberstufe_write_translator,
            'passport_sc': self.passport_sc,
            'abschlusszeugnis_oberstufe_sc': self.abschlusszeugnis_oberstufe_sc,
            'leistungszeugnis_oberstufe_sc': self.leistungszeugnis_oberstufe_sc,
            'antrag_auf_bewertung_sc': self.antrag_auf_bewertung_sc,
            'contract_sc': self.contract_sc,
            'erklärung_zum_eschäftigungsverhältnis_zav': self.erklärung_zum_eschäftigungsverhältnis_zav,
            'vollmacht_zav': self.vollmacht_zav,
            'contract_zav': self.contract_zav,
            'language_enrollment_document_zav': self.language_enrollment_document_zav,
            'nursing_school_enrollment_document_zav': self.nursing_school_enrollment_document_zav,
            'passport_zav': self.passport_zav,
            'client_id': self.client_id,
            'zav': self.zav,
            'sc': self.sc,
            "ProcessID": self.ProcessID
        }

        if include_file_data:
            # 检查每个整数型字段是否有文件上传
            for field in self.__table__.columns:
                if isinstance(field.type, db.Integer):
                    field_name = field.name
                    # 获取最后上传的文件
                    file_upload = FileUpload.query.filter_by(
                        user_id=self.id, field_name=field_name).order_by(FileUpload.upload_time.desc()).first()
                    if file_upload:
                        student_dict[f"{field_name}_file_data"] = {
                            'file_path': file_upload.file_path,
                            'filename': os.path.basename(file_upload.file_path)
                        }
                    else:
                        student_dict[f"{field_name}_file_data"] = None

        groups = {
            'china_document': [
                'abschlusszeugnis_oberstufe_china_document',
                'abschlusszeugnis_fachhochschule_china_document',
                'leistungszeugni_oberstufe_china_document',
                'leistungszeugnis_fachhochschule_china_document',
                'passport_china_document',
                'vollmacht_china_document',
                'cv_lebenslauf_china_document',
                'antrag_auf_bewertung_china_document',
                'vormlose_absichtserklärung_china_document',
                'motivation_schreiben_china_document',
                'language_level_scan_china_document'
            ],
            'write_translator': [
                'passport_write_translator',
                'abschlusszeugnis_oberstufe_write_translator',
                'leistungszeugnis_oberstufe_write_translator'
            ],
            'sc': [
                'passport_sc',
                'abschlusszeugnis_oberstufe_sc',
                'leistungszeugnis_oberstufe_sc',
                'antrag_auf_bewertung_sc',
                'contract_sc'
            ],
            'zav': [
                'erklärung_zum_eschäftigungsverhältnis_zav',
                'vollmacht_zav',
                'contract_zav',
                'language_enrollment_document_zav',
                'nursing_school_enrollment_document_zav',
                'passport_zav'
            ]
        }

        # 检查并设置每组字段
        for group_name, field_names in groups.items():
            student_dict[group_name] = 1 if self.check_all_fields_have_files(field_names) else 0

        # 特殊处理 'sc' 字段
        sc_field_names = [
                'passport_write_translator',
                'abschlusszeugnis_oberstufe_write_translator',
                'leistungszeugnis_oberstufe_write_translator',
                'antrag_auf_bewertung_china_document',
                'contract'
        ]
        student_dict['sc'] = 1 if self.check_all_fields_have_files2(sc_field_names) else 0

        zav_field_names = [
            'Erklärung_zum_Beschäftigungsverhältnis',
            'vollmacht_china_document',
            'contract',
            'language_enrollment_document',
            'nursing_school_enrollment_document',
            'passport_write_translator'
        ]
        student_dict['zav'] = 1 if self.check_all_fields_have_files2(zav_field_names) else 0

        return student_dict

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, default="")
    nach_name = db.Column(db.String(255), nullable=False, default="")
    type = db.Column(db.String(255), nullable=False, default="")
    channel = db.Column(db.String(255), nullable=False, default="")
    german_level = db.Column(db.String(255), nullable=False, default="")
    chinese_interview_training = db.Column(db.Integer, nullable=False, default=0)
    interview_q_and_a = db.Column(db.Integer, nullable=False, default=0)
    german_interview_training = db.Column(db.Integer, nullable=False, default=0)
    employer = db.Column(db.String(255), nullable=False, default="")
    visa = db.Column(db.Integer, nullable=False, default=0)
    birthday = db.Column(db.DateTime, default=None)  # 默认为 None，表示没有设置
    china_document = db.Column(db.Integer, nullable=False, default=0)
    write_translator = db.Column(db.Integer, nullable=False, default=0)
    interview_date = db.Column(db.DateTime, default=None)
    contract = db.Column(db.Integer, nullable=False, default=0)
    Erklärung_zum_Beschäftigungsverhältnis = db.Column(db.Integer, nullable=False, default=0)
    language_enrollment_document = db.Column(db.Integer, nullable=False, default=0)
    nursing_school_enrollment_document = db.Column(db.Integer, nullable=False, default=0)
    barmer = db.Column(db.Integer, nullable=False, default=0)
    b2_course = db.Column(db.DateTime, default=None)
    b2_score = db.Column(db.Integer, nullable=False, default=0)
    ausbildung_start = db.Column(db.DateTime, default=None)
    visa_valide_until = db.Column(db.DateTime, default=None)
    payment = db.Column(db.TEXT, default='[]')
    note = db.Column(db.String(255), nullable=False, default="")
    Erweitertes_Führungszeugniss = db.Column(db.DateTime, default=None)
    email_address = db.Column(db.String(255), nullable=False, default="")
    apartment_address = db.Column(db.String(255), nullable=False, default="")
    german_phone_number = db.Column(db.String(255), nullable=False, default="")
    additional1 = db.Column(db.String(255), nullable=False, default="")
    additional2 = db.Column(db.String(255), nullable=False, default="")
    additional3 = db.Column(db.String(255), nullable=False, default="")
    additional4 = db.Column(db.String(255), nullable=False, default="")
    additional5 = db.Column(db.String(255), nullable=False, default="")
    additional6 = db.Column(db.String(255), nullable=False, default="")
    additional7 = db.Column(db.String(255), nullable=False, default="")
    additional8 = db.Column(db.String(255), nullable=False, default="")
    additional9 = db.Column(db.String(255), nullable=False, default="")
    additional10 = db.Column(db.String(255), nullable=False, default="")
    abschlusszeugnis_oberstufe_china_document = db.Column(db.Integer, default=0)
    abschlusszeugnis_fachhochschule_china_document = db.Column(db.Integer, default=0)
    leistungszeugni_oberstufe_china_document = db.Column(db.Integer, default=0)
    leistungszeugnis_fachhochschule_china_document = db.Column(db.Integer, default=0)
    passport_china_document = db.Column(db.Integer, default=0)
    vollmacht_china_document = db.Column(db.Integer, default=0)
    cv_lebenslauf_china_document = db.Column(db.Integer, default=0)
    antrag_auf_bewertung_china_document = db.Column(db.Integer, default=0)
    vormlose_absichtserklärung_china_document = db.Column(db.Integer, default=0)
    motivation_schreiben_china_document = db.Column(db.Integer, default=0)
    language_level_scan_china_document = db.Column(db.Integer, default=0)
    passport_write_translator = db.Column(db.Integer, default=0)
    abschlusszeugnis_oberstufe_write_translator = db.Column(db.Integer, default=0)
    leistungszeugnis_oberstufe_write_translator = db.Column(db.Integer, default=0)
    passport_sc = db.Column(db.Integer, default=0)
    abschlusszeugnis_oberstufe_sc = db.Column(db.Integer, default=0)
    leistungszeugnis_oberstufe_sc = db.Column(db.Integer, default=0)
    antrag_auf_bewertung_sc = db.Column(db.Integer, default=0)
    contract_sc = db.Column(db.Integer, default=0)
    erklärung_zum_eschäftigungsverhältnis_zav = db.Column(db.Integer, default=0)
    vollmacht_zav = db.Column(db.Integer, default=0)
    contract_zav = db.Column(db.Integer, default=0)
    language_enrollment_document_zav = db.Column(db.Integer, default=0)
    nursing_school_enrollment_document_zav = db.Column(db.Integer, default=0)
    passport_zav = db.Column(db.Integer, default=0)
    client_id = db.Column(db.Integer, default=0)
    zav = db.Column(db.Integer, default=0)
    sc = db.Column(db.Integer, default=0)
    ProcessID = db.Column(db.Integer, nullable=False, default=0)


@route_student.route('', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400
    payment_data = data.get('payment', [])
    payment_data = json.dumps(payment_data)

    try:
        new_student = Student(
            name=data.get('name'),
            nach_name=data.get('nach_name'),
            type=data.get('type'),
            channel=data.get('channel'),
            german_level=data.get('german_level'),
            chinese_interview_training=data.get('chinese_interview_training'),
            interview_q_and_a=data.get('interview_q_and_a'),
            german_interview_training=data.get('german_interview_training'),
            employer=data.get('employer'),
            visa=data.get('visa'),
            birthday=data.get('birthday'),  # 确保日期字段以正确的格式传入
            china_document=data.get('china_document'),
            write_translator=data.get('write_translator'),
            interview_date=data.get('interview_date'),  # 同样，确保日期字段格式正确
            contract=data.get('contract'),
            Erklärung_zum_Beschäftigungsverhältnis=data.get('Erklärung_zum_Beschäftigungsverhältnis'),
            language_enrollment_document=data.get('language_enrollment_document'),
            nursing_school_enrollment_document=data.get('nursing_school_enrollment_document'),
            barmer=data.get('barmer'),
            b2_course=data.get('b2_course'),  # 日期字段格式
            b2_score=data.get('b2_score'),
            ausbildung_start=data.get('ausbildung_start'),  # 日期字段格式
            visa_valide_until=data.get('visa_valide_until'),  # 日期字段格式
            payment=payment_data,  # 日期字段格式
            note=data.get('note'),
            Erweitertes_Führungszeugniss=data.get('Erweitertes_Führungszeugniss'),  # 日期字段格式
            email_address=data.get('email_address'),
            apartment_address=data.get('apartment_address'),
            german_phone_number=data.get('german_phone_number'),
            additional1=data.get('additional1'),
            additional2=data.get('additional2'),
            additional3=data.get('additional3'),
            additional4=data.get('additional4'),
            additional5=data.get('additional5'),
            additional6=data.get('additional6'),
            additional7=data.get('additional7'),
            additional8=data.get('additional8'),
            additional9=data.get('additional9'),
            additional10=data.get('additional10')
        )

        # 将新学生添加到数据库
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict()), 201
    except KeyError as e:
        # 如果缺少必需的字段
        return jsonify({'message': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        # 如果发生其他错误
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@route_student.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # 只更新传入的字段
    for key, value in data.items():
        if key == 'payment' and isinstance(value, list):
            # 序列化 payment 数组
            value = json.dumps(value)

        if hasattr(student, key):
            setattr(student, key, value)

    try:
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@route_student.route('/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@route_student.route('/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    return jsonify(student.to_dict(include_file_data=True)), 200

@route_student.route('', methods=['GET'])
def get_students():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('size', 10, type=int)
    name_search = request.args.get('name', '', type=str)
    order = request.args.get('order', 'desc', type=str)

    # 构建查询并根据 name 参数进行过滤
    query = Student.query
    if name_search:
        query = query.filter(Student.name.ilike(f"%{name_search}%"))

    # 根据 order 参数进行排序
    if order.lower() == 'asc':
        query = query.order_by(Student.id.asc())
    else:
        query = query.order_by(Student.id.desc())

    paginated_students = query.paginate(page=page, per_page=per_page, error_out=False)
    students_data = [student.to_dict(include_file_data=False) for student in paginated_students.items]

    pagination_data = {
        'total_pages': paginated_students.pages,
        'total_items': paginated_students.total,
        'current_page': page,
        'per_page': per_page,
        'items': students_data
    }

    return jsonify(pagination_data), 200
