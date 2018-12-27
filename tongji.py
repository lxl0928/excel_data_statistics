# coding: utf-8

"""
各种数据统计，结果输出...
"""

import sys
from pprint import pprint
from decimal import Decimal
from datetime import datetime
from collections import OrderedDict

from pyexcel_xls import save_data

from tables import (
    tb_lingquan_beifujin,
    tb_ningbo_beifujin,
    tb_salary_info,
)
from utils import get_db_session

cnt_now = datetime.now()
cnt_time = "{}{}{}{}{}".format(cnt_now.year, cnt_now.month, cnt_now.day, cnt_now.hour, cnt_now.minute)

result_path = "./doc/{}.xlsx".format(cnt_time)


def get_salary_info_data():
    """ 从薪资表读取数据

    :return:
    """
    sql = tb_salary_info.select().where(
        tb_salary_info.c.id != 0
    )
    with get_db_session() as session:
        salary_data = session.execute(sql).fetchall()

    return salary_data


def get_ningbo_beifujin():
    """ 从xxx备付金读取数据

    :return:
    """
    sql = tb_ningbo_beifujin.select().where(
        tb_ningbo_beifujin.c.id != 0
    )
    with get_db_session() as session:
        ningbo_data = session.execute(sql).fetchall()

    return ningbo_data


def get_linquan_beifujin():
    """ 从xxxxx备付金读取数据

    :return:
    """
    sql = tb_lingquan_beifujin.select().where(
        tb_lingquan_beifujin.c.id != 0
    )
    with get_db_session() as session:
        linquan_data = session.execute(sql).fetchall()

    return linquan_data


def assemble_salary_data(data):
    """ 组装薪资表的数据

    :param data:
        {
            "身份证号_1": {
                "name": "xxx",
                "id_card_number": "xxxxxxxxxx",
                "phone_number_1": "xxxxxxxxxxxx",
                "phone_number_2": "xxxxxxxxxxxx",
                "bank_card_number_1": "xxxxxxxxxxxxxxxx",
                "bank_card_number_2": "xxxxxxxxxxxxxxxxxxxx",
                "bank_card_number_3": "xxxxxxxxxxxxxxxxxxxx",
                "bank_name_1": "中国建设银行",
                "bank_name_2": "中国工商银行",
                "bank_name_3": "中国工商银行",
                "salary_total": 8000.40,
                "nb_total": 4000.00,
                "lq_total": 4000.40,
                "company_name": "xxxxxxxxxxx"
            },
            "身份证号_2": {
                "name": "xxxxx",
                "id_card_number": "xxxxxxxxxxx",
                "phone_number_1": "xxxxxxxxxxx",
                "phone_number_2": "xxxxxxxxxxx",
                "bank_card_number_1": "xxxxxxxxxxxxxxxxxxxx",
                "bank_card_number_2": "xxxxxxxxxxxxxxxxxxxx",
                "bank_card_number_3": "xxxxxxxxxxxxxxxxxxxx",
                "bank_name_1": "中国建设银行",
                "bank_name_2": "中国工商银行",
                "bank_name_3": "中国工商银行",
                "salary_total": 8000.40,
                "nb_total": 4000.00,
                "lq_total": 4000.40,
                "company_name": "xxxxxxx",
                "beifujin_account": "xxxxxxxxxx" or "xxxxxxxxxxxx"
            }
            ....
        }
    :return:
    """
    res_dict = dict()
    salary_bank_card_id_list = list()
    for row in data:
        salary_bank_card_id_list.append(row.ka_hao)
        id_card_number = row.shen_fen_zheng

        if id_card_number in res_dict.keys():

            old_data = res_dict[id_card_number]
            bank_card_number_1 = old_data.get("bank_card_number_1", "")
            bank_card_number_2 = old_data.get("bank_card_number_2", "")

            if old_data["phone_number_1"] != row.shou_ji_hao:
                res_dict[id_card_number]["phone_number_2"] = row.shou_ji_hao

            if bank_card_number_1 and bank_card_number_1 != row.ka_hao and not res_dict[id_card_number].get("bank_card_number_2"):
                """ 卡1存在，并且当前卡号不等于卡1，且卡2不存在的时候，更新卡2 """
                res_dict[id_card_number]["bank_card_number_2"] = row.ka_hao

            elif bank_card_number_1 and bank_card_number_2 and row.ka_hao != bank_card_number_1 and row.ka_hao != bank_card_number_2 and not res_dict[id_card_number].get("bank_card_number_3"):
                """ 卡1存在，卡2存在, 且卡号不等于卡1， 卡2，且卡3不存在的时候, 更新卡3"""

                res_dict[id_card_number]["bank_card_number_3"] = row.ka_hao

            else:
                pass

            res_dict[id_card_number]["salary_total"] = old_data["salary_total"] + row.jin_e

        else:
            if row.bei_fu_jing_zhang_hu == "xxxxxxxxxxx"
                beifujin_account = "xxxxxxxxxxxxx"

            elif row.bei_fu_jing_zhang_hu == "xxxxxxxxxx":
                beifujin_account = "xxxxxxxxxxxxx"
            else:
                beifujin_account = "xxxxxxxxxxxx"

            res_dict[id_card_number] = {
                "name": row.xing_ming,
                "id_card_number": id_card_number,
                "phone_number_1": row.shou_ji_hao,
                "phone_number_2": "",
                "bank_card_number_1": row.ka_hao,
                "bank_card_number_2": "",
                "bank_card_number_3": "",
                "bank_name_1": "",
                "bank_name_2": "",
                "bank_name_3": "",
                "salary_total": row.jin_e,
                "nb_total": 0.0,
                "lq_total": 0.0,
                "company_name": row.gong_si_ming,
                "beifujin_account": beifujin_account
            }

    salary_bank_card_id_set = set(salary_bank_card_id_list)
    return res_dict, salary_bank_card_id_set


