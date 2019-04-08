from init import db
from exceptions import DbCommitException


class DbMixin:

    @classmethod
    def add(cls, obj):
        db.session.add(obj)
        cls._session_commit()

    @classmethod
    def delete(cls, obj):
        db.session.delete(obj)
        cls._session_commit()

    def update(self):
        self._session_commit()

    @staticmethod
    def _session_commit():
        try:
            # 事物提交
            db.session.commit()
        except Exception:
            # 回滚
            db.session.rollback()
            raise DbCommitException()
