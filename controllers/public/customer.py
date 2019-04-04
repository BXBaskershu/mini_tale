from controllers import BaseController
from models.customer_model import Customer


class CustomerController(BaseController):

    def _post_index(self):
        """ 请求Customer的列表数据 """
        return 'hello world'
