# @Time    : 2024/1/15 18:26
# @Author  : kai huang
# @File    : Client.py
# -*- coding: utf-8 -*-
import os
from datetime import datetime

from flask import Flask, request, jsonify, Blueprint
from application import db
from web.controllers.FileUpload import FileUpload

route_client = Blueprint('client_page', __name__)


class Client(db.Model):
    __tablename__ = 'client'  # 确保表名与您的数据库中的表名匹配

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    first_contact_feedback = db.Column(db.String(255), nullable=False)
    second_contact_feedback = db.Column(db.String(255), nullable=False)
    third_contact_and_feedback = db.Column(db.String(255), nullable=False)
    contract = db.Column(db.Integer, nullable=False)
    payment_terms = db.Column(db.String(255), nullable=False)
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

    def to_dict(self, include_file_data=False):
        client_dict = {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'city': self.city,
            'contact_person': self.contact_person,
            'department': self.department,
            'address': self.address,
            'phone': self.phone,
            'first_contact_feedback': self.first_contact_feedback,
            'second_contact_feedback': self.second_contact_feedback,
            'third_contact_and_feedback': self.third_contact_and_feedback,
            'contract': self.contract,
            'payment_terms': self.payment_terms,
            "additional1": self.additional1,
            "additional2": self.additional2,
            "additional3": self.additional3,
            "additional4": self.additional4,
            "additional5": self.additional5,
            "additional6": self.additional6,
            "additional7": self.additional7,
            "additional8": self.additional8,
            "additional9": self.additional9,
            "additional10": self.additional10
        }

        if include_file_data:
            # 检查每个整数型字段是否有文件上传
            for field in self.__table__.columns:
                if isinstance(field.type, db.Integer):
                    field_name = field.name
                    file_upload = FileUpload.query.filter_by(
                        user_id=self.id, field_name=field_name).first()
                    if file_upload:
                        client_dict[f"{field_name}_file_data"] = {
                            'file_path': file_upload.file_path,
                            'filename': os.path.basename(file_upload.file_path)
                        }
                    else:
                        client_dict[f"{field_name}_file_data"] = None

        return client_dict

@route_client.route('', methods=['POST'])
def create_client():
    data = request.get_json()
    client = Client(**data)
    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201

@route_client.route('/<int:client_id>', methods=['PUT'])
def update_client(client_id):
      client = Client.query.get(client_id)
      if not client:
          return jsonify({'message': 'Client not found'}), 404

      data = request.get_json()
      for key, value in data.items():
          if hasattr(client, key):
              setattr(client, key, value)

      db.session.commit()
      return jsonify(client.to_dict()), 200
@route_client.route('/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get(client_id)
    if client is None:
        return jsonify({'message': 'Client not found'}), 404
    return jsonify(client.to_dict(include_file_data=True)), 200

@route_client.route('/<int:client_id>/delete', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted successfully'}), 200

@route_client.route('/clients', methods=['GET'])
def get_clients():
    # 获取分页、搜索和排序参数
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    name_search = request.args.get('name', '', type=str)
    order = request.args.get('order', 'desc', type=str)

    # 构建基础查询
    query = Client.query

    # 应用名称过滤
    if name_search:
        query = query.filter(Client.name.ilike(f"%{name_search}%"))

    # 应用排序
    if order.lower() == 'asc':
        query = query.order_by(Client.id.asc())
    else:
        query = query.order_by(Client.id.desc())

    # 执行分页查询
    paginated_clients = query.paginate(page=page, per_page=size, error_out=False)
    clients_data = [client.to_dict(include_file_data=True) for client in paginated_clients.items]

    # 准备分页信息
    pagination_data = {
        'total_pages': paginated_clients.pages,
        'total_items': paginated_clients.total,
        'current_page': page,
        'size': size,
        'items': clients_data
    }

    return jsonify(pagination_data), 200




