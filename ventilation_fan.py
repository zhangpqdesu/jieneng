# ————————————通风机能效—————————————— #

import math
from scipy.interpolate import interp1d
from sqlalchemy import create_engine, Column, Integer, Float, String, text, Numeric, or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
import pandas as pd
import numpy as np

# 创建数据库连接引擎
engine = create_engine('mysql+pymysql://Administrator:XWClassroom20202023@www.ylxteach.net:3366/demo?charset=gbk',
                       echo=True)

# 创建基类
Base = declarative_base()


# 计算压力系数
def PCoefficient(Pf, p1, u):
    kp = 1  # 暂时定为1，需要甲方给出。后续可以改为输入形式
    PCoefficient_value = Pf * kp / (p1 * (u ** 2))
    return PCoefficient_value


# 计算比转速
def Ns(type, n, q, Pf, p1):
    ns = 0
    kp = 1
    Pf_value = Pf
    if '双吸' in type:
        ns = 5.54 * n * ((q / 2) ** 0.5) / (1.2 * Pf_value * kp / p1) ** 0.75
    else:
        ns = 5.54 * n * (q ** 0.5) / (1.2 * Pf_value * kp / p1) ** 0.75
    return ns


# 计算通风机效率
def Ventilation_fan_efficiency(q, Pf, pr):
    kp = 1
    Pf_value = Pf
    Nr = (q * Pf_value * kp / (1000 * pr)) * 100
    return Nr


# 计算通风机组效率
def Ventilation_unit_efficiency(q, Pf, pe):
    kp = 1
    Pf_value = Pf
    Ne = (q * Pf_value * kp / (1000 * pe)) * 100
    return Ne


# 计算普通电动机直联式（A式传动）通风机效率
def A_efficiency(q, Pf, pe, Nm):
    Ne = Ventilation_unit_efficiency(q, Pf, pe)
    Nr = Ne / Nm
    return Nr


# 删除表
# 创建 MetaData 对象
# metadata = MetaData()

# # 定义表对象
# VTableOne = Table('VTableOne', metadata)
# # 删除表
# VTableOne.drop(engine)
#
# # 定义表对象
# VTableTwo = Table('VTableTwo', metadata)
# # 删除表
# VTableTwo.drop(engine)
#
# # 定义表对象
# VTableThree = Table('VTableThree', metadata)
# # 删除表
# VTableThree.drop(engine)
#
# # 定义表对象
# VTableFour = Table('VTableFour', metadata)
# # 删除表
# VTableFour.drop(engine)


# ————————————表1———————————— #

# 定义模型
class VTableOne(Base):
    __tablename__ = 'VTableOne'
    index = Column(Integer, primary_key=True)
    PCoefficient_left = Column(Numeric(precision=10, scale=2))
    PCoefficient_right = Column(Numeric(precision=10, scale=2))
    Ns_left = Column(Integer)
    Ns_right = Column(Integer)
    MachineNumber_left = Column(Numeric(precision=10, scale=2))
    MachineNumber_right = Column(Numeric(precision=10, scale=2))
    Efficiency = Column(Integer)
    grade = Column(String(10))


# # 创建数据表格
# def create_table():
#     data = [
#         {'PCoefficient_left': 1.35, 'PCoefficient_right': 1.55, 'Ns_left': 45, 'Ns_right': 65,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 2.5, 'Efficiency': 43, 'grade': '3级'},
#         {'PCoefficient_left': 1.35, 'PCoefficient_right': 1.55, 'Ns_left': 45, 'Ns_right': 65,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 2.5, 'Efficiency': 58, 'grade': '2级'},
#         {'PCoefficient_left': 1.35, 'PCoefficient_right': 1.55, 'Ns_left': 45, 'Ns_right': 65,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 2.5, 'Efficiency': 61, 'grade': '1级'},
#         {'PCoefficient_left': 1.05, 'PCoefficient_right': 1.35, 'Ns_left': 35, 'Ns_right': 55,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 2.5, 'Efficiency': 45, 'grade': '3级'},
#         {'PCoefficient_left': 1.05, 'PCoefficient_right': 1.35, 'Ns_left': 35, 'Ns_right': 55,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 2.5, 'Efficiency': 62, 'grade': '2级'},
#         {'PCoefficient_left': 1.05, 'PCoefficient_right': 1.35, 'Ns_left': 35, 'Ns_right': 55,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 2.5, 'Efficiency': 65, 'grade': '1级'},
#         {'PCoefficient_left': 0.95, 'PCoefficient_right': 1.05, 'Ns_left': 10, 'Ns_right': 20,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 2.5, 'Efficiency': 49, 'grade': '3级'},
#     ]
#     df = pd.DataFrame(data)
#     df.to_sql('VTableOne', engine, if_exists='replace', index=True)
#
#
# # 创建数据表格并写入数据库
# create_table()


