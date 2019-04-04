from flask import make_response, jsonify

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
