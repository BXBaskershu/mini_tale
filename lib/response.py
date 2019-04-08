from flask import make_response, jsonify
from flask_restful import marshal

from lib.prompt import AccountPrompt


class Response:
    @staticmethod
    def construct_response(dict_content):
        """返回包含dict_content数据json response

        :dict_content: 需要传输前端的数据
        :return: json response
        """
        response = make_response(jsonify(dict_content))
        return response

    @staticmethod
    def error(desc, errmsg, code=0):
        """返回包含错误的信息的response

        :desc: 错误描述
        :errmsg: 错误信息
        :code: 错误代码
        :return: json response
        """
        content = {
            'status': 1,
            'desc': desc,
            'msg': errmsg,
            'code': code
        }
        return Response.construct_response(content)

    @staticmethod
    def permission_denied():
        """ 用户没有操作权限时的response返回 """
        return Response.error(*AccountPrompt.PERMISSION_DENIED)

    @staticmethod
    def field_error(field):
        """ request请求字段出现错误时的response返回 """
        return Response.error('字段错误：[{}]'.format(field), 'invalid {}'.format(field))

    @staticmethod
    def success(desc=''):
        """ request请求成功 """
        content = {
            'status': 0,
            'msg': 'success',
            'desc': desc,
        }
        return Response.construct_response(content)

    @staticmethod
    def success_with_data(return_key, return_val, desc=''):
        """ request正常返回数据 """
        content = {
            'status': 0,
            'msg': 'success',
            'desc': desc,
            return_key: return_val
        }
        return Response.construct_response(content)

    @staticmethod
    def marshal(models, resouce_fields, envelope):
        """对一组model数据列表变成json数据并保存到respon中

        :models: 一组model类型数据的列表
        :envelope: 列表数据在json中的键名
        :resouce_fields: 字典类型，包含了model中的那些属性需要被序列化
        :return: json response
        """
        # import ipdb; ipdb.sset_trace()
        return marshal(models, resouce_fields, envelope=envelope)
