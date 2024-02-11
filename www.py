# -*- coding: utf-8 -*-
from application import app

# 待定（登录功能做统一拦截和处理）

# 蓝图功能
# from web.controllers.index import route_index
from web.controllers.user.User import route_user
from web.controllers.client.Student import route_student
from web.controllers.client.Nurse import route_nurse
from web.controllers.client.Client import route_client
from web.controllers.File import route_file
from web.controllers.EmailSettings import route_email

# app.register_blueprint(route_index, url_prefix = "/index" )
app.register_blueprint(route_user, url_prefix = "/user" )
app.register_blueprint(route_student, url_prefix ="/client/student")
app.register_blueprint(route_nurse, url_prefix ="/client/nurse")
app.register_blueprint(route_client, url_prefix ="/client")
app.register_blueprint(route_file, url_prefix ="/file")
app.register_blueprint(route_email, url_prefix ="/email")
