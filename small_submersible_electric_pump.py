# ————————————小型潜水电泵-建表———————————— #

import math
from scipy.interpolate import interp1d
from sqlalchemy import create_engine, Column, Integer, Float, String, text, Numeric, or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table

# ————————————单级泵参数 表1———————————— #

# 创建数据库连接引擎
engine = create_engine('mysql+pymysql://Administrator:XWClassroom20202023@www.ylxteach.net:3366/demo?charset=gbk',
                       echo=True)

# 创建基类
Base = declarative_base()


# # 删除表
# # # 创建 MetaData 对象
# # metadata = MetaData()
# # # 定义表对象
# # SSSinglestage_table = Table('SSSingleStage_TableOne', metadata)
# # # 删除表
# # SSSinglestage_table.drop(engine)
#
# 定义 Pump 模型
class Pump(Base):
    __tablename__ = 'SSSingleStage_TableOne'  # 小型潜水电泵的单级泵参数-表1
    id = Column(Integer, primary_key=True)
    rotation_speed = Column(Float, nullable=False)  # 转速
    flow_rate = Column(Float, nullable=False)  # 流量
    head = Column(Float, nullable=False)  # 扬程
    power = Column(Float, nullable=False)  # 功率
    pump_type = Column(String(50), nullable=False)  # 类型
    efficiency = Column(Numeric(precision=10, scale=2), nullable=False)  # 电泵效率


#
#
# # 创建数据表
# Base.metadata.create_all(engine)
#
# # 创建一个会话类
# Session = sessionmaker(bind=engine)
# # 创建一个会话对象
# session = Session()
#
# # 添加数据
# data = [
#     {'rotation_speed': 3000, 'flow_rate': 1.5, 'head': 7, 'power': 0.12, 'pump_type': 'QDX', 'efficiency': 13.9},
#     {'rotation_speed': 3000, 'flow_rate': 3, 'head': 5.5, 'power': 0.12, 'pump_type': 'QDX', 'efficiency': 22.1},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 3.5, 'power': 0.12, 'pump_type': 'QDX', 'efficiency': 27.1},
#
#     {'rotation_speed': 3000, 'flow_rate': 1.5, 'head': 9, 'power': 0.18, 'pump_type': 'QDX', 'efficiency': 12.7},
#     {'rotation_speed': 3000, 'flow_rate': 3, 'head': 8, 'power': 0.18, 'pump_type': 'QDX', 'efficiency': 21.4},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 5, 'power': 0.18, 'pump_type': 'QDX', 'efficiency': 28.3},
#     {'rotation_speed': 3000, 'flow_rate': 10, 'head': 3.5, 'power': 0.18, 'pump_type': 'QDX', 'efficiency': 30.8},
#
#     {'rotation_speed': 3000, 'flow_rate': 1.5, 'head': 11, 'power': 0.25, 'pump_type': 'QDX', 'efficiency': 12.6},
#     {'rotation_speed': 3000, 'flow_rate': 3, 'head': 10, 'power': 0.25, 'pump_type': 'QDX', 'efficiency': 21.9},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 7, 'power': 0.25, 'pump_type': 'QDX', 'efficiency': 30.4},
#     {'rotation_speed': 3000, 'flow_rate': 10, 'head': 4.5, 'power': 0.25, 'pump_type': 'QDX', 'efficiency': 33.5},
#     {'rotation_speed': 3000, 'flow_rate': 15, 'head': 3, 'power': 0.25, 'pump_type': 'QDX', 'efficiency': 33.5},
#
#     {'rotation_speed': 3000, 'flow_rate': 1.5, 'head': 15, 'power': 0.37, 'pump_type': 'QDX', 'efficiency': 11.7},
#     {'rotation_speed': 3000, 'flow_rate': 3, 'head': 14, 'power': 0.37, 'pump_type': 'QDX', 'efficiency': 21.6},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 10, 'power': 0.37, 'pump_type': 'QDX', 'efficiency': 32.0},
#     {'rotation_speed': 3000, 'flow_rate': 10, 'head': 7, 'power': 0.37, 'pump_type': 'QDX', 'efficiency': 36.8},
#     {'rotation_speed': 3000, 'flow_rate': 15, 'head': 5, 'power': 0.37, 'pump_type': 'QDX', 'efficiency': 38.7},
#     {'rotation_speed': 3000, 'flow_rate': 25, 'head': 3, 'power': 0.37, 'pump_type': 'QDX', 'efficiency': 37.8},
# ]
# # 使用循环向数据库添加数据
# for item in data:
#     new_pump = Pump(**item)
#     session.add(new_pump)
# # 提交会话，将新数据写入数据库
# session.commit()
# # 关闭会话
# session.close()


