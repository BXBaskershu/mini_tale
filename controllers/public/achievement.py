"""
从销售、部门、产品类型三个维度的业绩统计api接口
"""
from datetime import date

from sqlalchemy import func

from controllers import BaseController
from lib.response import Response
from models.achievement_model import Achievement


class AchievementController(BaseController):

    def _get_salesman(self):
        """ 销售在一段时间内不同产品类型的业绩 """
        result = {
            'salesman_name': '',  # 销售员的姓名
            'salesman_id': '',  # 销售员的主键id
            'start_date': '',  # 业绩统计的起始日期
            'end_date': '',  # 业绩统计的结束日期
            'achievements': list()  # 具体的业绩数据
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
                result['achievements'].append(achievement_json)
        except Exception as e:
            return Response.error('请求出错', str(e))

        return result
