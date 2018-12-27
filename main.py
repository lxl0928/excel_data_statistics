# coding: utf-8

"""
读取Excel表，统计进入数据库...


注意: main.py 不可直接使用，此代码不完全，为测试用。
"""

from datetime import datetime

from pyexcel_xls import get_data

salary_info_path = "./doc/lingquan_ningbo_salary_info.xlsx"
lingquan_beifujin_path = "./doc/lingquan_beifujin.xlsx"
ningbo_beifujin_path = "./doc/ningbo_beifujin.xlsx"
test_path = "./doc/test.xlsx"


from sqlalchemy.engine.result import RowProxy
from sqlalchemy import and_

from tables import (
    tb_lingquan_beifujin,
    tb_ningbo_beifujin,
    tb_salary_info
)

from utils import get_db_session


def read_xls_file():
    xls_data = get_data(salary_info_path)
    for sheet_n in xls_data.keys():
        data = xls_data[sheet_n]
        count = 0
        for row in data:
            # 每行数据 -> row
            if count == 0:
                count += 1
            elif count <= 16188 and count != 0 :
                count += 1
            else:
                print(row, len(row))

                xing_ming = row[0].rstrip()
                shou_ji_hao = int(row[1].rstrip())
                shen_fen_zheng = row[2].rstrip()
                ka_hao = row[3].rstrip()
                jin_e = float(row[4]) if row[4] else 0.0
                gong_si_ming = row[5].rstrip()
                dao_ru_shi_jian = datetime.strptime(row[6].rstrip(), '%Y-%m-%d %H:%M:%S') if row[6] else datetime.now()
                zhuang_tai = row[7].rstrip()
                que_ren_shi_jian = datetime.strptime(row[8].rstrip(), '%Y-%m-%d %H:%M:%S') if row[8] else datetime.now()
                yong_gong_lei_xing = row[9].rstrip() if row[9] else ''
                yu_qi_dai_kou = float(row[10]) if row[10] else 0.0
                dong_jie = float(row[11]) if row[11] else 0.0
                bei_fu_jing_zhang_hu = row[12].rstrip() if len(row) > 12 else ''
                di_san_fang_ding_dan_hao = row[13].rstrip() if len(row) > 13 else ''
                zhi_fu_zhuang_tai = row[14].rstrip() if len(row) > 14 else ''

                sql = tb_salary_info.insert().values(
                    xing_ming=xing_ming,
                    shou_ji_hao=shou_ji_hao,
                    shen_fen_zheng=shen_fen_zheng,
                    ka_hao=ka_hao,
                    jin_e=jin_e,
                    gong_si_ming=gong_si_ming,
                    dao_ru_shi_jian=dao_ru_shi_jian,
                    zhuang_tai=zhuang_tai,
                    que_ren_shi_jian=que_ren_shi_jian,
                    yong_gong_lei_xing=yong_gong_lei_xing,
                    yu_qi_dai_kou=yu_qi_dai_kou,
                    dong_jie=dong_jie,
                    bei_fu_jing_zhang_hu=bei_fu_jing_zhang_hu,
                    di_san_fang_ding_dan_hao=di_san_fang_ding_dan_hao,
                    zhi_fu_zhuang_tai=zhi_fu_zhuang_tai
                )

                with get_db_session() as session:
                    session.execute(sql)
                    print(count, ", success", "\n")

if __name__ == "__main__":
    read_xls_file()
