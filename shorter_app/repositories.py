from flask import current_app
from shorter_app.models import Shorter, Stats


class BaseRespository:
    @classmethod
    def commit(cls):
        current_app.db_session.commit()


class ShorterRepository(BaseRespository):
    @classmethod
    def add(cls, shorter):
        current_app.db_session.add(shorter)
        current_app.db_session.commit()

    @classmethod
    def get(cls, code):
        return current_app.db_session.query(Shorter).filter_by(code=code).first()

    @classmethod
    def get_all(cls):
        return current_app.db_session.query(Shorter).all()


class StatsRepository(BaseRespository):
    @classmethod
    def add(self, stats):
        current_app.db_session.add(stats)
        current_app.db_session.commit()

    @classmethod
    def get(self, code):
        return Stats.query.filter(Stats.code == code).first()

    @classmethod
    def get_all(self):
        return current_app.db_session.query(Stats).all()
