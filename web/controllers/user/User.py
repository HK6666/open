# User.py
from sqlite3 import IntegrityError

from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

# Assuming db is already initialized in your file
from application import db
route_user = Blueprint('user_page', __name__)

# User Model
class User(db.Model):
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_super': self.is_super,
            'gender': self.gender,
            'phone': self.phone,
            }

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_super = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


@route_user.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(name=name).first()
    if existing_user:
        # 如果用户已存在，返回错误信息
        return jsonify({'error': 'Username already exists'}), 400

    try:
        # 如果用户名不存在，尝试创建新用户
        new_user = User(
            name=name,
            password=data.get('password'),  # 确保密码是加密的
            is_super=data.get('is_super'),
            gender=data.get('gender'),
            phone=data.get('phone')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'A database error occurred'}), 500

@route_user.route("/login", methods=['POST'])
def login():
    # 获取请求中的用户名和密码
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # 在数据库中查找用户
    user = User.query.filter_by(name=username).first()

    # 验证用户名和密码
    if user and user.password == password:
        # 创建 JWT 令牌
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token, user=user.to_dict()), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@route_user.route("/<int:user_id>", methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'user': {'name': user.name, 'phone': user.phone},'id': user.id}), 200

@route_user.route("/<int:user_id>", methods=['PUT'])
@jwt_required()
def update_user(user_id):
    # 获取当前登录用户的用户名
    current_user_name = get_jwt_identity()

    # 查询当前登录用户的信息
    current_user = User.query.filter_by(name=current_user_name).first()

    # 检查当前用户是否具有更新权限
    if not current_user or current_user.is_super not in [1, 2]:
        return jsonify({'message': 'Permission denied'}), 403

    # 查询要更新的用户
    user_to_update = User.query.filter_by(id=user_id).first()
    if not user_to_update:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # 检查并更新字段，如果字段存在于 JSON 数据中
    if 'name' in data:
        user_to_update.name = data['name']
    if 'phone' in data:
        user_to_update.phone = data['phone']
    if 'is_super' in data:
        user_to_update.is_super = data['is_super']

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200



@route_user.route("/delete/<int:user_id>", methods=['POST'])
@jwt_required()
def delete_user(user_id):
    # 获取当前登录用户的用户名
    current_user_name = get_jwt_identity()

    # 查询当前登录用户的信息
    current_user = User.query.filter_by(name=current_user_name).first()
    delete_user = User.query.filter_by(id=user_id).first()

    # 检查当前用户是否具有管理权限
    if not current_user or current_user.is_super not in [1, 2]:
        return jsonify({'message': 'Permission denied'}), 403
    if not delete_user or delete_user.is_super in [1, 2]:
        return jsonify({'message': 'delete_user Permission denied'}), 403

    # 查询要删除的用户
    user_to_delete = User.query.filter_by(id=user_id).first()
    if not user_to_delete:
        return jsonify({'message': 'User not found'}), 404

    # 检查用户是否试图删除自己（可选）
    if current_user.id == user_to_delete.id:
        return jsonify({'message': 'You cannot delete yourself'}), 403

    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


@route_user.route("/users", methods=['GET'])
# @jwt_required()
def get_users():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    # 分页查询
    paginated_users = User.query.paginate(page=page, per_page=size, error_out=False)
    users_data = [{
        'id': user.id,
        'name': user.name,
        'phone': user.phone,
        'is_super': user.is_super,
        'gender': user.gender,
    } for user in paginated_users.items]

    # 准备分页信息
    pagination_data = {
        'total_pages': paginated_users.pages,
        'total_items': paginated_users.total,
        'current_page': page,
        'size': size,
        'items': users_data
    }

    return jsonify(pagination_data), 200