# ————————————多级泵参数 表2———————————— #
# 定义 MultiPump 模型
class MultiPump(Base):
    __tablename__ = 'SSMultiStage_TableOne'  # 小型潜水电泵的多级泵参数-表2
    id = Column(Integer, primary_key=True)
    rotation_speed = Column(Float, nullable=False)  # 转速
    flow_rate = Column(Float, nullable=False)  # 流量
    head = Column(Float, nullable=False)  # 扬程
    stage = Column(Float, nullable=False)  # 级数
    power = Column(Float, nullable=False)  # 功率
    pump_type = Column(String(50), nullable=False)  # 类型
    efficiency = Column(Numeric(precision=10, scale=2), nullable=False)  # 电泵效率


#
#
# # 创建数据表
# Base.metadata.create_all(engine)
# # 创建一个会话类
# Session = sessionmaker(bind=engine)
# # 创建一个会话对象
# session = Session()
# # 添加数据
# data = [
#     {'rotation_speed': 3000, 'flow_rate': 3, 'head': 22, 'stage': 2, 'power': 0.75, 'pump_type': 'QD',
#      'efficiency': 24.6},
#     {'rotation_speed': 3000, 'flow_rate': 3, 'head': 30, 'stage': 2, 'power': 0.75, 'pump_type': 'QD',
#      'efficiency': 21.6},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 21, 'stage': 3, 'power': 0.75, 'pump_type': 'QX',
#      'efficiency': 39.4},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 21, 'stage': 3, 'power': 0.75, 'pump_type': 'Q',
#      'efficiency': 37.0},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 21, 'stage': 3, 'power': 0.75, 'pump_type': 'QY',
#      'efficiency': 34.7},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 21, 'stage': 3, 'power': 0.75, 'pump_type': 'QS',
#      'efficiency': 32.5},
#
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 20, 'stage': 2, 'power': 0.75, 'pump_type': 'QX',
#      'efficiency': 37.8},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 20, 'stage': 2, 'power': 0.75, 'pump_type': 'Q',
#      'efficiency': 35.4},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 20, 'stage': 2, 'power': 0.75, 'pump_type': 'QY',
#      'efficiency': 33.3},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 20, 'stage': 2, 'power': 0.75, 'pump_type': 'QS',
#      'efficiency': 31.1},
#
#     {'rotation_speed': 3000, 'flow_rate': 10, 'head': 14, 'stage': 2, 'power': 0.75, 'pump_type': 'QX',
#      'efficiency': 43.4},
#     {'rotation_speed': 3000, 'flow_rate': 10, 'head': 14, 'stage': 2, 'power': 0.75, 'pump_type': 'Q',
#      'efficiency': 40.7},
#     {'rotation_speed': 3000, 'flow_rate': 10, 'head': 14, 'stage': 2, 'power': 0.75, 'pump_type': 'QY',
#      'efficiency': 38.2},
#     {'rotation_speed': 3000, 'flow_rate': 10, 'head': 14, 'stage': 2, 'power': 0.75, 'pump_type': 'QS',
#      'efficiency': 35.8},
#
#     {'rotation_speed': 3000, 'flow_rate': 3, 'head': 45, 'stage': 3, 'power': 1.1, 'pump_type': 'QD',
#      'efficiency': 23.0},
#
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 32, 'stage': 4, 'power': 1.1, 'pump_type': 'QX',
#      'efficiency': 40.7},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 32, 'stage': 4, 'power': 1.1, 'pump_type': 'Q',
#      'efficiency': 38.1},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 32, 'stage': 4, 'power': 1.1, 'pump_type': 'QY',
#      'efficiency': 35.9},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'head': 32, 'stage': 4, 'power': 1.1, 'pump_type': 'QS',
#      'efficiency': 33.7},
# ]
# # 使用循环向数据库添加数据
# for item in data:
#     new_pump = MultiPump(**item)
#     session.add(new_pump)
# # 提交会话，将新数据写入数据库
# session.commit()
# session.close()