# ————————————表2———————————— #
# 定义模型
class VTableTwo(Base):
    __tablename__ = 'VTableTwo'
    index = Column(Integer, primary_key=True)
    PCoefficient_left = Column(Numeric(precision=10, scale=2))
    PCoefficient_right = Column(Numeric(precision=10, scale=2))
    Ns_left = Column(Integer)
    Ns_right = Column(Integer)
    MachineNumber_left = Column(Numeric(precision=10, scale=2))
    MachineNumber_right = Column(Numeric(precision=10, scale=2))
    Efficiency = Column(Integer)
    grade = Column(String(10))


# # 创建数据表格
# def create_table():
#     data = [
#         {'PCoefficient_left': 0.85, 'PCoefficient_right': 0.95, 'Ns_left': 5, 'Ns_right': 15,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 5.0, 'Efficiency': 62, 'grade': '3级'},
#         {'PCoefficient_left': 0.85, 'PCoefficient_right': 0.95, 'Ns_left': 5, 'Ns_right': 15,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 5.0, 'Efficiency': 72, 'grade': '2级'},
#         {'PCoefficient_left': 0.85, 'PCoefficient_right': 0.95, 'Ns_left': 5, 'Ns_right': 15,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 5.0, 'Efficiency': 75, 'grade': '1级'},
#
#         {'PCoefficient_left': 0.85, 'PCoefficient_right': 0.95, 'Ns_left': 15, 'Ns_right': 30,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 5.0, 'Efficiency': 65, 'grade': '3级'},
#         {'PCoefficient_left': 0.85, 'PCoefficient_right': 0.95, 'Ns_left': 15, 'Ns_right': 30,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 5.0, 'Efficiency': 74, 'grade': '2级'},
#         {'PCoefficient_left': 0.85, 'PCoefficient_right': 0.95, 'Ns_left': 15, 'Ns_right': 30,
#          'MachineNumber_left': 2.0, 'MachineNumber_right': 5.0, 'Efficiency': 77, 'grade': '1级'},
#     ]
#     df = pd.DataFrame(data)
#     df.to_sql('VTableTwo', engine, if_exists='replace', index=True)
#
#
# # 创建数据表格并写入数据库
# create_table()

# ————————————表3———————————— #
# 定义模型
class VTableThree(Base):
    __tablename__ = 'VTableThree'
    index = Column(Integer, primary_key=True)
    r_left = Column(Numeric(precision=10, scale=2))  # 轮毂比左边界
    r_right = Column(Numeric(precision=10, scale=2))  # 轮毂比右边界
    MachineNumber_left = Column(Numeric(precision=10, scale=2))  # 机号左边界
    MachineNumber_right = Column(Numeric(precision=10, scale=2))  # 机号右边界
    Efficiency = Column(Integer)
    grade = Column(String(10))


# # 创建数据表格
# def create_table():
#     data = [
#         {'r_left': 0.0, 'r_right': 0.3, 'MachineNumber_left': 2.5, 'MachineNumber_right': 5.0,
#          'Efficiency': 55, 'grade': '3级'},
#         {'r_left': 0.0, 'r_right': 0.3, 'MachineNumber_left': 2.5, 'MachineNumber_right': 5.0,
#          'Efficiency': 66, 'grade': '2级'},
#         {'r_left': 0.0, 'r_right': 0.3, 'MachineNumber_left': 2.5, 'MachineNumber_right': 5.0,
#          'Efficiency': 69, 'grade': '1级'},
#
#         {'r_left': 0.3, 'r_right': 0.4, 'MachineNumber_left': 2.5, 'MachineNumber_right': 5.0,
#          'Efficiency': 59, 'grade': '3级'},
#         {'r_left': 0.0, 'r_right': 0.3, 'MachineNumber_left': 2.5, 'MachineNumber_right': 5.0,
#          'Efficiency': 68, 'grade': '2级'},
#         {'r_left': 0.0, 'r_right': 0.3, 'MachineNumber_left': 2.5, 'MachineNumber_right': 5.0,
#          'Efficiency': 71, 'grade': '1级'},
#     ]
#     df = pd.DataFrame(data)
#     df.to_sql('VTableThree', engine, if_exists='replace', index=True)
#
#
# # 创建数据表格并写入数据库
# create_table()

