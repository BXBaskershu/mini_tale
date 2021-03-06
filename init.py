import os

from celery import Celery
from sqlalchemy import create_engine

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import configs

__all__ = ('db', 'app', 'celery', 'pg_engine')

config = configs[os.environ.get('tale_config_module', 'local')]


def make_celery(app):
    """ 创建一个celery对象

    http://flask.pocoo.org/docs/1.0/patterns/celery/
    """
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery


def create_app():
    """ 创建flask项目的实例 """
    app = Flask(__name__)
    db = SQLAlchemy(app)
    app.config.from_object(config)
    db.init_app(app)
    return db, app


# 创建数据库连接引擎，用于手动执行sql语句或者数据库方法
pg_engine = create_engine(config.PG_SQLALCHEMY_DATABASE_URI)

db, app = create_app()
celery = make_celery(app)