# ————————————表3———————————— #
# 定义 TableThree 模型
class TableThree(Base):
    __tablename__ = 'TableThree'  # 小型潜水电泵的单级泵参数-表1
    id = Column(Integer, primary_key=True)
    rotation_speed = Column(Float, nullable=False)  # 转速
    flow_rate = Column(Float, nullable=False)  # 流量
    pump_type = Column(String(50), nullable=False)  # 类型
    head = Column(Float, nullable=False)  # 扬程
    power = Column(Float, nullable=False)  # 功率
    efficiency = Column(Numeric(precision=10, scale=2), nullable=False)  # 电泵效率


#
#
# # 创建数据表
# Base.metadata.create_all(engine)
#
# # 创建一个会话类
# Session = sessionmaker(bind=engine)
# # 创建一个会话对象
# session = Session()
#
# # 添加数据
# data = [
#     {'rotation_speed': 3000, 'flow_rate': 6, 'pump_type': 'QXL', 'head': 10, 'power': 0.55,
#      'efficiency': 25.5},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'pump_type': 'QXR', 'head': 12, 'power': 0.75,
#      'efficiency': 21.9},
#
#     {'rotation_speed': 3000, 'flow_rate': 10, 'pump_type': 'QXL', 'head': 7, 'power': 0.55,
#      'efficiency': 29.1},
#     {'rotation_speed': 3000, 'flow_rate': 10, 'pump_type': 'QXR', 'head': 8, 'power': 0.75,
#      'efficiency': 24.5},
#
#     {'rotation_speed': 3000, 'flow_rate': 6, 'pump_type': 'QXL', 'head': 13, 'power': 0.75,
#      'efficiency': 26.4},
#     {'rotation_speed': 3000, 'flow_rate': 6, 'pump_type': 'QXR', 'head': 17, 'power': 1.1,
#      'efficiency': 22.5},
#
#     {'rotation_speed': 3000, 'flow_rate': 10, 'pump_type': 'QXL', 'head': 9, 'power': 0.75,
#      'efficiency': 30.4},
#     {'rotation_speed': 3000, 'flow_rate': 10, 'pump_type': 'QXR', 'head': 11, 'power': 1.1,
#      'efficiency': 25.6},
#
#     {'rotation_speed': 3000, 'flow_rate': 15, 'pump_type': 'QXL', 'head': 7, 'power': 0.75,
#      'efficiency': 33.0},
#     {'rotation_speed': 3000, 'flow_rate': 15, 'pump_type': 'QXR', 'head': 8, 'power': 1.1,
#      'efficiency': 27.8},
# ]
# # 使用循环向数据库添加数据
# for item in data:
#     new_pump = TableThree(**item)
#     session.add(new_pump)
# # 提交会话，将新数据写入数据库
# session.commit()
# session.close()