def assemble_ningbo_data(data):
    """ 组装xxx备付金表的数据

    :param data:
        {
            "银行卡号1": {
                "name": "xxxxx",
                "nb_beifujin_total": 100.0,
                "bank_name": "中国建设银行",
            },
            "银行卡号2": {
                "name": "xxxx",
                "nb_beifujin_total": 100.0,
                "bank_name": "中国建设银行",
            },
        }
    :return:
    """

    res_dict = dict()
    for row in data:
        bank_card_number = row.ka_hao
        if bank_card_number in res_dict.keys():
            old_data = res_dict[bank_card_number]

            res_dict[bank_card_number]["nb_beifujin_total"] = row.zhi_chu + old_data["nb_beifujin_total"]
        else:
            res_dict[bank_card_number] = {
                "name": row.xing_ming,
                "nb_beifujin_total": row.zhi_chu,
                "bank_name": row.kai_hu_hang
            }

    return res_dict


def assemble_linquan_data(data):
    """ 组装xxxxx备付金表的数据

    :param data:
        {
            "银行卡号1": {
                "name": "xxxxxx",
                "lq_beifujin_total": 100.0,
                "bank_name": "中国建设银行",
            },
            "银行卡号2": {
                "name": "xxxxx",
                "lq_beifujin_total": 100.0,
                "bank_name": "中国建设银行",
            },
        }
    :return:
    """

    res_dict = dict()
    for row in data:
        bank_card_number = row.ka_hao
        if bank_card_number in res_dict.keys():
            old_data = res_dict[bank_card_number]
            res_dict[bank_card_number]["lq_beifujin_total"] = row.zhi_chu + old_data["lq_beifujin_total"]
            if row.xing_ming != old_data.get('name'):
                res_dict[bank_card_number]["name_1"] = row.xing_ming
        else:
            res_dict[bank_card_number] = {
                "name": row.xing_ming,
                "name_1": "",
                "lq_beifujin_total": row.zhi_chu,
                "bank_name": row.kai_hu_hang
            }

    return res_dict


