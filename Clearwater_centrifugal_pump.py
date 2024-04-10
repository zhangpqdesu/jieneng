# ————————————清水离心泵———————————— #

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


# ————————————计算比转速———————————— #
# 单吸
def calculate_ns_1(n, Q, H):
    ns = 3.65 * n * math.sqrt(Q / 3600) / (H ** 0.75)
    return ns


# 双吸
def calculate_ns_2(n, Q, H):
    ns = 3.65 * n * math.sqrt(Q / 7200) / (H ** 0.75)
    return ns


# ————————————单级清水离心泵———————————— #
# ————————————查流量-目标能效限定值曲线图———————————— #
# ————————————查流量-基准值曲线图———————————— #
def single_stage_pump(Q):
    # 手动输入数据
    Q_value = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
               1500,
               2000, 3000]
    # 目标能效限定值
    TargetEnergy_value = [56.0, 62.0, 65.2, 67.4, 68.9, 70.0, 71.8, 72.9, 73.8, 74.5, 75.0, 75.6, 76.0, 77.8, 78.8,
                          80.0,
                          81.0, 81.7, 82.2, 82.7, 83.0, 83.3, 83.7, 84.6, 85.2, 86.0]
    # 基准值
    Baseline_value = [58.0, 64.0, 67.2, 69.4, 70.9, 72.0, 73.8, 74.9, 75.8, 76.5, 77.0, 77.6, 78.0, 79.8,
                      80.8,
                      82.0, 83.0, 83.7, 84.2, 84.7, 85.0, 85.3, 85.7, 86.6, 87.2, 88.0]
    # 创建插值函数
    interpolation_function_1 = interp1d(Q_value, TargetEnergy_value, kind='linear')
    interpolation_function_2 = interp1d(Q_value, Baseline_value, kind='linear')
    # 使用插值函数计算对应的目标能效限定值和基准值
    Target_energy_efficiency = interpolation_function_1(Q)
    Baseline_efficiency = interpolation_function_2(Q)
    # 返回结果
    return Target_energy_efficiency, Baseline_efficiency

    # # 拟合的曲线图
    # # 生成更密集的数据点用于绘图
    # Q_dense = np.linspace(min(Q_value), max(Q_value), 1000)
    # target_dense = interpolation_function_1(Q_dense)
    # baseline_dense = interpolation_function_2(Q_dense)
    #
    # # 绘制曲线图
    # # 创建两个子图
    # fig, ax1 = plt.subplots()
    # # 绘制第一条曲线
    # color = 'tab:blue'
    # ax1.set_xlabel('流量 (Q/(m^3/h))', fontproperties='SimHei')
    # ax1.set_ylabel('效率 (η/%)', fontproperties='SimHei', color=color)
    # ax1.plot(Q_value, TargetEnergy_value, label='TargetEnergy_value')
    # ax1.tick_params(axis='y', labelcolor=color)
    # # 绘制第二条曲线
    # ax2 = ax1.twinx()
    # color = 'tab:red'
    # ax1.set_ylabel('效率 (η/%)', fontproperties='SimHei', color=color)
    # ax1.plot(Q_value, Baseline_value, label='Baseline_value')
    # ax1.tick_params(axis='y', labelcolor=color)
    # # 添加图例
    # fig.tight_layout()
    # fig.legend(loc='upper right')
    # plt.title('单级流量与目标能效限定值及基准值关系曲线图', fontproperties='SimHei')
    # plt.grid(True)
    # plt.show()


