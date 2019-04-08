import re


class Validator:

    MOBILE_PATTERN = r'1[2-9]\d{9}'
    PHONE_PATTERN = r'0\d+'

    @staticmethod
    def validate_phone(val):
        """ 检验传入的数据是否是一个手机号码 """
        phone_regex = re.compile(Validator.MOBILE_PATTERN)
        return phone_regex.match(val) and len(val) == 11