def assemble_data(salary, ningbo, linquan):
    """ 组装所有表的数据，为输出到excel做准备

    :param salary:
    :param ningbo:
    :param linquan:
    :return:
    [
        {
            "name": ,
            "id_card_number": ,
            "phone_number_1": ,
            "phone_number_2": ,
            "bank_card_number_1": ,
            "bank_card_number_2": ,
            "bank_name_1": ,
            "bank_name_2": ,
            "salary_total": ,
            "beifujin_account": ,
            "nb_beifujin_total": ,
            "lq_beifujin_total": ,
            "company_name":
        },
        {
            "name": ,
            "id_card_number": ,
            "phone_number_1": ,
            "phone_number_2": ,
            "bank_card_number_1": ,
            "bank_card_number_2": ,
            "bank_name_1": ,
            "bank_name_2": ,
            "salary_total": ,
            "beifujin_account": ,
            "nb_beifujin_total": ,
            "lq_beifujin_total": ,
            "company_name":
        },
    ]
    """
    res_data = list()
    bank_only_in_salary_data = dict()
    bank_only_in_ningbo_and_linquan_data = dict()
    salary_all_bank_ids_data = dict()

    for id_c_num, s_salary_data in salary.items():
        item = dict()
        item["name"] = s_salary_data["name"]
        item["id_card_number"] = id_c_num
        item["phone_number_1"] = s_salary_data["phone_number_1"]
        item["phone_number_2"] = s_salary_data["phone_number_2"]
        item["salary_total"] = s_salary_data["salary_total"]
        item["company_name"] = s_salary_data["company_name"]
        item["beifujin_account"] = s_salary_data["beifujin_account"]

        bank_card_number_1 = s_salary_data["bank_card_number_1"]
        bank_card_number_2 = s_salary_data["bank_card_number_2"]
        bank_card_number_3 = s_salary_data["bank_card_number_3"]

        if bank_card_number_1:

            item["bank_card_number_1"] = bank_card_number_1

            if bank_card_number_1 in ningbo.keys():
                item["bank_name_1"] = ningbo[bank_card_number_1]["bank_name"]
                item["bank_card_number_1_money"] = item.get("bank_card_number_1_money", Decimal(0.0)) + ningbo[bank_card_number_1]["nb_beifujin_total"]
                item["nb_beifujin_total"] = item.get("nb_beifujin_total", Decimal(0.0)) + ningbo[bank_card_number_1]["nb_beifujin_total"]

            if bank_card_number_1 in linquan.keys():
                item["bank_name_1"] = linquan[bank_card_number_1]["bank_name"]
                item["bank_card_number_1_money"] = item.get("bank_card_number_1_money", Decimal(0.0)) + linquan[bank_card_number_1]["lq_beifujin_total"]
                item["lq_beifujin_total"] = item.get("lq_beifujin_total", Decimal(0.0)) + linquan[bank_card_number_1]["lq_beifujin_total"]

            if bank_card_number_1 not in ningbo.keys() and bank_card_number_1 not in linquan.keys():
                bank_only_in_salary_data[bank_card_number_1] = {
                    "name": item.get("name"),
                    "money": item.get("salary_total"),
                    "bank_name": "",
                    "beifujin": item.get("beifujin_account")
                }

            salary_all_bank_ids_data[bank_card_number_1] = item

        if bank_card_number_2:
            item["bank_card_number_2"] = bank_card_number_2
            if bank_card_number_2 in ningbo.keys():
                item["bank_name_2"] = ningbo[bank_card_number_2]["bank_name"]
                item["bank_card_number_2_money"] = item.get("bank_card_number_2_money", Decimal(0.0)) + ningbo[bank_card_number_2]["nb_beifujin_total"]
                item["nb_beifujin_total"] = item.get("nb_beifujin_total", Decimal(0.0)) + ningbo[bank_card_number_2]["nb_beifujin_total"]

            if bank_card_number_2 in linquan.keys():
                item["bank_name_2"] = linquan[bank_card_number_2]["bank_name"]
                item["bank_card_number_2_money"] = item.get("bank_card_number_2_money", Decimal(0.0)) + linquan[bank_card_number_2]["lq_beifujin_total"]
                item["lq_beifujin_total"] = item.get("lq_beifujin_total", Decimal(0.0)) + linquan[bank_card_number_2]["lq_beifujin_total"]

            if bank_card_number_2 not in ningbo.keys() and bank_card_number_2 not in linquan.keys():
                bank_only_in_salary_data[bank_card_number_2] = {
                    "name": item.get("name"),
                    "money": item.get("salary_total"),
                    "bank_name": "",
                    "beifujin": item.get("beifujin_account")
                }

            salary_all_bank_ids_data[bank_card_number_2] = item

        if bank_card_number_3:
            item["bank_card_number_3"] = bank_card_number_3

            if bank_card_number_3 in ningbo.keys():
                item["bank_name_3"] = ningbo[bank_card_number_3]["bank_name"]
                item["bank_card_number_3_money"] = item.get("bank_card_number_3_money", Decimal(0.0)) + ningbo[bank_card_number_3]["nb_beifujin_total"]
                item["nb_beifujin_total"] = item.get("nb_beifujin_total", Decimal(0.0)) + ningbo[bank_card_number_3]["nb_beifujin_total"]

            if bank_card_number_3 in linquan.keys():
                item["bank_name_3"] = linquan[bank_card_number_3]["bank_name"]
                item["bank_card_number_3_money"] = item.get("bank_card_number_3_money", Decimal(0.0)) + linquan[bank_card_number_3]["lq_beifujin_total"]
                item["lq_beifujin_total"] = item.get("lq_beifujin_total", Decimal(0.0)) + linquan[bank_card_number_3]["lq_beifujin_total"]

            if bank_card_number_3 not in ningbo.keys() and bank_card_number_3 not in linquan.keys():
                bank_only_in_salary_data[bank_card_number_3] = {
                    "name": item.get("name"),
                    "money": item.get("salary_total"),
                    "bank_name": "",
                    "beifujin": item.get("beifujin_account")
                }

            salary_all_bank_ids_data[bank_card_number_3] = item

        res_data.append(item)

    # print("bank_only_in_salary: ", bank_only_in_salary_data)
    # print("salary_all_bank_card_id: ", salary_all_bank_ids_data)

    ningbo_ids = set(ningbo.keys())
    linquan_ids = set(linquan.keys())
    ningbo_linquan = ningbo_ids | linquan_ids

    for _id in ningbo_linquan:

        if _id and _id not in salary_all_bank_ids_data.keys():

            if _id in ningbo.keys() and _id in linquan.keys():
                bank_only_in_ningbo_and_linquan_data[_id] = {
                    "name": ningbo[_id]['name'],
                    "money": ningbo[_id]["nb_beifujin_total"] + linquan[_id]["lq_beifujin_total"],
                    "bank_name": ningbo[_id]['bank_name'],
                    "beifujin": "在xxx备付金，xxxx备付金都出现了这个卡号，但是在工资中没有出现"
                }

            elif _id in linquan.keys():
                bank_only_in_ningbo_and_linquan_data[_id] = {
                    "name": linquan[_id]["name"],
                    "money": linquan[_id]["lq_beifujin_total"],
                    "bank_name": linquan[_id]['bank_name'],
                    "beifujin": "xxxxxxxxxxxxxx"
                }

            else:
                bank_only_in_ningbo_and_linquan_data[_id] = {
                    "name": ningbo[_id]["name"],
                    "money": ningbo[_id]["nb_beifujin_total"],
                    "bank_name": ningbo[_id]['bank_name'],
                    "beifujin": "xxxxxxxx"
                }

    return res_data, bank_only_in_salary_data, bank_only_in_ningbo_and_linquan_data


