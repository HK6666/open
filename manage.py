# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 21:39
# @Author  : kai huang
# @File    : manage.py.py

from application import app
import www
def main():
    app.run(host='0.0.0.0', port=app.config['SERVER_PORT'], use_reloader=True)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
