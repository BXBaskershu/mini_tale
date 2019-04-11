"""
从销售、部门、产品类型三个维度的业绩统计api接口
"""
from datetime import date

from sqlalchemy import func, or_, cast, VARCHAR

from controllers import BaseController
from lib.response import Response
from models.achievement_model import Achievement


class AchievementController(BaseController):

    def _get_salesman(self):
        """ 销售维度的业绩统计 """
        result = {
            'salesman_name': '',  # 销售员的姓名
            'salesman_id': '',  # 销售员的主键id
            'start_date': '',  # 业绩统计的起始日期
            'end_date': '',  # 业绩统计的结束日期
            'achievements': dict()  # 具体的业绩数据
        }
        # argument
        self.parser.add_argument('salesman', type=int, required=True)  # 销售员的用户id
        self.parser.add_argument('start_date', type=int, required=True)
        self.parser.add_argument('end_date', type=int, required=True)
        args = self.parser.parse_args()

        salesman_id = args.get('salesman')
        start_timestamp = args.get('start_date')
        end_timestamp = args.get('end_date')
        start_date = date.fromtimestamp(start_timestamp)
        end_date = date.fromtimestamp(end_timestamp)

        try:
            # 找出这段时间内销售不同类型产品的业绩
            achievements = Achievement.query.with_entities(
                Achievement.salesman_name,
                Achievement.salesman_id,
                Achievement.order_type,
                func.sum(Achievement.order_money).label('sum_money'),
                func.sum(Achievement.order_price).label('sum_price')
            ).filter(
                Achievement.salesman_id==salesman_id,
                Achievement.order_date.between(start_date, end_date)
            ).group_by(
                Achievement.salesman_name,
                Achievement.salesman_id,
                Achievement.order_type
            )

            # 如果销售在这一段时间内没有业绩
            if len(list(achievements)) <= 0:
                return Response.construct_response('该销售员在这一段时间内没有业绩')

            # 构造result
            result['salesman_name'] = achievements[0].salesman_name
            result['salesman_id'] = achievements[0].salesman_id
            result['start_date'] = start_date.strftime('%Y-%m-%d')
            result['end_date'] = end_date.strftime('%Y-%m-%d')
            for achievement in achievements:
                achievement_json = {
                    'order_type': achievement.order_type,
                    'sum_money': achievement.sum_money,
                    'sum_price': achievement.sum_price,
                }
                result['achievements'][str(achievement.order_type)] = achievement_json
        except Exception as e:
            return Response.error('请求出错', str(e))

        return result

    def _get_department(self):
        """ 部门维度的业绩统计 """
        result = {
            'department_id': '',  # 部门ID
            'start_date': '',  # 业绩统计的起始日期
            'end_date': '',  # 业绩统计的结束日期
            'achievements': dict()  # 具体的业绩数据
        }
        # arguments
        self.parser.add_argument('department', type=int, required=True)  # 部门ID
        self.parser.add_argument('start_date', type=int, required=True)
        self.parser.add_argument('end_date', type=int, required=True)
        args = self.parser.parse_args()

        department_id = args.get('department')
        start_timestamp = args.get('start_date')
        end_timestamp = args.get('end_date')
        start_date = date.fromtimestamp(start_timestamp)
        end_date = date.fromtimestamp(end_timestamp)

        try:
            # 找出这段时间内部门及下属部门不同类型产品的业绩
            achievements = Achievement.query.with_entities(
                Achievement.order_type,
                func.sum(Achievement.order_money).label('sum_money'),
                func.sum(Achievement.order_price).label('sum_price')
            ).filter(
                Achievement.order_date.between(start_date, end_date),
                or_(
                    Achievement.department_id==department_id,
                    Achievement.department_line.any(str(department_id))
                )
            ).group_by(
                Achievement.order_type
            )
            # 构造result
            result['department_id'] = department_id
            result['start_date'] = start_date.strftime('%Y-%m-%d')
            result['end_date'] = end_date.strftime('%Y-%m-%d')
            for achievement in achievements:
                achievement_json = {
                    'order_type': achievement.order_type,
                    'sum_money': achievement.sum_money,
                    'sum_price': achievement.sum_price,
                }
                result['achievements'][achievement.order_type] = achievement_json
        except Exception as e:
            return Response.error('请求出错', str(e))

        return result

    def _get_order_type(self):
        """ 完成产品类型维度的业绩统计 """
        result = {
            'order_type': '',  # 产品类型
            'start_date': '',  # 业绩统计的起始日期
            'end_date': '',  # 业绩统计的结束日期
            'achievements': dict()  # 具体的业绩数据
        }
        # argumengts
        self.parser.add_argument('order_type', type=int, required=True)  # 产品类型
        self.parser.add_argument('start_date', type=int, required=True)
        self.parser.add_argument('end_date', type=int, required=True)
        args = self.parser.parse_args()

        order_type = args.get('order_type')
        start_timestamp = args.get('start_date')
        end_timestamp = args.get('end_date')
        start_date = date.fromtimestamp(start_timestamp)
        end_date = date.fromtimestamp(end_timestamp)

        try:
            # 找出这段时间部门不同类型产品的业绩, 这里将部门和部门线数据拼称一个列表
            achievements = Achievement.query.with_entities(
                func.array_append(
                    Achievement.department_line,
                    cast(Achievement.department_id, VARCHAR(50))
                ).label('department_line'),
                func.sum(Achievement.order_money).label('sum_money'),
                func.sum(Achievement.order_price).label('sum_price')
            ).filter(
                Achievement.order_type==order_type,
                Achievement.order_date.between(start_date, end_date)
            ).group_by(
                Achievement.department_id,
                Achievement.department_line
            )
            # 构造result
            result['order_type'] = order_type
            result['start_date'] = start_date.strftime('%Y-%m-%d')
            result['end_date'] = end_date.strftime('%Y-%m-%d')
            for achievement in achievements:
                for department in achievement.department_line:
                    if department not in result['achievements']:
                        # 如果当前部门在数据中没有，则作为一条新数据添加进achievements中
                        achievement_json = {
                            'department': department,
                            'sum_money': achievement.sum_money,
                            'sum_price': achievement.sum_price,
                        }
                        result['achievements'][department] = achievement_json
                    else:
                        # 如果部门已经在achievements中了，直接累加
                        result['achievements'][department]['sum_money'] += achievement.sum_money
                        result['achievements'][department]['sum_price'] += achievement.sum_price
        except Exception as e:
            return Response.error('请求出错', str(e))

        return result