# ————————————多级清水离心泵———————————— #
# ————————————查流量-目标能效限定值曲线图———————————— #
# ————————————查流量-基准值曲线图———————————— #
def multi_stage_pump(Q):
    # 手动输入数据
    Q_value = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
               1500,
               2000, 3000]
    # 目标能效限定值
    TargetEnergy_value = [53.4, 57.4, 59.8, 61.5, 62.8, 63.9, 65.5, 66.9, 67.9, 68.9, 69.5, 70.3, 70.9, 73.3, 74.9,
                          77.2, 78.6, 79.5, 80.2, 80.8, 81.1, 81.5, 81.9, 82.8, 83.1, 83.5]
    # 基准值
    Baseline_value = [55.4, 59.4, 61.8, 63.5, 64.8, 65.9, 67.5, 68.9, 69.9, 70.9, 71.5, 72.3, 72.9, 75.3, 76.9, 79.2,
                      80.6, 81.5, 82.2, 82.8, 83.1, 83.5, 83.9, 84.8, 85.1, 85.5]
    # 创建插值函数
    interpolation_function_1 = interp1d(Q_value, TargetEnergy_value, kind='linear')
    interpolation_function_2 = interp1d(Q_value, Baseline_value, kind='linear')
    # 使用插值函数计算对应的目标能效限定值和基准值
    Target_energy_efficiency = interpolation_function_1(Q)
    Baseline_efficiency = interpolation_function_2(Q)
    # 输出查得的结果
    return Target_energy_efficiency, Baseline_efficiency

    # # 拟合的曲线图
    # # 生成更密集的数据点用于绘图
    # Q_dense = np.linspace(min(Q_value), max(Q_value), 1000)
    # target_dense = interpolation_function_1(Q_dense)
    # baseline_dense = interpolation_function_2(Q_dense)
    #
    # # 绘制曲线图
    # # 创建两个子图
    # fig, ax1 = plt.subplots()
    # # 绘制第一条曲线
    # color = 'tab:blue'
    # ax1.set_xlabel('流量 (Q/(m^3/h))', fontproperties='SimHei')
    # ax1.set_ylabel('效率 (η/%)', fontproperties='SimHei', color=color)
    # ax1.plot(Q_value, TargetEnergy_value, label='TargetEnergy_value')
    # ax1.tick_params(axis='y', labelcolor=color)
    # # 绘制第二条曲线
    # ax2 = ax1.twinx()
    # color = 'tab:red'
    # ax1.set_ylabel('效率 (η/%)', fontproperties='SimHei', color=color)
    # ax1.plot(Q_value, Baseline_value, label='Baseline_value')
    # ax1.tick_params(axis='y', labelcolor=color)
    # # 添加图例
    # fig.tight_layout()
    # fig.legend(loc='upper right')
    # plt.title('多级流量与目标能效限定值及基准值关系曲线图', fontproperties='SimHei')
    # plt.grid(True)
    # plt.show()


# ————————————查比转速-效率修正值曲线图 n_s=20~120———————————— #
def efficiency_correction_value1(ns):
    # 横坐标比转速的值
    Ns_value = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 850, 90, 95, 100, 110, 120]
    # 效率修正值
    Correction_value = [32, 25.5, 20.6, 17.3, 14.7, 12.5, 10.5, 9.0, 7.5, 6.0, 5.0, 4.0, 3.2, 2.5, 2.0, 1.5, 1.0, 0.5,
                        0]
    # 创建插值函数
    interpolation_function = interp1d(Ns_value, Correction_value, kind='linear')
    # 使用插值函数计算对应的修正值
    Efficiency_correction_value = interpolation_function(ns)
    # 输出查到的效率修正值
    return Efficiency_correction_value