# ————————————检查是否跳转附录A———————————— #
# 定义一个函数来查询泵效率
def query_pump_efficiency(session, Input_data):
    found_match = False  # 设置一个标志来记录是否找到匹配记录

    for data in Input_data:

        print("正在执行查询，条件为：", data)

        # 查询第一个表
        query_pump1 = session.query(Pump).filter_by(
            **{key: data[key] for key in data.keys() if hasattr(Pump, key)}
        ).first()

        if query_pump1:
            found_match = True
            return query_pump1.efficiency

        # 查询第二个表
        query_pump2 = None
        if 'stage' in data:  # 只有表二有 stage 属性，所以在查询表二时才匹配 stage
            query_pump2 = session.query(MultiPump).filter_by(
                **{key: data[key] for key in data.keys() if hasattr(MultiPump, key)}
            ).first()

        if query_pump2:
            found_match = True
            return query_pump2.efficiency

        # 查询第三个表
        query_pump3 = session.query(TableThree).filter_by(
            **{key: data[key] for key in data.keys() if hasattr(TableThree, key)}
        ).first()

        if query_pump3:
            found_match = True
            return query_pump3.efficiency

    if not found_match:
        return None  # 没有找到匹配记录，返回空值


# ——————————————计算比转速—————————— #
def calculate_ns(n, Q, H):
    if Q > 3000:
        Q = 3000
    ns = 3.65 * n * math.sqrt(Q / 3600) / (H ** 0.75)
    return ns


