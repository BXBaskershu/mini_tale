from sqlalchemy.dialects import postgresql

from init import db


class Achievement(db.Model):
    __bind_key__ = 'pg'

    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    salesman_name = db.Column(db.String(50), nullable=False)
    salesman_id = db.Column(db.Integer, nullable=False)
    department_name = db.Column(db.String(50), nullable=False)
    department_id = db.Column(db.Integer, nullable=False)
    department_line = db.Column(postgresql.ARRAY(db.String(10)), nullable=False)
    order_type = db.Column(db.Integer, nullable=False)
    order_price = db.Column(db.Integer, nullable=False)
    order_money = db.Column(db.Integer, nullable=False)
    order_date = db.Column(postgresql.DATE, nullable=False)

    def __repr__(self):
        return 'Achievement({department_name}, {salesman_name},  {order_type})'.format(
            department_name=self.department_name,
            salesman_name=self.salesman_name,
            order_type=self.order_type
        )