def insert_data(data):
    """ 将统计后的数据插入数据库->暂未使用此function

    Column("name", String(64), nullable=False),  # 姓名
    Column("id_card_number", String(20), nullable=False, unique=True),  # 身份证号码
    Column("phone_number_1", String(16), nullable=False, unique=True),  # 手机号码
    Column("phone_number_2", String(16), nullable=False, unique=True),  # 手机号码
    Column("bank_card_number_1", String(24), nullable=False, unique=True),  # 银行卡号码
    Column("bank_card_number_2", String(24), nullable=True, unique=True),  # 银行卡号码
    Column("bank_name_1", String(64), nullable=False),  # 开户行1
    Column("bank_name_2", String(64), nullable=True),  # 开户行1
    Column("salary_total", DOUBLE, nullable=False),  # 工资信息表里的所发工资总额
    Column("nb_beifujin_total", DOUBLE, default=0.0),  # xxx_备付金总额
    Column("lq_beifujin_total", DOUBLE, default=0.0),  # xxxxxxxx备付金总额
    Column("beifujin_account", String(36), nullable=False),  # salary表标注的从哪个表转出去的
    Column("company_name", String(64)),  # 公司名字

    :param data:
    :return:

    """
    pprint(data)

    print("\n\n\n")
    pprint(len(data))
    return data


