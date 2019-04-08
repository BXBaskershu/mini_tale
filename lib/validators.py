import re


class Validator:

    PHONE_PATTERN = r'0\d+'

    @staticmethod
    def validate_phone(val):
        """ 检验传入的数据是否是一个电话号码 """
        phone_regex = re.compile(Validator.PHONE_PATTERN)
        return phone_regex.match(val) and len(val) >= 6 and len(val) <= 13
