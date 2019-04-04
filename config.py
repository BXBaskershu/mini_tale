class BaseConfig:
    """ 基础的配置文件 """
    # base
    DEBUG = False
    PORT = 5000
    HOST = '0.0.0.0'

    # flask-restful
    API_URL_PREFIX = '/api'

    @classmethod
    def init_app(cls, app):
        app.debug = cls.DEBUG
        app.port = cls.PORT
        app.host = cls.HOST


class LocalConfig(BaseConfig):
    """ 本地的配置文件 """
    # base
    DEBUG = True

    # database
    MYSQL_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3333/bx_crm'
    PG_SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123456@127.0.0.1:5555/bx_crm'
    # SQLALCHEMY_DATABASE_URI = MYSQL_SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_BINDS = {
        'mysql': MYSQL_SQLALCHEMY_DATABASE_URI,
        'pg': PG_SQLALCHEMY_DATABASE_URI,
    }


configs = {
    'local': LocalConfig,
}
