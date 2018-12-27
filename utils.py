ii# coding: utf-8

"""
数据库帮助类...
"""
import logging
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError

from tables import Session


@contextmanager
def get_db_session(*args, **kwargs):
    session = Session(*args, **kwargs)
    try:
        yield session
        session.commit()
    except IntegrityError as e:
        logging.error(msg="get_db_session()->报了一个IntegrityError异常: {0}".format(e))
        session.rollback()
        raise
    except Exception as e:
        logging.error(msg="get_db_session()->报了一个其它异常: {0}".format(e))
        session.rollback()
        raise
    finally:
        session.close()
