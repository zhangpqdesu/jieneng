# ————————————石油化工离心泵———————————— #

import math
from scipy.interpolate import interp1d


# ————————————计算比转速—————————————— #
# 单吸
def calculate_ns_1(n, Q, H):
    if Q > 3000:
        Q = 3000
    ns = 3.65 * n * math.sqrt(Q / 3600) / (H ** 0.75)
    return ns


# 双吸
def calculate_ns_2(n, Q, H):
    if Q > 3000:
        Q = 3000
    ns = 3.65 * n * math.sqrt(Q / 7200) / (H ** 0.75)
    return ns


# ————————————图1 流量-目标能效限定值的关系曲线图———————————— #
def target_energy_efficiency_limit(Q):
    # 手动输入数据
    Q_value = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
               1500, 2000, 3000]
    # 目标能效限定值
    TargetEEL_value = [48.0, 54.1, 57.5, 59.9, 61.8, 63.0, 65.1, 66.8, 68.0, 69.0, 69.8, 70.5, 71.0, 73.0, 74.4, 76.2,
                       77.4, 78.2, 78.9, 79.4, 79.9, 80.2, 80.5, 81.6, 82.2, 83.0]
    # 创建插值函数
    interpolation_function = interp1d(Q_value, TargetEEL_value, kind='linear')
    # 使用插值函数计算对应的目标能效限定值
    TargetEEL_result = interpolation_function(Q)
    # 返回结果
    return TargetEEL_result


# ————————————图1 流量-基准值的关系曲线图———————————— #
def base_efficiency(Q):
    # 手动输入数据
    Q_value = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
               1500, 2000, 3000]
    # 基准值
    BaseE_value = [50.0, 56.1, 59.5, 61.9, 63.8, 65.0, 67.1, 68.8, 70.0, 71.0, 71.8, 72.5, 73.0, 75.0, 76.4, 78.2, 79.4,
                   80.2, 80.9, 81.4, 81.9, 82.2, 82.5, 83.6, 84.2, 85.0]
    # 创建插值函数
    interpolation_function = interp1d(Q_value, BaseE_value, kind='linear')
    # 使用插值函数计算对应的基准值
    BaseE_result = interpolation_function(Q)
    # 返回结果
    return BaseE_result


# ————————————图2 ns=20-120 ns-效率修正值的关系曲线图———————————— #
def efficiency_correction_factor_1(ns):
    # 手动输入数据
    Ns_value = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120]
    # 效率修正值
    Correction_value = [32, 25.5, 20.6, 17.3, 14.7, 12.5, 10.5, 8.8, 7.3, 6.0, 4.9, 4.0, 3.2, 2.6, 2.0, 1.5, 1.0, 0.3,
                        0]
    # 创建插值函数
    interpolation_function = interp1d(Ns_value, Correction_value, kind='linear')
    # 使用插值函数计算对应的效率修正值
    Correction_result = interpolation_function(ns)
    # 返回结果
    return Correction_result


# ————————————图3 ns=210-300 ns-效率修正值的关系曲线图———————————— #
def efficiency_correction_factor_2(ns):
    # 手动输入数据
    Ns_value = [210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    # 效率修正值
    Correction_value = [0, 0.3, 0.7, 1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0]
    # 创建插值函数
    interpolation_function = interp1d(Ns_value, Correction_value, kind='linear')
    # 使用插值函数计算对应的效率修正值
    Correction_result = interpolation_function(ns)
    # 返回结果
    return Correction_result


# ————————————查找效率修正值———————————— #
def search_correction_factor(ns):
    if 20 <= ns < 120:
        efficiency_correction_factor_1(ns)
    elif 210 < ns <= 300:
        efficiency_correction_factor_2(ns)


# ————————————泵规定点效率———————————— #
def specified_point_efficiency(ns):
    SpecifiedPE_result = 0
    if 20 <= ns < 120 or 210 < ns <= 300:
        SpecifiedPE_result = base_efficiency(Q) - search_correction_factor(ns)
    elif 120 <= ns <= 210:
        SpecifiedPE_result = base_efficiency(Q)
    return SpecifiedPE_result


# ————————————泵目标能效限定值-能效3级———————————— #
def pump_target_efficiency_limit(ns):
    PumpTargetEL_result = 0
    if 20 <= ns < 120 or 210 < ns <= 300:
        PumpTargetEL_result = target_energy_efficiency_limit(Q) - search_correction_factor(ns)
    elif 120 <= ns <= 210:
        PumpTargetEL_result = target_energy_efficiency_limit(Q)
    return PumpTargetEL_result


# ————————————泵节能评价值-能效2级———————————— #
def pump_energy_saving_evaluation_value(ns, Q):
    PumpSavingEV_result = 0
    if 20 <= ns < 60:
        PumpSavingEV_result = specified_point_efficiency(ns) + 5
    elif 60 <= ns < 120:
        PumpSavingEV_result = specified_point_efficiency(ns) + 1
    elif 120 <= ns <= 300:
        if 5 <= Q <= 300:
            PumpSavingEV_result = specified_point_efficiency(ns) + 1
        elif Q > 300:
            PumpSavingEV_result = specified_point_efficiency(ns) + 2
    return PumpSavingEV_result


# ————————————能效1级———————————— #
def one_level_value(ns, Q):
    OneLV_result = 0
    if 20 <= ns < 60:
        if 5 <= Q <= 300:
            OneLV_result = specified_point_efficiency(ns) + 10
        elif Q > 300:
            OneLV_result = specified_point_efficiency(ns) + 11
    elif 60 <= ns < 120:
        if 5 <= Q <= 300:
            OneLV_result = specified_point_efficiency(ns) + 4
        elif Q > 300:
            OneLV_result = specified_point_efficiency(ns) + 5
    elif 120 <= ns <= 300:
        OneLV_result = specified_point_efficiency(ns) + 3
    return OneLV_result


# ————————————实际泵效率———————————— #
def actual_pump_efficiency(Rho, H, Q, P):
    pump_effective_power = Rho * 9.81 * H * Q / 3600
    pump_input_power = P
    RealEfficiency = (pump_effective_power / pump_input_power) * 100

    return RealEfficiency


# ————————————示例输入———————————— #
n = 2980  # 转速
Q = 325  # 流量
H = 73.5  # 扬程
P = 87.91  # 功率
Rho = 1  # 密度
Type = '单吸'

# ————————————结果———————————— #
ns = 0
# 求比转速
if Type == '单吸':
    ns = calculate_ns_1(n, Q, H)
elif Type == '双吸':
    ns = calculate_ns_2(n, Q, H)

# 泵目标能效限定值=能效三级
ThreeLevel_value = pump_target_efficiency_limit(ns)
print(f"泵目标能效限定值(能效3级)为:{ThreeLevel_value:.1f}%")

# 泵节能评价值
TwoLevel_value = pump_energy_saving_evaluation_value(ns, Q)
print(f"泵节能评价值(能效2级)为:{TwoLevel_value:.1f}%")

# 能效1级的值
OneLevel_value = one_level_value(ns, Q)
print(f"能效1级的值为:{OneLevel_value:.1f}%")

# 实际泵效率
real_efficiency = actual_pump_efficiency(Rho, H, Q, P)
print(f"实际泵效率为:{real_efficiency:.1f}%")
