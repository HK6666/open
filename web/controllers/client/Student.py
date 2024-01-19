# @Time    : 2024/1/14 23:31
# @Author  : kai huang
# @File    : Student.py.py
# -*- coding: utf-8 -*-
import os
from sqlite3 import IntegrityError

from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

from application import db
from web.controllers.FileUpload import FileUpload

route_student = Blueprint('student_page', __name__)

class Student(db.Model):
    __tablename__ = 'student'

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
            'payment': self.payment.isoformat() if self.payment else None,
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
        }

        if include_file_data:
            # 检查每个整数型字段是否有文件上传
            for field in self.__table__.columns:
                if isinstance(field.type, db.Integer):
                    field_name = field.name
                    file_upload = FileUpload.query.filter_by(
                        user_id=self.id, field_name=field_name).first()
                    if file_upload:
                        student_dict[f"{field_name}_file_data"] = {
                            'file_path': file_upload.file_path,
                            'filename': os.path.basename(file_upload.file_path)
                        }
                    else:
                        student_dict[f"{field_name}_file_data"] = None

        return student_dict

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nach_name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    channel = db.Column(db.String(255), nullable=False)
    german_level = db.Column(db.String(255), nullable=False)
    chinese_interview_training = db.Column(db.Integer, nullable=False)
    interview_q_and_a = db.Column(db.Integer, nullable=False)
    german_interview_training = db.Column(db.Integer, nullable=False)
    employer = db.Column(db.String(255), nullable=False)
    visa = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.DateTime)
    china_document = db.Column(db.Integer, nullable=False)
    write_translator = db.Column(db.Integer, nullable=False)
    interview_date = db.Column(db.DateTime)
    contract = db.Column(db.Integer, nullable=False)
    Erklärung_zum_Beschäftigungsverhältnis = db.Column(db.Integer, nullable=False)
    language_enrollment_document = db.Column(db.Integer, nullable=False)
    nursing_school_enrollment_document = db.Column(db.Integer, nullable=False)
    barmer = db.Column(db.Integer, nullable=False)
    b2_course = db.Column(db.DateTime)
    b2_score = db.Column(db.Integer, nullable=False)
    ausbildung_start = db.Column(db.DateTime)
    visa_valide_until = db.Column(db.DateTime)
    payment = db.Column(db.DateTime)
    note = db.Column(db.String(255), nullable=False)
    Erweitertes_Führungszeugniss = db.Column(db.DateTime)
    email_address = db.Column(db.String(255), nullable=False)
    apartment_address = db.Column(db.String(255), nullable=False)
    german_phone_number = db.Column(db.String(255), nullable=False)
    additional1 = db.Column(db.String(255), nullable=False)
    additional2 = db.Column(db.String(255), nullable=False)
    additional3 = db.Column(db.String(255), nullable=False)
    additional4 = db.Column(db.String(255), nullable=False)
    additional5 = db.Column(db.String(255), nullable=False)
    additional6 = db.Column(db.String(255), nullable=False)
    additional7 = db.Column(db.String(255), nullable=False)
    additional8 = db.Column(db.String(255), nullable=False)
    additional9 = db.Column(db.String(255), nullable=False)
    additional10 = db.Column(db.String(255), nullable=False)


@route_student.route('', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

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
            payment=data.get('payment'),  # 日期字段格式
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

    return jsonify(student.to_dict()), 200

@route_student.route('', methods=['GET'])
def get_students():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('size', 10, type=int)  # 注意这里是 'size', 不是 'per_page'

    paginated_students = Student.query.order_by(Student.id.desc()).paginate(page=page, per_page=per_page,
                                                                        error_out=False)
    students_data = [student.to_dict(include_file_data=True) for student in paginated_students.items]

    pagination_data = {
        'total_pages': paginated_students.pages,
        'total_items': paginated_students.total,
        'current_page': page,
        'per_page': per_page,
        'items': students_data
    }

    return jsonify(pagination_data), 200