# ————————————表4———————————— #
# 定义模型
class VTableFour(Base):
    __tablename__ = 'VTableFour'
    index = Column(Integer, primary_key=True)
    PCoefficient_left = Column(Numeric(precision=10, scale=2))
    PCoefficient_right = Column(Numeric(precision=10, scale=2))
    Ns_left = Column(Integer)
    Ns_right = Column(Integer)
    MachineNumber_left = Column(Numeric(precision=10, scale=2))
    MachineNumber_right = Column(Numeric(precision=10, scale=2))
    Efficiency = Column(Integer)
    grade = Column(String(10))


# # 创建数据表格
# def create_table():
#     data = [
#         {'PCoefficient_left': 1.0, 'PCoefficient_right': 1.1, 'Ns_left': 50, 'Ns_right': 99999,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 36, 'grade': '3级'},
#         {'PCoefficient_left': 1.0, 'PCoefficient_right': 1.1, 'Ns_left': 50, 'Ns_right': 99999,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 43, 'grade': '2级'},
#         {'PCoefficient_left': 1.0, 'PCoefficient_right': 1.1, 'Ns_left': 50, 'Ns_right': 99999,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 46, 'grade': '1级'},
#
#         {'PCoefficient_left': 1.0, 'PCoefficient_right': 1.1, 'Ns_left': 30, 'Ns_right': 50,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 35, 'grade': '3级'},
#         {'PCoefficient_left': 1.0, 'PCoefficient_right': 1.1, 'Ns_left': 30, 'Ns_right': 50,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 42, 'grade': '2级'},
#         {'PCoefficient_left': 1.0, 'PCoefficient_right': 1.1, 'Ns_left': 30, 'Ns_right': 50,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 45, 'grade': '1级'},
#
#         {'PCoefficient_left': 1.1, 'PCoefficient_right': 1.2, 'Ns_left': 50, 'Ns_right': 99999,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 35, 'grade': '3级'},
#         {'PCoefficient_left': 1.1, 'PCoefficient_right': 1.2, 'Ns_left': 50, 'Ns_right': 99999,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 43, 'grade': '2级'},
#         {'PCoefficient_left': 1.1, 'PCoefficient_right': 1.2, 'Ns_left': 50, 'Ns_right': 99999,
#          'MachineNumber_left': 0, 'MachineNumber_right': 2, 'Efficiency': 46, 'grade': '1级'},
#     ]
#     df = pd.DataFrame(data)
#     df.to_sql('VTableFour', engine, if_exists='replace', index=True)
#
#
# # 创建数据表格并写入数据库
# create_table()

# ————————————查表1———————————— #
def query_efficiency_one(session, Input_data):
    found_match = False  # 设置一个标志来记录是否找到匹配记录

    for data in Input_data:
        print("正在执行查询，条件为：", data)

        # 查询第一个表
        query_pump1 = session.query(VTableOne).filter(
            getattr(VTableOne, 'MachineNumber_left') <= data['MachineNumber'],
            getattr(VTableOne, 'MachineNumber_right') >= data['MachineNumber'],
            getattr(VTableOne, 'PCoefficient_left') <= data['PCoefficiency'],
            getattr(VTableOne, 'PCoefficient_right') >= data['PCoefficiency'],
            getattr(VTableOne, 'Ns_left') <= data['ns'],
            getattr(VTableOne, 'Ns_right') >= data['ns'],
            VTableOne.grade == data['grade']
        ).first()

        if query_pump1:
            return query_pump1.Efficiency
        else:
            print("未找到匹配的记录")

    if not found_match:
        print("没有找到任何匹配的记录")
        return None


