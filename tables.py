# coding: utf-8

"""
定义数据库表格，存储Excel数据...
"""

import os
import pymysql
from sqlalchemy import (
    MetaData, Table, Column, text, create_engine, ForeignKey
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.sql.schema import PrimaryKeyConstraint, Index, CheckConstraint
from sqlalchemy.types import SmallInteger, Integer, BigInteger, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects.mysql import DOUBLE

# 需要先去本地的mysql数据库创建tb_xxxx的DB.
mysql_conn = "mysql+pymysql://root:{}@127.0.0.1/{}?charset=utf8".format("password", "tb_xxxx")
engine = create_engine(mysql_conn, poolclass=QueuePool)

metadata = MetaData(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)

BaseModel = declarative_base()  # 创建对象的基类

# xx备付金表
tb_ningbo_beifujin = Table(
    'tb_ningbo_beifujin', metadata,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('jiao_yi_ri_qi', Integer),
    Column('ji_zhang_ri_qi', Integer),
    Column('ye_wu_lei_xing', String(256)),
    Column('shou_ru', DOUBLE),
    Column('zhi_chu', DOUBLE),
    Column('zhang_mian_yu_e', DOUBLE),
    Column('kai_hu_hang', String(256)),
    Column('xing_ming', String(64), ),
    Column('ka_hao', String(64), index=True),
    Column('bei_zhu', String(256)),
    Column('gong_si_ming', String(256)),
)

# xx备付金表
tb_lingquan_beifujin = Table(
    'tb_lingquan_beifujin', metadata,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('jiao_yi_ri_qi', Integer),
    Column('ji_zhang_ri_qi', Integer),
    Column('ye_wu_lei_xing', String(256)),
    Column('shou_ru', DOUBLE),
    Column('zhi_chu', DOUBLE),
    Column('zhang_mian_yu_e', DOUBLE),
    Column('kai_hu_hang', String(256)),
    Column('xing_ming', String(64), ),
    Column('ka_hao', String(64), index=True),
    Column('bei_zhu', String(256)),
    Column('gong_si_ming', String(256)),
)

# 工资信息表
tb_salary_info = Table(
    'tb_salary_info', metadata,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('xing_ming', String(64)),
    Column('shou_ji_hao', BigInteger, index=True),
    Column('shen_fen_zheng', String(32), index=True),
    Column('ka_hao', String(64), nullable=False, index=True),
    Column('jin_e', DOUBLE),
    Column('gong_si_ming', String(256)),
    Column('dao_ru_shi_jian', DateTime),
    Column('zhuang_tai', String(64)),
    Column('que_ren_shi_jian', DateTime),
    Column('yong_gong_lei_xing', String(64)),
    Column('yu_qi_dai_kou', DOUBLE),
    Column('dong_jie', DOUBLE),
    Column('bei_fu_jing_zhang_hu', String(64)),  # 是从哪个转出去的: xxx（工资）代表: xx备付金   为空代表: xx备付金
    Column('di_san_fang_ding_dan_hao', String(64)),
    Column('zhi_fu_zhuang_tai', String(32))
)

tb_tongji = Table(
    "tb_tongji", metadata,
    Column('id', Integer, nullable=False, primary_key=True),
    Column("name", String(64), nullable=False),  # 姓名
    Column("id_card_number", String(20), nullable=False, unique=True),  # 身份证号码
    Column("phone_number_1", String(16), nullable=False, unique=True),  # 手机号码
    Column("phone_number_2", String(16), nullable=False, unique=True),  # 手机号码
    Column("bank_card_number_1", String(24), nullable=False, unique=True),  # 银行卡号码
    Column("bank_card_number_2", String(24), nullable=True, unique=True),  # 银行卡号码
    Column("bank_name_1", String(64), nullable=False),  # 开户行1
    Column("bank_name_2", String(64), nullable=True),  # 开户行1
    Column("salary_total", DOUBLE, nullable=False),  # 工资信息表里的所发工资总额
    Column("nb_beifujin_total", DOUBLE, default=0.0),  # xx_备付金总额
    Column("lq_beifujin_total", DOUBLE, default=0.0),  # xx_备付金总额
    Column("beifujin_account", String(36), nullable=False),  # salary表标注的从哪个表转出去的
    Column("company_name", String(64)),  # 公司名字
)

# metadata.drop_all(bind=engine)
metadata.create_all(bind=engine)
