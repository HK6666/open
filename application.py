from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

# 配置加载
app.config.from_pyfile('config/base_setting.py')
app.config.from_pyfile('config/local_setting.py')

# 配置JWT扩展
app.config['JWT_SECRET_KEY'] = '123456DDDD'  # 设置JWT密钥，用于签名令牌
jwt = JWTManager(app)

# 初始化 SQLAlchemy
db = SQLAlchemy(app)
