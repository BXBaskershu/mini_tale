from controllers import BaseController
from lib.prompt import CommonPrompt
from lib.response import Response
from lib.validators import Validator
from models.customer_model import Customer, CustomerType


class CustomerController(BaseController):

    def _post_index(self):
        """ 请求Customer的列表数据 """
        result = {
            'total': 0,  # 当前页面的customer数量
            'page': 0,  # 当面页码
            'pages': 0,  # 总页码
            'customers': list()  # 当前customer的数据
        }
        # argument的获取与校验
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('per_page', type=int, default=20)
        args = self.parser.parse_args()

        page = args.get('page', 1)
        per_page = args.get('per_page', 20)

        # 如果page小于等于0，返回错误
        if page <= 0:
            return Response(*CommonPrompt.INVALID_PAGE)

        # 获取customer数据
        try:
            customers_page = Customer.query.order_by(Customer.id) \
                .paginate(page=page, per_page=per_page)
            pages = customers_page.pages
            customers_data = customers_page.items
            customers_json = [customer.to_json() for customer in customers_data]

            # 构造result
            result['total'] = len(customers_json)
            result['page'] = page
            result['pages'] = pages
            result['customers'] = customers_json
        except Exception as e:
            return Response.error('请求出错', str(e))

        return result

    def _post_update(self):
        """ 将Customer的类型进行更新 """
        # argument的校验与获取
        self.parser.add_argument('customer_id', type=int, required=True)
        self.parser.add_argument(
            'customer_type',
            type=int,
            required=True,
            choices=CustomerType.choices(),
            help='请传入正确的customer_type参数')
        args = self.parser.parse_args()

        customer_id = args.get('customer_id')
        customer_type = args.get('customer_type')

        # 获取具体的customer，并更新的客户类型
        try:
            customer = Customer.query.filter_by(id=customer_id).first()
            customer.customer_type = customer_type
            customer.update()
        except AttributeError:
            return Response.error('请求出错', 'custoemr_id无法定位到一个具体的customer对象')
        except Exception as e:
            return Response.error('请求出错', str(e))

        return Response.success('customer的状态修改成功')

    def _post_delete(self):
        """ 将指定的customer对象删除 """
        # argument的校验与获取
        self.parser.add_argument('customer_id', type=int, required=True)
        args = self.parser.parse_args()
        customer_id = args.get('customer_id')

        try:
            customer = Customer.query.filter_by(id=customer_id).first()
            Customer.delete(customer)
        except AttributeError:
            return Response.error('请求出错', 'custoemr_id无法定位到一个具体的customer对象')
        except Exception as e:
            return Response.error('请求出错', str(e))

        return Response.success('删除成功')

    def _post_add(self):
        """ 新增一个customer对象 """
        # argument的校验与获取
        self.parser.add_argument('short_name', type=str, required=True)
        self.parser.add_argument('full_name', type=str, required=True)
        self.parser.add_argument('telephone', type=str, required=True)
        self.parser.add_argument(
            'customer_type',
            type=int,
            required=True,
            choices=CustomerType.choices(),
            help='请传入正确的customer_type参数')
        args = self.parser.parse_args()

        short_name = args.get('short_name')
        full_name = args.get('full_name')
        telephone = args.get('telephone')
        customer_type = args.get('customer_type')

        if Customer.query.filter_by(short_name=short_name).first():
            return Response.error('请求出错', f'{short_name}已经添加在customer列表中了')

        if Customer.query.filter_by(full_name=full_name).first():
            return Response.error('请求出错', f'{full_name}已经添加在customer列表中了')

        if not Validator.validate_phone(telephone):
            return Response.error('请求出错', 'telephone不是一个有效的电话号码')

        try:
            customer = Customer(
                short_name=short_name,
                full_name=full_name,
                telephone=telephone,
                customer_type=customer_type
            )
            Customer.add(obj=customer)
        except Exception as e:
            return Response.error('请求出错', str(e))

        return Response.success('添加成功')