# ————————————查比转速-效率修正值曲线图 n_s=20~120———————————— #
def efficiency_correction_value2(ns):
    # 横坐标比转速的值
    Ns_value = [210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    # 效率修正值
    Correction_value = [0, 0.3, 0.7, 1.0, 1.3, 1.7, 1.9, 2.2, 2.7, 3.0]
    # 创建插值函数
    interpolation_function = interp1d(Ns_value, Correction_value, kind='linear')
    # 使用插值函数计算对应的修正值
    Efficiency_correction_value = interpolation_function(ns)
    # 输出查到的效率修正值
    return Efficiency_correction_value


# ————————————泵目标能效限定值———————————— #
def pump_target_efficiency_value(Type, n, Q, H):
    if '单级单吸' in Type:
        ns = calculate_ns_1(n, Q, H)
    elif '单级双吸' in Type:
        ns = calculate_ns_2(n, Q, H)
    pump_target_efficiency = 0
    if 5 <= Q <= 10000 and 120 <= ns <= 210:
        if '单级单吸' in Type or '单级多吸' in Type:
            result = single_stage_pump(Q)
            pump_target_efficiency = result[0]
        elif '多级' in Type:
            result = multi_stage_pump(Q)
            pump_target_efficiency = result[0]
        else:
            print("不是单级也不是多级")
    elif 5 <= Q <= 10000 and 20 <= ns <= 120:
        if '单级' in Type or '单级多吸' in Type:
            result = single_stage_pump(Q)
            Efficiency_correction_value = efficiency_correction_value1(ns)
            pump_target_efficiency = result[0] - Efficiency_correction_value
        elif '多级' in Type:
            result = multi_stage_pump(Q)
            Efficiency_correction_value = efficiency_correction_value1(ns)
            pump_target_efficiency = result[0] - Efficiency_correction_value
        else:
            print("不是单级也不是多级")
    elif 5 <= Q <= 10000 and 120 <= ns <= 300:
        if '单级' in Type or '单级多吸' in Type:
            result = single_stage_pump(Q)
            Efficiency_correction_value = efficiency_correction_value1(ns)
            pump_target_efficiency = result[0] - Efficiency_correction_value
        elif '多级' in Type:
            result = multi_stage_pump(Q)
            Efficiency_correction_value = efficiency_correction_value1(ns)
            pump_target_efficiency = result[0] - Efficiency_correction_value
        else:
            print("不是单级也不是多级")
    elif 10000 <= Q:
        pump_target_efficiency = 88
        # print(f"查曲线图2得到的流量为 {Q} 的目标能效限定值为：{pump_target_efficiency:.1f}%")
    else:
        print("流量数据错误！！！")

    return pump_target_efficiency


# ————————————泵节能评价值———————————— #
def pump_energySaving_assessment_value(Type, n, Q, H):
    if '单级单吸' in Type:
        ns = calculate_ns_1(n, Q, H)
    elif '单级双吸' in Type:
        ns = calculate_ns_2(n, Q, H)
    pump_energySaving = 0
    if 5 <= Q <= 10000 and 120 <= ns <= 210:
        if '单级单吸' in Type:
            if Q <= 300:
                result = single_stage_pump(Q)
                pump_energySaving = result[1] + 2
            elif Q > 300:
                result = single_stage_pump(Q)
                pump_energySaving = result[1] + 1
        elif '单级双吸' in Type:
            if Q <= 600:
                result = single_stage_pump(Q)
                pump_energySaving = result[1] + 2
            elif Q > 600:
                result = single_stage_pump(Q)
                pump_energySaving = result[1] + 1
        elif '多级' in Type:
            if Q <= 100:
                result = multi_stage_pump(Q)
                pump_energySaving = result[1] + 2
            elif Q > 100:
                result = multi_stage_pump(Q)
                pump_energySaving = result[1] + 1
    elif 5 <= Q <= 10000 and 20 <= ns <= 120:
        if '单级单吸' in Type:
            if Q <= 300:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value1(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 2
            elif Q > 300:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value1(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 1
        elif '单级多吸' in Type:
            if Q <= 600:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value1(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 2
            elif Q > 600:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value1(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 1
        elif '多级' in Type:
            if Q <= 100:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value1(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 2
            elif Q > 100:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value1(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 1
    elif 5 <= Q <= 10000 and 120 <= ns <= 300:
        if '单级单吸' in Type:
            if Q <= 300:
                result = single_stage_pump(Q)
                pump_energySaving = result[1] + 2
            elif Q > 300:
                result = single_stage_pump(Q)
                pump_energySaving = result[1] + 1
        elif '单级双吸' in Type:
            if Q <= 600:
                result = single_stage_pump(Q)
                pump_energySaving = result[1] + 2
            elif Q > 600:
                result = single_stage_pump(Q)
                pump_energySaving = result[1] + 1
        elif '多级' in Type:
            if Q <= 100:
                result = multi_stage_pump(Q)
                pump_energySaving = result[1] + 2
            elif Q > 100:
                result = multi_stage_pump(Q)
                pump_energySaving = result[1] + 1
    elif 5 <= Q <= 10000 and 20 <= ns <= 120:
        if '单级单吸' in Type:
            if Q <= 300:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value2(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 2
            elif Q > 300:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value2(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 1
        elif '单级多吸' in Type:
            if Q <= 600:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value2(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 2
            elif Q > 600:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value2(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 1
        elif '多级' in Type:
            if Q <= 100:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value2(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 2
            elif Q > 100:
                result = single_stage_pump(Q)
                Efficiency_correction_value = efficiency_correction_value2(ns)
                pump_energySaving = result[1] - Efficiency_correction_value + 1
    elif 10000 <= Q:
        pump_energySaving = 90
        # print(f"查曲线图2得到的流量为 {Q} 的目标能效限定值为：{pump_target_efficiency:.1f}%")
    else:
        print("流量数据错误！！！")

    return pump_energySaving


# ————————————实际泵效率———————————— #
def actual_pump_efficiency(Rho, H, Q, P):
    pump_effective_power = Rho * 9.81 * H * Q / 3600
    pump_input_power = P
    efficiency = (pump_effective_power / pump_input_power) * 100

    return efficiency


# ————————————比较结果———————————— #
def finally_result1(Rho, n, Q, H, P, Type, Efficiency):
    # 泵目标能效限定值
    pump_target_value = pump_target_efficiency_value(Type, n, Q, H)
    # print(f"泵目标能效限定值为:{pump_target_value:.1f}%")

    # 泵节能评价值
    pump_energySaving = pump_energySaving_assessment_value(Type, n, Q, H)
    # print(f"泵节能评价值为:{pump_energySaving:.1f}%")

    if Efficiency >= pump_energySaving:
        return '符合节能评价'
    elif pump_target_value <= Efficiency < pump_energySaving:
        return '符合目标能效限定值'
    else:
        return '低于目标能效限定值'

    # # 实际泵效率
    # real_efficiency = actual_pump_efficiency(Rho, H, Q, P)
    # print(f"实际泵效率为:{real_efficiency:.1f}%")
