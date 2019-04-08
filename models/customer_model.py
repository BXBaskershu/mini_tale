from sqlalchemy.dialects.mysql import TINYINT

from init import db
from models.mixins import DbMixin
from utils import get_current_timestamp, timestamp_to_datetime


class CustomerType:
    COMPANY = 0  # 公司
    PERSONAL = 1  # 个人

    @staticmethod
    def choices():
        return (CustomerType.COMPANY, CustomerType.PERSONAL)


def customer_type_mapping(_type):
    _mapping = {
        CustomerType.COMPANY: '公司用户',
        CustomerType.PERSONAL: '个人用户'
    }
    return _mapping.get(_type)


class Customer(DbMixin, db.Model):
    __bind_key__ = 'mysql'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    full_name = db.Column(db.String(128), nullable=False, unique=True, index=True)
    customer_type = db.Column(TINYINT, nullable=False, default=CustomerType.COMPANY)
    telephone = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.Integer, nullable=False, default=get_current_timestamp)

    def __repr__(self):
        return 'Customer({full_name}, {telephone})'.format(
            full_name=self.full_name,
            telephone=self.telephone)

    def to_json(self):
        """ 将customer装成dict格式的数据，并且字典中的值必须都可以直接被序列化 """
        customer_type = customer_type_mapping(self.customer_type)
        create_time = timestamp_to_datetime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')

        customer_json = dict(
            short_name=self.short_name,
            full_name=self.full_name,
            customer_type=customer_type,
            telephone=self.telephone,
            create_time=create_time
        )
        return customer_json