# ————————————表A.1 ns:120~210 下泵式———————————— #
def Q_X(Q):
    # 手动输入数据
    Q_value = [1.5, 3, 6, 10, 12.5, 15, 20, 25, 30, 35, 40, 50, 60, 65, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400,
               500, 600]
    # 目标能效限定值
    Esp = [42.0, 52.5, 61.0, 66.0, 67.8, 69.5, 71.5, 72.9, 74.0, 74.8, 75.5, 76.5, 77.0, 77.4, 77.8, 78.0, 78.5, 79.0,
           79.3, 80.0, 80.5, 80.9, 81.1, 81.8, 82.0, 82.5]
    # 创建插值函数
    interpolation_function = interp1d(Q_value, Esp, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    Esp_result = interpolation_function(Q)
    # 返回结果
    return Esp_result


# ————————————表A.1 ns:120~210 上泵式———————————— #
def Q_(Q):
    # 手动输入数据
    Q_value = [1.5, 3, 6, 10, 12.5, 15, 20, 25, 30, 35, 40, 50, 60, 65, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400,
               500, 600, 700, 800, 900, 1000]
    # 目标能效限定值
    Esp = [39.0, 49.3, 57.4, 62.0, 64.0, 65.3, 67.0, 68.7, 69.5, 70.3, 71.0, 72.0, 72.7, 73.0, 73.2, 73.7, 74.0, 74.1,
           74.9, 75.3, 75.9, 76.1, 76.6, 76.9, 77.0, 77.2, 77.3, 77.4, 77.5, 77.5]
    # 创建插值函数
    interpolation_function = interp1d(Q_value, Esp, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    Esp_result = interpolation_function(Q)
    # 返回结果
    return Esp_result


# ————————————表A.1 ns:100~200 QXL———————————— #
def QXL(Q):
    # 手动输入数据
    Q_value = [3, 6, 10, 12.5, 15, 20, 25, 30, 35, 40, 50, 60, 65, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400,
               500]
    # 目标能效限定值
    Esp = [34.0, 42.0, 47.0, 49.0, 50.7, 56.0, 54.6, 56.0, 57.0, 58.0, 59.3, 60.4, 60.9, 61.2, 62.0, 62.5, 63.0, 64.0,
           64.8, 65.8, 66.4, 67.0, 67.5, 68.0]
    # 创建插值函数
    interpolation_function = interp1d(Q_value, Esp, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    Esp_result = interpolation_function(Q)
    # 返回结果
    return Esp_result


# ————————————表A.1 ns:100~200 QXR———————————— #
def QXR(Q):
    # 手动输入数据
    Q_value = [3, 6, 10, 12.5, 15, 20, 25, 30, 35, 40, 50, 60, 65, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400]
    # 目标能效限定值
    Esp = [29.0, 34.5, 38.3, 40.0, 41.2, 43.2, 44.9, 46.0, 47.0, 48.0, 49.3, 50.5, 51.0, 51.4, 52.0, 52.9, 53.7, 54.8,
           55.9, 57.0, 58.0, 59.0, 60.0]
    # 创建插值函数
    interpolation_function = interp1d(Q_value, Esp, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    Esp_result = interpolation_function(Q)
    # 返回结果
    return Esp_result


# ————————————表A.2 上下泵式修正 ns<120 ———————————— #
def Q_X_correction_1(ns):
    # 手动输入数据
    NS_value = [15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    # 目标能效限定值
    E = [30.0, 25.0, 19.0, 14.0, 10.0, 7.0, 5.0, 3.0, 2.0, 1.0, 0.3, 0]
    # 创建插值函数
    interpolation_function = interp1d(NS_value, E, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    E_result = interpolation_function(ns)
    # 返回结果
    return E_result


# ————————————表A.2 上下泵式修正 ns>210 ———————————— #
def Q_X_correction_2(ns):
    # 手动输入数据
    NS_value = [210, 260, 280, 300, 350, 400, 440, 460, 480, 500]
    # 目标能效限定值
    E = [0, 0.3, 1.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0, 5.0]
    # 创建插值函数
    interpolation_function = interp1d(NS_value, E, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    E_result = interpolation_function(ns)
    # 返回结果
    return E_result


# ————————————表A.2 其他修正 ns<100 ———————————— #
def Q_XRL_correction_1(ns):
    # 手动输入数据
    NS_value = [20, 30, 40, 50, 60, 70, 80, 90, 100]
    # 目标能效限定值
    E = [5.0, 3.0, 2.0, 1.5, 1.0, 0.65, 0.3, 0.2, 0.1]
    # 创建插值函数
    interpolation_function = interp1d(NS_value, E, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    E_result = interpolation_function(ns)
    # 返回结果
    return E_result


# ————————————表A.2 其他修正 ns>200 ———————————— #
def Q_XRL_correction_2(ns):
    # 手动输入数据
    NS_value = [200, 260, 280, 300, 350, 400, 440, 460, 480, 500]
    # 目标能效限定值
    E = [0, 0.1, 0.2, 0.3, 1.1, 1.7, 2.0, 2.2, 2.3, 2.5]
    # 创建插值函数
    interpolation_function = interp1d(NS_value, E, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    E_result = interpolation_function(ns)
    # 返回结果
    return E_result


# ————————————计算泵效率Eb———————————— #
def Eb(pump_type, Q, ns):
    Eb_result = 0
    if 'X' in pump_type and 'XR' not in pump_type and 'XL' not in pump_type:
        if 120 <= ns <= 210:
            Eb_result = Q_X(Q)
        elif ns < 120:
            Eb_result = Q_X(Q) - Q_X_correction_1(ns)
        elif ns > 210:
            Eb_result = Q_X(Q) - Q_X_correction_2(ns)
    if 'X' not in pump_type:
        if 120 <= ns <= 210:
            Eb_result = Q_(Q)
        elif ns < 120:
            Eb_result = Q_(Q) - Q_X_correction_1(ns)
        elif ns > 210:
            Eb_result = Q_(Q) - Q_X_correction_2(ns)
    if 'XL' in pump_type:
        if 100 <= ns <= 200:
            Eb_result = QXL(Q)
        elif ns < 100:
            Eb_result = QXL(Q) - Q_XRL_correction_1(ns)
        elif ns > 200:
            Eb_result = QXL(Q) - Q_XRL_correction_2(ns)
    if 'XR' in pump_type:
        if 100 <= ns <= 200:
            Eb_result = QXR(Q)
        elif ns < 100:
            Eb_result = QXR(Q) - Q_XRL_correction_1(ns)
        elif ns > 200:
            Eb_result = QXR(Q) - Q_XRL_correction_2(ns)
    return Eb_result


# ————————————建立数据表四———————————— #
# 定义 SmallTableFour 模型
class SmallTableFour(Base):
    __tablename__ = 'SmallTableFour'
    id = Column(Integer, primary_key=True)
    power = Column(Numeric(precision=10, scale=2), nullable=False)  # 功率
    typeOne = Column(String(50), nullable=True)  # 类型1-是否是单相
    typeTwo = Column(String(50), nullable=True)  # 类型2-充油式/充水式/干式
    n = Column(Integer, nullable=False)  # 转速
    Ed = Column(Numeric(precision=10, scale=2), nullable=False)  # 电动机效率


#
#
# # 创建数据表
# Base.metadata.create_all(engine)
# # 创建一个会话类
# Session = sessionmaker(bind=engine)
# # 创建一个会话对象
# session = Session()
# # 添加数据
# data = [
#     {'power': 0.12, 'typeOne': 'D', 'typeTwo': '', 'n': 3000, 'Ed': 47},
#     {'power': 0.18, 'typeOne': 'D', 'typeTwo': '', 'n': 3000, 'Ed': 49},
#     {'power': 0.25, 'typeOne': 'D', 'typeTwo': '', 'n': 3000, 'Ed': 53},
#     {'power': 0.37, 'typeOne': 'D', 'typeTwo': 'Y', 'n': 3000, 'Ed': 52},
#     {'power': 0.37, 'typeOne': 'D', 'typeTwo': 'S', 'n': 3000, 'Ed': 50},
#     {'power': 0.37, 'typeOne': 'D', 'typeTwo': '', 'n': 3000, 'Ed': 58},
#     {'power': 0.55, 'typeOne': 'D', 'typeTwo': 'Y', 'n': 3000, 'Ed': 54},
#     {'power': 0.55, 'typeOne': 'D', 'typeTwo': 'S', 'n': 3000, 'Ed': 52},
#     {'power': 0.55, 'typeOne': 'D', 'typeTwo': '', 'n': 3000, 'Ed': 61},
#     {'power': 0.55, 'typeOne': '', 'typeTwo': 'Y', 'n': 3000, 'Ed': 56},
#     {'power': 0.55, 'typeOne': '', 'typeTwo': 'S', 'n': 3000, 'Ed': 54},
#     {'power': 0.55, 'typeOne': '', 'typeTwo': '', 'n': 3000, 'Ed': 65},
# ]
# # 使用循环向数据库添加数据
# for item in data:
#     new_pump = SmallTableFour(**item)
#     session.add(new_pump)
# # 提交会话，将新数据写入数据库
# session.commit()
# session.close()


# ————————————查表4———————————— #
# 创建会话
Session = sessionmaker(bind=engine)
session = Session()


# 定义一个函数来查询 Ed
def get_Ed(power, pump_type, rotation_speed):
    Ed_result = 0
    # 将输入的 type 拆分为字符列表
    type_chars = list(pump_type)

    # 构建查询条件
    typeOne_conditions = []
    typeTwo_conditions = []
    for char in type_chars:
        if char == 'D':
            typeOne_conditions.append(SmallTableFour.typeOne.like(f'%{char}%'))
        elif char == 'Y' or char == 'S':
            typeTwo_conditions.append(SmallTableFour.typeTwo.like(f'%{char}%'))

    # 如果没有匹配到任何条件，说明输入的 type 是空字符，添加一个匹配空字符的条件
    if not typeOne_conditions:
        typeOne_conditions.append(SmallTableFour.typeOne == '')
    if not typeTwo_conditions:
        typeTwo_conditions.append(SmallTableFour.typeTwo == '')

    # 查询数据库
    result = session.query(SmallTableFour.Ed).filter(SmallTableFour.power == power).filter(
        SmallTableFour.n == rotation_speed).filter(
        and_(*typeOne_conditions), and_(*typeTwo_conditions)
    ).first()
    if result is not None:
        Ed_decimal = result[0]
        Ed_result = float(Ed_decimal)
    else:
        print("未找到匹配记录")

    return Ed_result


# ————————————电泵效率偏差———————————— #
def Ed_deviation(power, pump_type, rotation_speed):
    Ed = get_Ed(power, pump_type, rotation_speed)
    EdDeviation = -((0.1003 / (Ed / 100 - 0.02)) - 0.067) * 100

    return EdDeviation


# ————————————计算电泵效率———————————— #
def Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power):
    # 调用查询函数
    Session = sessionmaker(bind=engine)
    session = Session()

    E_result = query_pump_efficiency(session, Input_data)

    # 关闭会话
    session.close()
    if E_result is None:
        E_result = Eb(pump_type, Q, ns) * get_Ed(power, pump_type, rotation_speed) / 100 - 1.5
    return E_result


# ————————————能效1级———————————— #
def efficiencyOne(power, pump_type):
    EOne = 0
    if power <= 3:
        if 'QXL' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 2.5
        elif 'QXR' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.5
        elif 'QS' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 2.0
        elif 'QY' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 2.5
        elif 'QDX' in pump_type or 'QD' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 2.0
        elif 'QX' in pump_type or 'Q' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.0
        else:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.0
    elif 3 < power <= 11:
        if 'QXL' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.0
        elif 'QXR' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 2.0
        elif 'QS' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 2.5
        elif 'QY' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.0
        elif 'QX' in pump_type or 'Q' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.5
        else:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.5
    elif 11 < power <= 22:
        if 'QXL' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.5
        elif 'QXR' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 2.5
        elif 'QS' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 2.5
        elif 'QY' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.0
        elif 'QX' in pump_type or 'Q' in pump_type:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.5
        else:
            EOne = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 3.5
    return EOne


# ————————————能效2级———————————— #
def efficiencyTwo(power, pump_type):
    ETwo = 0
    if power <= 3:
        if 'QXL' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.3
        elif 'QXR' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 0.8
        elif 'QS' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.0
        elif 'QY' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.3
        elif 'QDX' in pump_type or 'QD' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.0
        elif 'QX' in pump_type or 'Q' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.5
        else:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.5
    elif 3 < power <= 11:
        if 'QXL' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.5
        elif 'QXR' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.0
        elif 'QS' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.3
        elif 'QY' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.5
        elif 'QX' in pump_type or 'Q' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.8
        else:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.8
    elif 11 < power <= 22:
        if 'QXL' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.8
        elif 'QXR' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.3
        elif 'QS' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.3
        elif 'QY' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.5
        elif 'QX' in pump_type or 'Q' in pump_type:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.8
        else:
            ETwo = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) + 1.8
    return ETwo

# ——————————能效3级———————————— #
def efficiencyThree(session, Input_data, pump_type, Q, ns, rotation_speed, power):
    EThree = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power) - Ed_deviation(power, pump_type, rotation_speed)
    return EThree

# ————————————示例输入———————————— #
def get_input_data():
    rotation_speed = int(input("请输入转速："))
    flow_rate = float(input("请输入流量："))
    head = float(input("请输入扬程："))
    stage = int(input("请输入级数："))
    power = float(input("请输入功率："))
    pump_type = input("请输入泵类型：")
    ns = int(input("请输入ns："))

    return {'rotation_speed': rotation_speed, 'flow_rate': flow_rate, 'head': head, 'stage': stage, 'power': power,
            'pump_type': pump_type, 'ns': ns}


# 初始化示例数据数组
Input_data = []

# 循环获取用户输入，并将数据添加到示例数据数组中
while True:
    data = get_input_data()
    Input_data.append(data)

    continue_input = input("是否继续输入？(y/n): ")
    if continue_input.lower() != 'y':
        break

rotation_speed = data['rotation_speed']
Q = data['flow_rate']
pump_type = data['pump_type']
head = data['head']
stage = data['stage']
power = data['power']
ns = data['ns']

E_finally_result = Efficiency(session, Input_data, pump_type, Q, ns, rotation_speed, power)
print(f"电泵效率为：{E_finally_result:.2f}%")


# ————————————计算实际的能效等级———————————— #
def real_efficiency():
    realE = int(input("请输入实际效率："))
    if realE >= efficiencyOne(power, pump_type):
        print("1级")
    elif efficiencyTwo(power, pump_type) <= realE <= efficiencyOne(power, pump_type):
        print("2级")
    elif efficiencyThree(session, Input_data, pump_type, Q, ns, rotation_speed, power) <= realE <= efficiencyTwo(power, pump_type):
        print("3级")
    else:
        print("不合格！")
