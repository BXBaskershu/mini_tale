import decimal
import inspect
import six

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import Argument, RequestParser

from lib.response import Response


class RequestType:
    GET = 'GET'
    POST = 'POST'


class CustomArgument(Argument):
    def convert(self, value, op):
        # check if we're expecting a string and the value is `None`
        if value is None and \
           inspect.isclass(self.type) and \
           issubclass(self.type, six.string_types):
            return

        # and check if we're expecting a file storage and haven't overridden `type`
        # (required because the below instantiation isn't valid for FileStorage)
        elif isinstance(value, FileStorage) and self.type == FileStorage:
            return value

        try:
            return self.type(value, self.name, op)
        except (TypeError, LookupError, ):
            try:
                if self.type is decimal.Decimal:
                    return self.type(str(value), self.name)
                else:
                    return self.type(value, self.name)
            except (TypeError, LookupError, ):
                # add list check
                if self.type == list and not isinstance(value, list):
                    raise (TypeError, LookupError, )
                return self.type(value)

    def handle_validation_error(self, error, bundle_errors):
        help_str = '(%s) ' % self.help if self.help else ''
        error_msg = ' '.join([help_str, str(error)]) if help_str else str(error)
        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            msg = {self.name: "%s" % (error_msg)}
            return error, msg
        # make msg shorter
        msg = "{}".format(self.name)
        raise BadRequest(msg)


class BaseResource(Resource):
    def __init__(self):
        self.parser = RequestParser(argument_class=CustomArgument)


class BaseController(BaseResource):
    decorators = list()

    def _route_method(self, method, request_type):
        """根据不同的method和reqeust_type返回contorller中不同的方法名

        :method: url后面的method参数
        :request_type: request请求的方法，GET还是POST方法
        :return: json类型的response
        """
        route_method = None
        if request_type == RequestType.GET:
            content = dict(msg='这是一个get方法')
            return Response.construct_response(content)
        elif request_type == RequestType.POST:
            route_method = '_post_{}'.format(method if method else 'index')
        else:
            return Response.error('路由错误', 'system routing error')

        # 如果route_method为空或者contorller中没有route_method方法
        if route_method is None or not hasattr(self, route_method):
            return Response.error('请求的方法不存在', 'method does not exist')

        func = getattr(self, route_method)

        try:
            response = func()
        except BadRequest as ex:
            return Response.field_error(ex.description)
        return response

    def get(self, method=None):
        """request请求使用GET方法后，最终调用改方法

        :self: controller的实例
        :mthod: url后面的method参数，决定接下来调用control的某一具体方法
        :return: 异常或者dict参数
        """
        return self._route_method(method, RequestType.GET)

    def post(self, method=None):
        """request请求使用POST方法后，最终调用改方法

        :self: controller的实例
        :mthod: url后面的method参数，决定接下来调用control的某一具体方法
        :return: 异常或者dict参数
        """
        return self._route_method(method, RequestType.POST)