def save_7775_xls_file(tongji_data, only_in_salary, only_in_beifujin):
    """ 保存数据，输出到Excel表格.
    Column("name", String(64), nullable=False),  # 姓名
    Column("id_card_number", String(20), nullable=False, unique=True),  # 身份证号码
    Column("phone_number_1", String(16), nullable=False, unique=True),  # 手机号码
    Column("phone_number_2", String(16), nullable=False, unique=True),  # 手机号码
    Column("bank_card_number_1", String(24), nullable=False, unique=True),  # 银行卡号码
    Column("bank_card_number_2", String(24), nullable=True, unique=True),  # 银行卡号码
    Column("bank_name_1", String(64), nullable=False),  # 开户行1
    Column("bank_name_2", String(64), nullable=True),  # 开户行1
    Column("salary_total", DOUBLE, nullable=False),  # 工资信息表里的所发工资总额
    Column("nb_beifujin_total", DOUBLE, default=0.0),  # xxx_备付金总额
    Column("lq_beifujin_total", DOUBLE, default=0.0),  # xxxxxxxx备付金总额
    Column("beifujin_account", String(36), nullable=False),  # salary表标注的从哪个表转出去的
    Column("company_name", String(64)),  # 公司名字
    :return:
    """
    data = OrderedDict()
    # sheet表的数据
    zong_biao = []
    sheet_xiang_jia_bu_deng_biao = []
    lai_zi_liang_ge_bei_fu_jin_biao = []
    only_in_salary_biao = []
    only_in_beifujin_biao = []

    res_data = []
    row_1_data = ["姓名", "身份证号码",
                  "电话号码_1", "电话号码_2",
                  "银行卡_1", "银行卡1_名称", "银行卡1_金额",
                  "银行卡_2", "银行卡2_名称", "银行卡2_金额",
                  "银行卡_3", "银行卡3_名称", "银行卡3_金额",
                  "工资信息表_总金额",
                  "工资信息表_备付金账户",
                  "xxxxxx备付金_统计",
                  "xxxxxxxx备付金_统计",
                  "是否异常",
                  "公司名称",
                  ]  # 每一行的数据
    # print(row_1_data, len(row_1_data))
    row_1_data_1 = [
        "姓名",
        "银行卡号",
        "金额",
        "备付金账户",
        "备注"
    ]

    zong_biao.append(row_1_data)  # 总表
    sheet_xiang_jia_bu_deng_biao.append(row_1_data)  # 两个备付金相加，不等于工资表
    lai_zi_liang_ge_bei_fu_jin_biao.append(row_1_data)  # 两个备付金都有支出的
    only_in_salary_biao.append(row_1_data_1)
    only_in_beifujin_biao.append(row_1_data_1)

    tmp_nb = 0
    tmp_lq = 0
    tmp_salary = 0

    for item in tongji_data:
        salary_total = float(format(item.get("salary_total", 0.0), "0.2f"))
        nb_total = float(format(item.get("nb_beifujin_total", 0.0), "0.2f"))
        lq_total = float(format(item.get("lq_beifujin_total", 0.0), "0.2f"))

        tmp_nb += nb_total
        tmp_lq += lq_total
        tmp_salary += salary_total

        try:
            if item.get("bank_card_number_1") and item.get("bank_card_number_1_money", ""):
                card_1_number, card_1_name, card_1_money = item.get("bank_card_number_1", ""), item.get("bank_name_1", ""), float(format(item.get("bank_card_number_1_money", 0.0), "0.2f"))
            else:
                card_1_number, card_1_name, card_1_money = "", "", 0.0

            if item.get("bank_card_number_2") and item.get("bank_card_number_2_money", ""):
                card_2_number, card_2_name, card_2_money = item.get("bank_card_number_2", ""), item.get("bank_name_2", ""), float(format(item.get("bank_card_number_2_money", 0.0), "0.2f"))
            else:
                card_2_number, card_2_name, card_2_money = "", "", 0.0

            if item.get("bank_card_number_3") and item.get("bank_card_number_3_money", ""):
                card_3_number, card_3_name, card_3_money = item.get("bank_card_number_3", ""), item.get("bank_name_3", ""), float(format(item.get("bank_card_number_3_money", 0.0), "0.2f"))
            else:
                card_3_number, card_3_name, card_3_money = "", "", 0.0

        except Exception as e:
            print(item)
            sys.exit()

        row_2_data = [
            item.get("name", ""), item.get("id_card_number"),
            item.get("phone_number_1", ""), item.get("phone_number_2"),
            card_1_number if item.get("bank_card_number_1", "") else "", card_1_name if item.get("bank_card_number_1", "") else "", card_1_money if item.get("bank_card_number_1", "") else 0.0,
            card_2_number if item.get("bank_card_number_2", "") else "", card_2_name if item.get("bank_card_number_2", "") else "", card_2_money if item.get("bank_card_number_2", "") else 0.0,
            card_3_number if item.get("bank_card_number_3", "") else "", card_3_name if item.get("bank_card_number_3", "") else "", card_3_money if item.get("bank_card_number_3", "") else 0.0,
            salary_total,
            item.get("beifujin_account", ""),
            nb_total,
            lq_total,
            "是" if nb_total + lq_total != salary_total else "",
            item.get("company_name", "")
        ]
        # print(item.get("name", ""), len(row_2_data))

        # 逐条添加数据
        res_data.append(row_2_data)

        # 总表
        zong_biao.append(row_2_data)

        # 相加不等表
        if nb_total + lq_total != salary_total:
            sheet_xiang_jia_bu_deng_biao.append(row_2_data)

        # 来自两个备付金表
        if nb_total and lq_total:
            lai_zi_liang_ge_bei_fu_jin_biao.append(row_2_data)

    # only in salary 表
    only_in_salary_total_money = 0.0
    only_in_beifujin_total_money = 0.0
    for k, item in only_in_salary.items():
        """
        "姓名",
        "银行卡号",
        "金额",
        "备付金账户",
        "备注"
        """
        cnt_money = float(format(item.get("money", 0.0), "0.2f"))
        row_2_data = [
            item.get("name", ""),
            k,
            cnt_money,
            item.get("beifujin", ""),
            "仅在工资表中存在此记录"
        ]
        only_in_salary_biao.append(row_2_data)
        only_in_salary_total_money += cnt_money

    for k, item in only_in_beifujin.items():
        """
        "姓名",
        "银行卡号",
        "金额",
        "备付金账户",
        "备注"
        """
        cnt_money = float(format(item.get("money", 0.0), "0.2f"))
        row_2_data = [
            item.get("name", ""),
            k,
            cnt_money,
            item.get("beifujin", ""),
            "仅在备付金表中存在此记录"
        ]
        only_in_beifujin_biao.append(row_2_data)
        only_in_beifujin_total_money += cnt_money

    # 添加sheet表
    data.update({u"总表": zong_biao})
    data.update({u"相加不等的部分": sheet_xiang_jia_bu_deng_biao})
    data.update({u"两个备付金的表都有支出数据": lai_zi_liang_ge_bei_fu_jin_biao})
    data.update({u"仅在工资表中存在的记录": only_in_salary_biao})
    data.update({u"仅在备付金表存在的记录": only_in_beifujin_biao})

    nb_total = sum([item[15] for item in res_data])
    lq_total = sum([item[16] for item in res_data])
    salary_total = sum([item[13] for item in res_data])
    ningbo_data = []
    linquan_data = []

    for item in res_data:
        if item[15] == "xxxxxx备付金":
            ningbo_data.append(item)
        else:
            linquan_data.append(item)

    print("总表数据: ", len(zong_biao) - 1, "金额: ", salary_total)
    print("总表来自xxx备付金表的", len(ningbo_data), "金额: ", nb_total)
    print("总表来自xxx备付金表的", len(linquan_data), "金额: ", lq_total)
    print("两备付金表相加不等工资表: ", len(sheet_xiang_jia_bu_deng_biao) - 1, "金额: ", "暂无法统计")
    print("两个备付金表都有数据: ", len(lai_zi_liang_ge_bei_fu_jin_biao), "金额: ", "暂无法统计")
    print("仅在备付金表存在的记录: ", len(only_in_beifujin_biao) - 1, "金额:", only_in_beifujin_total_money)
    print("仅在工资表中存在的记录: ", len(only_in_salary_biao) - 1, "金额: ", only_in_salary_total_money)

    # 保存成xls文件
    save_data(result_path, data)


