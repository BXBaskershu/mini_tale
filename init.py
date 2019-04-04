import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import configs

__all__ = ('db', 'app')

config = configs[os.environ.get('tale_config_module', 'local')]


def create_app():
    """ 创建flask项目的实例 """
    app = Flask(__name__)
    db = SQLAlchemy(app)
    app.config.from_object(config)
    db.init_app(app)
    return db, app


db, app = create_app()
