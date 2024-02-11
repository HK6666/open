from datetime import datetime

from flask import request, Blueprint, jsonify

from application import db
route_email = Blueprint('email', __name__)

class EmailSettings(db.Model):
    __tablename__ = 'email_settings'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    smtp_server = db.Column(db.String(255), nullable=False)
    smtp_port = db.Column(db.Integer, nullable=False)
    smtp_user = db.Column(db.String(255), nullable=False)
    smtp_password = db.Column(db.String(255), nullable=False)
    use_ssl = db.Column(db.Boolean, default=True)
    default_sender = db.Column(db.String(255))
    email_text = db.Column(db.Text)  # 新增字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port,
            "smtp_user": self.smtp_user,
            "smtp_password": self.smtp_password,
            "use_ssl": self.use_ssl,
            "default_sender": self.default_sender,
            "email_text": self.email_text,  # 新增字段
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }



@route_email.route('/settings', methods=['POST'])
def create_or_update_email_settings():
    data = request.get_json()
    email_setting = EmailSettings.query.first()

    if email_setting:
        # 更新现有设置
        for key, value in data.items():
            setattr(email_setting, key, value)
    else:
        # 创建新设置
        email_setting = EmailSettings(**data)
        db.session.add(email_setting)

    db.session.commit()
    return jsonify(email_setting.to_dict()), 201

@route_email.route('/settings', methods=['GET'])
def get_email_settings():
    email_setting = EmailSettings.query.first()
    if email_setting:
        return jsonify(email_setting.to_dict()), 200
    else:
        return jsonify({"message": "Email settings not found"}), 404