def judge_bank_card_id(salary, ningbo, linquan):
    """ 判断ningbo + linquan中的id是否有没有出现在salary中的

    :param salary:
    :param ningbo:
    :param linquan:
    :return:
    """
    ningbo_linquan = ningbo | linquan
    result_1 = []
    for _id in ningbo_linquan:
        if _id and _id not in salary:
            result_1.append(_id)

    result_2 = []
    for _id in salary:
        if _id and _id not in ningbo_linquan:
            result_2.append(_id)

    return result_1, result_2


if __name__ == "__main__":
    # salary
    salary_data, salary_bank_card_id_set = assemble_salary_data(data=get_salary_info_data())

    # ningbo
    ningbo_beifujin_data = assemble_ningbo_data(data=get_ningbo_beifujin())
    ningbo_bank_card_id_set = set(ningbo_beifujin_data.keys())

    # linquan
    linquan_beifujin_data = assemble_linquan_data(data=get_linquan_beifujin())
    linquan_bank_card_id_set = set(linquan_beifujin_data.keys())

    # assemble
    res_data, bank_only_in_salary_data, bank_only_in_ningbo_and_linquan_data = assemble_data(salary=salary_data, ningbo=ningbo_beifujin_data, linquan=linquan_beifujin_data)

    # data = insert_data(data=res_data)
    save_7775_xls_file(tongji_data=res_data, only_in_salary=bank_only_in_salary_data, only_in_beifujin=bank_only_in_ningbo_and_linquan_data)

    print("工资中出现了多少个不重复的银行卡: ", len(salary_bank_card_id_set))
    print("xxx备付金中出现了多少个不重复的银行卡: ", len(ningbo_bank_card_id_set))
    print("xxxxx备付金中出现了多少个不重复的银行卡: ", len(linquan_bank_card_id_set))
    print("xxx & xxxxx合计出现多少个不重复的银行卡: ", len(linquan_bank_card_id_set | ningbo_bank_card_id_set))

    result_1_ids, result_2_ids = judge_bank_card_id(salary_bank_card_id_set, ningbo_bank_card_id_set, linquan_bank_card_id_set)

    print("\n\n\n")
    print("在xxxxx or xxx中出现了, 但是没有在工资表中出现: ", len(result_1_ids))
    print("\n\n\n")
    print("在工资表中出现了，但是没有在xxxxx or xxx中出现: ", len(result_2_ids))

    print("\n\n\n")
    print("数据保存到: ", result_path, "成功...")

