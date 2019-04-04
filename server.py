from init import app
from urls import public_urls

from flask_restful import Api


def route():
    """ 使用flask-restful添加路由路径 """
    app_prefix = app.config.get('API_URL_PREFIX', '/api')
    api = Api(app, prefix=app_prefix)
    for url in public_urls:
        api.add_resource(*url)


def start_server():
    """ 启动flask项目 """
    route()  # 加载路由
    app.run()  # 启动程序


if __name__ == '__main__':
    start_server()
