# -*- coding: utf-8 -*-
from application import app

# 待定（登录功能做统一拦截和处理）

# 蓝图功能
# from web.controllers.index import route_index
from web.controllers.user.User import route_user
from web.controllers.student.Student import route_client
#
# app.register_blueprint(route_index, url_prefix = "/index" )
app.register_blueprint(route_user, url_prefix = "/user" )
app.register_blueprint(route_client, url_prefix ="/client")
