# -*- coding: utf-8 -*-
from application import app

# 待定（登录功能做统一拦截和处理）

# 蓝图功能
# from web.controllers.index import route_index
from web.controllers.user.User import route_user
#
# app.register_blueprint(route_index, url_prefix = "/index" )
app.register_blueprint(route_user, url_prefix = "/user" )
