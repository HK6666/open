import json
from datetime import timedelta, datetime
from sqlite3 import IntegrityError

from flask import Flask, request, jsonify, Blueprint

# Assuming db is already initialized in your file
from application import db
from web.controllers.user.User import User

route_process = Blueprint('process_page', __name__)

class Process(db.Model):
    __tablename__ = 'processes'
    ProcessID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProcessName = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Type = db.Column(db.String(255), nullable=False)  # 新增字段
    Step = db.Column(db.Integer)  # 新增字段，表示流程的步骤

    def to_dict(self):
        return {
            'ProcessID': self.ProcessID,
            'ProcessName': self.ProcessName,
            'Description': self.Description,
            'Type': self.Typ,
            'Step': self.Step  # 返回Step值
        }

class Approval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initiator_id = db.Column(db.Integer)  # 发起人的用户ID
    status = db.Column(db.String(50))  # 审批状态，例如"pending"、"approved"、"rejected"
    process_data = db.Column(db.Text)  # 存储待更新的流程数据，可以是JSON格式
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())


class ApprovalStatus(db.Model):
    __tablename__ = 'approval_status'

    id = db.Column(db.Integer, primary_key=True)
    approval_id = db.Column(db.Integer, db.ForeignKey('approval.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # 状态如 'pending', 'approved', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ApprovalStatus {self.id} for approval {self.approval_id} by user {self.user_id}>'

@route_process.route('/<int:user_id>/request_update', methods=['POST'])
def request_update(user_id):
    data = request.get_json()
    # 创建审批记录
    approval = Approval(
        initiator_id=user_id,
        status='pending',
        process_data=json.dumps(data)  # 假设data是包含流程更新信息的JSON
    )
    db.session.add(approval)
    db.session.flush()  # 刷新会话以获取approval的ID，前提是使用了自增ID

    # 获取所有超级管理员
    super_users = User.query.filter(User.is_super == 2, User.id != user_id).all()  # 排除自己

    # 为每个超级管理员创建待审批状态记录
    for super_user in super_users:
        approval_status = ApprovalStatus(
            approval_id=approval.id,
            user_id=super_user.id,
            status='pending'
        )
        db.session.add(approval_status)

    db.session.commit()
    return jsonify({'message': 'The update request has been submitted and is awaiting approval'}), 200


@route_process.route('/approve/<int:approval_id>/<int:user_id>', methods=['POST'])
def approve(approval_id, user_id):
    # 检查是否为超级管理员
    user = User.query.get_or_404(user_id)
    if user.is_super != 2:
        return jsonify({'message': 'Only super users can approve'}), 403

    # 检查审批状态记录是否存在
    approval_status = ApprovalStatus.query.filter_by(approval_id=approval_id, user_id=user_id).first()
    if not approval_status:
        return jsonify({'message': 'Approval status not found'}), 404

    # 假设前端发送的数据中包含一个status字段，其值为'approved'或'rejected'
    data = request.get_json()
    new_status = data.get('status')

    # 更新审批状态记录
    approval_status.status = new_status
    db.session.commit()

    # 检查是否所有审批都已通过
    all_approved = not db.session.query(ApprovalStatus)\
                                   .filter(ApprovalStatus.approval_id == approval_id,
                                           ApprovalStatus.status != 'approved')\
                                   .count()

    if all_approved:
        # 所有审批都已通过，执行流程更新逻辑
        approval = Approval.query.get(approval_id)

        # 解析存储在Approval表中的process_data字段，该字段包含JSON格式的流程数据
        new_processes_data = json.loads(approval.process_data)

        # 删除现有的所有流程数据
        Process.query.filter_by(Type=new_processes_data['processes'][0]["Type"]).delete()

        # 插入新的流程数据
        for process_data in new_processes_data['processes']:
            new_process = Process(
                ProcessName=process_data["ProcessName"],
                Description=process_data["Description"],
                Type=process_data["Type"],
                Step=process_data.get("Step", 1)
            )
            db.session.add(new_process)

        approval.status = 'approved'  # 标记整个审批流程为已批准
        db.session.commit()
        return jsonify({'message': 'Approval granted and process updated'}), 200
    else:
        return jsonify({'message': 'Approval granted, waiting for other approvals'}), 200

@route_process.route('/pending_approvals/<int:user_id>', methods=['GET'])
def pending_approvals(user_id):
    # 检查是否为超级管理员
    user = User.query.get_or_404(user_id)
    if user.is_super != 2:
        return jsonify({'message': 'Only super users can view pending approvals'}), 403

    # 获取待审批记录
    pending_approvals = ApprovalStatus.query.filter_by(user_id=user_id, status='pending').join(Approval, Approval.id == ApprovalStatus.approval_id).add_columns(Approval.id, Approval.initiator_id, Approval.status, Approval.process_data).all()

    approvals_data = [{
        'approval_id': approval.id,
        'initiator_id': approval.initiator_id,
        'status': approval.status,
        'process_data': approval.process_data
    } for approval in pending_approvals]

    return jsonify(approvals_data), 200


@route_process.route('/<type>', methods=['GET'])
def get_processes_by_type(type):
    processes = Process.query.filter_by(Type=type).all()
    processes_data = [{
        'ProcessID': process.ProcessID,
        'ProcessName': process.ProcessName,
        'Description': process.Description,
        'Type': process.Type,
        'Step': process.Step
    } for process in processes]
    return jsonify(processes_data)