# ————————————查表2———————————— #
def query_efficiency_two(session, Input_data):
    found_match = False  # 设置一个标志来记录是否找到匹配记录

    for data in Input_data:
        print("正在执行查询，条件为：", data)

        query_result = session.query(VTableTwo).filter(
            getattr(VTableTwo, 'MachineNumber_left') <= data['MachineNumber'],
            getattr(VTableTwo, 'MachineNumber_right') >= data['MachineNumber'],
            getattr(VTableTwo, 'PCoefficient_left') <= data['PCoefficiency'],
            getattr(VTableTwo, 'PCoefficient_right') >= data['PCoefficiency'],
            getattr(VTableTwo, 'Ns_left') <= data['ns'],
            getattr(VTableTwo, 'Ns_right') >= data['ns'],
            VTableTwo.grade == data['grade']
        ).first()

        if query_result:
            return query_result.Efficiency
        else:
            print("未找到匹配的记录")

    if not found_match:
        print("没有找到任何匹配的记录")
        return None


# ————————————查表3———————————— #
def query_efficiency_three(session, Input_data):
    found_match = False  # 设置一个标志来记录是否找到匹配记录

    for data in Input_data:
        print("正在执行查询，条件为：", data)

        # 查询第三个表
        query_result = session.query(VTableThree).filter(
            getattr(VTableThree, 'MachineNumber_left') <= data['MachineNumber'],
            getattr(VTableThree, 'MachineNumber_right') >= data['MachineNumber'],
            getattr(VTableThree, 'r_left') <= data['r'],
            getattr(VTableThree, 'r_right') >= data['r'],
            VTableThree.grade == data['grade']
        ).first()

        if query_result:
            return query_result.Efficiency
        else:
            print("未找到匹配的记录")

    if not found_match:
        print("没有找到任何匹配的记录")
        return None


# ————————————查表4———————————— #
def query_efficiency_four(session, Input_data):
    found_match = False  # 设置一个标志来记录是否找到匹配记录

    for data in Input_data:
        print("正在执行查询，条件为：", data)

        # 查询第四个表
        query_result = session.query(VTableFour).filter(
            getattr(VTableFour, 'MachineNumber_left') <= data['MachineNumber'],
            getattr(VTableFour, 'MachineNumber_right') >= data['MachineNumber'],
            getattr(VTableFour, 'PCoefficient_left') <= data['PCoefficiency'],
            getattr(VTableFour, 'PCoefficient_right') >= data['PCoefficiency'],
            getattr(VTableFour, 'Ns_left') <= data['ns'],
            getattr(VTableFour, 'Ns_right') >= data['ns'],
            VTableFour.grade == data['grade']
        ).first()

        if query_result:
            return query_result.Efficiency
        else:
            print("未找到匹配的记录")

    if not found_match:
        print("没有找到任何匹配的记录")
        return None


# ————————————设置能效等级———————————— #
def set_grade(input_data_list, grade_value):
    for data in input_data_list:
        data['grade'] = grade_value


# ————————————1级参考效率值———————————— #
def grade_one(Pf, p1, u, session, Input_data, type):
    set_grade(Input_data, '1级')
    Efficiency = 0
    PCoefficient_value = PCoefficient(Pf, p1, u)
    if '离心' in type:
        if '双吸入式' in type or '暖通空调用' in type:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data) - 1
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data) - 1
        elif '进气箱' in type:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data) - 4
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data) - 4
        elif '外转子' in type:
            Efficiency = query_efficiency_four(session, Input_data)
        else:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data)
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data)
    elif '轴流' in type:
        if '进气箱' in type:
            Efficiency = query_efficiency_three(session, Input_data) - 3
        elif '无扩散筒' in type:
            Efficiency = query_efficiency_three(session, Input_data) + 2
        elif '动叶可调' in type and '无进气箱' in type and '无扩散筒' in type:
            Efficiency = 89.5
        elif '可逆转' in type:
            Efficiency = query_efficiency_three(session, Input_data) - 8
        else:
            Efficiency = query_efficiency_three(session, Input_data)
    return Efficiency


# ————————————2级参考效率值———————————— #
def grade_two(Pf, p1, u, session, Input_data, type):
    set_grade(Input_data, '2级')
    Efficiency = 0
    PCoefficient_value = PCoefficient(Pf, p1, u)
    if '离心' in type:
        if '双吸入式' in type or '暖通空调用' in type:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data) - 1
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data) - 1
        elif '进气箱' in type:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data) - 4
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data) - 4
        elif '外转子' in type:
            Efficiency = query_efficiency_four(session, Input_data)
        else:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data)
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data)
    elif '轴流' in type:
        if '进气箱' in type:
            Efficiency = query_efficiency_three(session, Input_data) - 3
        elif '无扩散筒' in type:
            Efficiency = query_efficiency_three(session, Input_data) + 2
        elif '动叶可调' in type and '无进气箱' in type and '无扩散筒' in type:
            Efficiency = 87
        elif '可逆转' in type:
            Efficiency = query_efficiency_three(session, Input_data) - 8
        else:
            Efficiency = query_efficiency_three(session, Input_data)
    return Efficiency


