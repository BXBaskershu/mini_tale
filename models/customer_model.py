from init import db

from sqlalchemy.dialects.mysql import TINYINT

from utils import get_current_timestamp


class SeaType:
    DEPT = 0  # 线索公海
    PRIVATE = 1  # 私人

    MODEL = 2
    RULE = 3
    UPLOAD = 4
    CAPTURE = 5
    ARTIFACT = 6

    FORBIDDEN = 100  # 黑名单
    REPEATED_AT_ARTIFACT = 101

    BUFFER = 11  # 代理商缓冲海，缓冲海业务已于2019年1月份下掉

    NOT_EXISTS = -1  # 入库


class SystemCustomerTag:
    F = 0  # 未接通
    I = 1  # 客户初始状态
    L = 2  # 低意向
    H = 3  # 高意向
    O = 4  # 老客户
    Z = 5  # 准成单
    W = 10  # 无效客户

    FORECAST = 11  #预警客户
    DEAD = 12  # 死海客户

    NOT_EXIST = -1  #不存在的客户

    ALL = [DEAD, W, F, I, L, H, Z, O]    # 按客户意向从低到高排序
    IFL = [I, F, L]


class CustomerInfoType:
    BASIC = 'basic'
    AD = 'ad'
    ACCOUNT = 'account'
    CARD = 'card'
    ORDER = 'order'
    COUPON = 'coupon'
    FROZEN = 'frozen'
    FENGMING_INFO = 'fengmingInfo'
    FENGMING_V3_INFO = 'fengmingV3Info'
    FENGMING_SUMMARY = 'fengmingSummary'
    CPC_AD = 'cpcAd'
    GET_CLUSTER_ACCOUNT_BY_UID = 'getClusterAccountById'


class CustomerSource:
    MODEL = 0
    CUSTOM = 1
    RULE = 2
    BM = 3
    CAPTURE = 4
    POBIN = 5
    LEAD = 6

    ADMIN_IMPORT = 7
    ARTIFACT_IMPORT = 8

    TAOMI = 9


class Customer(db.Model):
    __bind_key__ = 'mysql'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_name = db.Column(db.String(64), nullable=False, index=True)
    full_name = db.Column(db.String(128), nullable=False, index=True)
    customer_type = db.Column(TINYINT, nullable=False, default=0)  # 0公司  1个人

    sea_type = db.Column(TINYINT, nullable=False, default=SeaType.DEPT)  # obsolete
    relation_id = db.Column(db.Integer, nullable=False)
    customer_core_id = db.Column(db.Integer, nullable=False, default=0)

    system_tag_id = db.Column(TINYINT, nullable=False, default=SystemCustomerTag.I, index=True)
    customer_source = db.Column(TINYINT, nullable=False, default=CustomerSource.MODEL)

    remark = db.Column(db.Text)  # 备注
    void_reason = db.Column(TINYINT)  # 无效原因，还有效的话为NULL

    create_time = db.Column(db.Integer, nullable=False, index=True,
                            default=get_current_timestamp)  # 转变为客户的时间，系统生成

    is_frozen = db.Column(TINYINT, nullable=False, default=0)
    frozen_reason = db.Column(TINYINT)
    frozen_time = db.Column(db.Integer)

    extra = db.Column(db.String(1024))

    def __repr__(self):
        return 'Customer({full_name})'.format(full_name=self.full_name)
