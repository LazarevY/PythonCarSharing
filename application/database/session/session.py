# from https://github.com/sandix90/sqlalchemy_basics

from logging import getLogger

from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from sqlalchemy.orm import Session

from application.database.modeles.base import BaseModel

log = getLogger()


class DBSession(object):
    _session: Session

    def __init__(self, session: Session, *args, **kwargs):
        self._session = session

    def query(self, *entities, **kwargs):
        return self._session.query(*entities, **kwargs)

    def execute_query(self, query, auto_commit=False):
        try:
            val = query(self)
            if auto_commit:
                self.commit_session()
            return val
        except SQLAlchemyError:
            self._session.rollback()
            return None

    def execute_add(self, entity, auto_commit=False):
        try:
            self.add_entity_object(entity)
            if auto_commit:
                self.commit_session()
            return True
        except SQLAlchemyError:
            self._session.rollback()
            return False

    def begin(self):
        return self._session.begin()

    def add_entity_object(self, model: BaseModel, need_flush: bool = False):
        self._session.add(model)

        if need_flush:
            self._session.flush([model])

    def delete_model(self, model: BaseModel):
        if model is None:
            log.warning(f'{__name__}: model is None')

        try:
            self._session.delete(model)
        except IntegrityError as e:
            log.error(f'`{__name__}` {e}')
        except DataError as e:
            log.error(f'`{__name__}` {e}')

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            log.error(f'`{__name__}` {e}')
            raise
        except DataError as e:
            log.error(f'`{__name__}` {e}')
            raise

        if need_close:
            self.close_session()

    def close_session(self):
        try:
            self._session.close()
        except IntegrityError as e:
            log.error(f'`{__name__}` {e}')
            raise
        except DataError as e:
            log.error(f'`{__name__}` {e}')
            raise