# ————————————3级参考效率值———————————— #
def grade_three(Pf, p1, u, session, Input_data, type):
    set_grade(Input_data, '3级')
    Efficiency = 0
    PCoefficient_value = PCoefficient(Pf, p1, u)
    if '离心' in type:
        if '双吸入式' in type or '暖通空调用' in type:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data) - 3
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data) - 3
        elif '进气箱' in type:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data) - 4
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data) - 4
        elif '外转子' in type:
            Efficiency = query_efficiency_four(session, Input_data)
        else:
            if 0.95 <= PCoefficient_value < 1.55:
                Efficiency = query_efficiency_one(session, Input_data)
            elif 0.25 <= PCoefficient_value < 0.95:
                Efficiency = query_efficiency_two(session, Input_data)
    elif '轴流' in type:
        if '进气箱' in type:
            Efficiency = query_efficiency_three(session, Input_data) - 3
        elif '无扩散筒' in type:
            Efficiency = query_efficiency_three(session, Input_data) + 2
        elif '动叶可调' in type and '无进气箱' in type and '无扩散筒' in type:
            Efficiency = 82
        elif '可逆转' in type:
            Efficiency = query_efficiency_three(session, Input_data) - 8
        else:
            Efficiency = query_efficiency_three(session, Input_data)
    return Efficiency


# ————————————计算实际效率———————————— #
def real_grade(type, q, Pf, pe, Nm, pr):
    kp = 1
    if '通风机组' in type:
        real_efficiency = Ventilation_unit_efficiency(q, Pf, pe)
    elif '直联式' in type:
        real_efficiency = A_efficiency(q, Pf, pe, Nm)
    else:
        real_efficiency = Ventilation_fan_efficiency(q, Pf, pr)
    return real_efficiency


def get_input_data(MachineNumber, r, type, Pf, p1, u, n, q, pr, pe, Nm):

    grade = 0

    kp = 1

    ns = Ns(type, n, q, Pf, p1)
    PCoefficiency = PCoefficient(Pf, p1, u)

    return {'MachineNumber': MachineNumber, 'grade': grade, 'r': r, 'type': type,
            'Pf': Pf, 'p1': p1, 'u': u, 'n': n, 'q': q, 'pr': pr, 'pe': pe, 'Nm': Nm, 'ns': ns,
            'PCoefficiency': PCoefficiency}


# ————————————比较———————————— #
def finally_result(MachineNumber, r, type, Pf, p1, u, n, q, pr, pe, Nm):
    # 初始化示例数据数组
    Input_data = []

    # 循环获取用户输入，并将数据添加到示例数据数组中
    while True:
        data = get_input_data(MachineNumber, r, type, Pf, p1, u, n, q, pr, pe, Nm)
        Input_data.append(data)

        break

    Session = sessionmaker(bind=engine)
    session = Session()

    type = Input_data[0]['type']
    q = Input_data[0]['q']
    Pf = Input_data[0]['Pf']
    pe = Input_data[0]['pe']
    Nm = Input_data[0]['Nm']
    pr = Input_data[0]['pr']
    p1 = Input_data[0]['p1']
    u = Input_data[0]['u']

    real_efficiency = real_grade(type, q, Pf, pe, Nm, pr)  # 计算出的实际效率值
    print("real", real_efficiency)
    A = grade_one(Pf, p1, u, session, Input_data, type)
    print("hh", A)
    if real_efficiency >= grade_one(Pf, p1, u, session, Input_data, type):
        return '1级'
    elif grade_two(Pf, p1, u, session, Input_data, type) <= real_efficiency < grade_one(Pf, p1, u, session,
                                                                                        Input_data, type):
        return '2级'
    elif grade_three(Pf, p1, u, session, Input_data, type) <= real_efficiency < grade_two(Pf, p1, u, session,
                                                                                          Input_data, type):
        return '3级'
    else:
        return '低于3级'

