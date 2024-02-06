import io
from copy import deepcopy
from typing import List, Dict, Any
import re
from pydantic import BaseModel
from PIL import Image
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from cnocr import CnOcr
from cnocr.utils import set_logger
from sqlalchemy import text
import math
import pymysql
logger = set_logger(log_level='DEBUG')

OCR_MODEL = CnOcr()
app = Flask(__name__)
#持久层框架，配置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Administrator:XWClassroom20202023@www.ylxteach.net:3366/demo?charset=gbk'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 电机对照表
class Motor(db.Model):
    __tablename__ = '电机对比参数表'
    电机型号 = db.Column(db.String(50), primary_key=True)
    效率 = db.Column(db.Float)
    额定功率 = db.Column(db.Float)
    转速 = db.Column(db.Integer)
    电机能级 = db.Column(db.String(20))


class PumpCalculation(db.Model):
    __tablename__ = '离心泵计算参数表'
    泵型号 = db.Column(db.String(50), primary_key=True)
    密度 = db.Column(db.Float)
    流量 = db.Column(db.Float)
    扬程 = db.Column(db.Float)
    输入功率 = db.Column(db.Float)
    泵效率 = db.Column(db.Float)
    流量 = db.Column(db.Float)
    扬程 = db.Column(db.Float)
    转速 = db.Column(db.Integer)
    能效 = db.Column(db.Float)
    detal = db.Column(db.Float)

class FanComparisonParameters(db.Model):
    __tablename__ = '风机对比参数表'
    fan_model = db.Column(db.String(50), nullable=False)#风机型号
    correction_factor = db.Column(db.Float, nullable=False)#修正系数
    outlet_stagnation_pressure = db.Column(db.Float, nullable=False)#出口滞止压力
    inlet_stagnation_pressure = db.Column(db.Float, nullable=False)#进口滞止压力
    inlet_stagnation_density = db.Column(db.Float, nullable=False)#进口滞止密度
    cascade_outer_circumferential_speed = db.Column(db.Float, nullable=False)#叶轮叶片外缘的圆周速度
    main_shaft_rotation_speed = db.Column(db.Integer, nullable=False)#主轴的转速
    fan_size = db.Column(db.String(50), nullable=False)# 机号
    impeller_hub_ratio = db.Column(db.Float, nullable=False)#轮毂比
    fan_level = db.Column(db.String(20), nullable=False)# 风机能级

    def __init__(self, fan_model, correction_factor, outlet_stagnation_pressure, inlet_stagnation_pressure, inlet_stagnation_density, cascade_outer_circumferential_speed, main_shaft_rotation_speed, fan_size, impeller_hub_ratio, fan_level):
        self.fan_model = fan_model
        self.correction_factor = correction_factor
        self.outlet_stagnation_pressure = outlet_stagnation_pressure
        self.inlet_stagnation_pressure = inlet_stagnation_pressure
        self.inlet_stagnation_density = inlet_stagnation_density
        self.cascade_outer_circumferential_speed = cascade_outer_circumferential_speed
        self.main_shaft_rotation_speed = main_shaft_rotation_speed
        self.fan_size = fan_size
        self.impeller_hub_ratio = impeller_hub_ratio
        self.fan_level = fan_level

    def __repr__(self):
        return f"<FanComparisonParameters {self.fan_model}>"

# ocr返回类
class OcrResponse:
    def __init__(self, results: List[Dict[str, Any]]) -> None:
        self.results = results

    def dict(self) -> Dict[str, Any]:
        return {'results': self.results}


# 获得电机对照表的参数
@app.route('/get_motor_params')
def get_motor_params():
    try:
        # 查询数据库中所有电机参数记录
        motor_records = Motor.query.all()

        # 将记录转换为字典形式
        motor_params = [{'电机型号': motor.电机型号, '效率': motor.效率, '额定功率': motor.额定功率, '转速': motor.转速, '电机能级': motor.电机能级} for motor in motor_records]

        # 返回 JSON 格式的参数
        return jsonify(motor_params)

    except Exception as e:
        return f'Database connection error: {str(e)}'

@app.route("/calculate_motor_energy_consumption", methods=['GET'])
def calculate_motor_energy_consumption():
    try:
        # From the request, get JSON data
        data = request.get_json()
        print(f'Received JSON data: {data}')

        speed_of_rotation = data['speedOfRotation']
        power = data['power']
        efficiency = data['efficiency']
        print(speed_of_rotation, power, efficiency)

        # Use the text function to declare the SQL expression
        sql_query = text(f"SELECT 电机能级 FROM 电机对比参数表 WHERE 转速 = {speed_of_rotation} AND 额定功率 = {power} AND 效率 <= {efficiency}")
        print(sql_query)

        # Execute the raw SQL query
        result = db.session.execute(sql_query).fetchone()
        print(result)

        if result:
            motor_energy_level = result[0]
            return jsonify({'motor_energy_level': motor_energy_level})

        # Handle the case when no matching record is found
        return jsonify({'error': '未找到匹配的电机参数'})

    except Exception as e:
        # Print detailed error information
        print(f'Exception type: {type(e).__name__}')
        print(f'Exception details: {str(e)}')
        return jsonify({'error': f'calculate motor energy consumption error: {str(e)}'})
#通风机效率计算
def ventilation_efficiency(inlet_volume_flow, outlet_pressure, inlet_pressure, compressibility_correction_factor, impeller_power):
    """
    计算通风机效率的函数

    参数：
    inlet_volume_flow (float): 通风机进口滞止容积流量，单位：立方米/秒
    outlet_pressure (float): 通风机出口滞止压力，单位：帕斯卡
    inlet_pressure (float): 通风机进口滞止压力，单位：帕斯卡
    compressibility_correction_factor (float): 压缩性修正系数
    impeller_power (float): 叶轮功率，单位：千瓦

    返回：
    float: 通风机效率，单位：百分比
    """
    efficiency = inlet_volume_flow * (outlet_pressure - inlet_pressure) * compressibility_correction_factor / (1000 * impeller_power) * 100
    return efficiency

def pressure_coefficient(outlet_pressure, inlet_pressure, compressibility_correction_factor, inlet_density, cascade_outer_circumferential_speed):
    """
    计算压力系数的函数

    参数：
    outlet_pressure (float): 通风机出口滞止压力，单位：帕斯卡
    inlet_pressure (float): 通风机进口滞止压力，单位：帕斯卡
    compressibility_correction_factor (float): 压缩性修正系数
    inlet_density (float): 通风机进口滞止密度，单位：千克/立方米
    cascade_outer_circumferential_speed (float): 叶轮叶片外缘的圆周速度，单位：米/秒

    返回：
    float: 压力系数
    """
    coefficient = (outlet_pressure - inlet_pressure) * compressibility_correction_factor / (inlet_density * cascade_outer_circumferential_speed * cascade_outer_circumferential_speed)
    return coefficient

def calculate_n_s(n, Q, outlet_pressure, inlet_pressure, compressibility_correction_factor, inlet_density):
    """
    计算单级单吸入式离心通风机的比转速

    参数：
    n (float): 通风机主轴的转速，单位为转每分钟（r/min）
    Q (float): 通风机进口滞止容积流量
    outlet_pressure (float): 通风机出口滞止压力，单位：帕斯卡
    inlet_pressure (float): 通风机进口滞止压力，单位：帕斯卡
    compressibility_correction_factor (float): 压缩性修正系数
    inlet_density (float): 通风机进口滞止密度，单位：千克/立方米

    返回：
    float: 单级单吸入式离心通风机的比转速
    """
    return 5.54 * n * (Q ** 0.5) / (1.2 * (outlet_pressure - inlet_pressure) * compressibility_correction_factor / inlet_density) ** 0.75

def calculate_n_s_double_inlet(n, Q, outlet_pressure, inlet_pressure, compressibility_correction_factor, inlet_density):
    """
    计算单级双吸入式离心通风机的比转速

    参数：
    n (float): 通风机主轴的转速，单位为转每分钟（r/min）
    Q (float): 通风机进口滞止容积流量
    outlet_pressure (float): 通风机出口滞止压力，单位：帕斯卡
    inlet_pressure (float): 通风机进口滞止压力，单位：帕斯卡
    compressibility_correction_factor (float): 压缩性修正系数
    inlet_density (float): 通风机进口滞止密度，单位：千克/立方米

    返回：
    float: 单级双吸入式离心通风机的比转速
    """
    return 5.54 * n * (Q / 2) ** 0.5 / (1.2 * (outlet_pressure - inlet_pressure) * compressibility_correction_factor / inlet_density) ** 0.75

@app.route('/ventilation_energy)consumption', methods=['POST'])
def ventilation_efficiency():
    data = request.get_json()
    inlet_volume_flow = data['inlet_volume_flow']
    outlet_pressure = data['outlet_pressure']
    inlet_pressure = data['inlet_pressure']
    compressibility_correction_factor = data['compressibility_correction_factor']
    impeller_power = data['impeller_power']
    inlet_density=data['inlet_density']
    cascade_outer_circumferential_speed=data['cascade_outer_circumferential_speed']
    efficiency = ventilation_efficiency(inlet_volume_flow, outlet_pressure, inlet_pressure, compressibility_correction_factor, impeller_power)
    coefficient = pressure_coefficient(outlet_pressure, inlet_pressure, compressibility_correction_factor, inlet_density, cascade_outer_circumferential_speed)
    n_s = calculate_n_s(n, Q, outlet_pressure, inlet_pressure, compressibility_correction_factor, inlet_density)

    conn = pymysql.connect(host='localhost', user='root', password='password', db='ventilation_db')
    cursor = conn.cursor()
    sql = "SELECT * FROM ventilation_records WHERE n_s=%s AND coefficient=%s AND efficiency=%s"
    cursor.execute(sql, (n_s, coefficient, efficiency))
    result = cursor.fetchone()

    if result:
        energy_grade = 'A' if result[3] > 90 else 'B'
        return {'energy_grade': energy_grade}
    else:
        return {'error': 'No matching record found'}

# 获取泵效率对应的能效等级      delta 的值查表得到，目前先暂定一个值（假设为2
def get_energy_efficiency_rating(pump_efficiency, flowrate, speed,delta=2):
    # 根据实际需求定义能效等级划分的逻辑
    if 5<=flowrate<=300:
        if 20<=speed<60:
            if delta>=10:
                return 'IE1'
            elif delta>=5:
                return 'IE2'
            elif delta>=-5:
                return 'IE3'
            else:return '输入参数错误或者未达到IE3'
        if 60<=speed<120:
            if delta >= 4:
                return 'IE1'
            elif delta >= 1:
                return 'IE2'
            elif delta >= -8:
                return 'IE3'
            else:
                return '输入参数错误或者未达到IE3'
        if 120<=speed<210:
            return 'IE3'
        if 210<=speed<300:
            if delta >= 3:
                return 'IE1'
            elif delta >= 1:
                return 'IE2'
            elif delta >= -9:
                return 'IE3'
            else:
                return '输入参数错误或者未达到IE3'
    elif flowrate>300:
        if 20<=speed<60:
            if delta>=11:
                return 'IE1'
            elif delta>=5:
                return 'IE2'
            elif delta>=-5:
                return 'IE3'
            else:return '输入参数错误或者未达到IE3'
        if 60<=speed<120:
            if delta >= 5:
                return 'IE1'
            elif delta >= 1:
                return 'IE2'
            elif delta >= -8:
                return 'IE3'
            else:
                return '输入参数错误或者未达到IE3'
        if 120<=speed<210:
            return 'IE3'
        if 210<=speed<300:
            if delta >= 3:
                return 'IE1'
            elif delta >= 2:
                return 'IE2'
            elif delta >= -7:
                return 'IE3'
            else:
                return '输入参数错误或者未达到IE3'

# 获得离心泵计算参数表的参数
@app.route('/get_pump_calculation', methods=['POST'])
def get_pump_calculation():
    try:
        # 从请求中获取参数
        data = request.get_json()
        print(f'Received JSON data: {data}')

        pump_type = data['type']
        density = data['density']
        flowrate = data['flowrate']
        waterlift = data['waterlift']
        powerin=data['powerin']
        speedn=data['speedn']


        # 计算泵效率
        pump_efficiency = (density * 9.8 * flowrate * waterlift * 1e-3) / powerin
        # 计算比转速
        specific_speed=(speedn * 3.65 * math.sqrt(flowrate)) / (waterlift ** 0.75)

        # 判断能效等级
        energy_efficiency_rating = get_energy_efficiency_rating(pump_efficiency, flowrate, specific_speed,delta=2)

        # 返回 JSON 格式的结果
        result = {
            'pump_type': pump_type,
            'density': density,
            'flowrate': flowrate,
            'waterlift': waterlift,
            'powerin': powerin,
            'pump_efficiency': pump_efficiency,
            'energy_efficiency_rating':energy_efficiency_rating
        }

        return jsonify(result)

    except Exception as e:
        return f'Database connection error: {str(e)}'



# 去除文本框中可能有的中文字符
def process_text(text):
    # 使用正则表达式匹配中文字符，并将其替换为空字符串
    processed_text = re.sub(r'[\u4e00-\u9fa5]', '', text)
    return processed_text


# 根据型号判断能效，这里暂时不考虑功率影响，对应能效都是我在网上查到的
def determine_energy_efficiency(processed_text):
    if "YE3-160M1-2" in processed_text:
        return "IE3", False
    elif "YE2-355M-8" in processed_text:
        return "IE2", False
    elif "SCB10-1250" in processed_text:
        return "落后产品，不计算能效", True
    elif "ZT250VSD-10.4GHN 380/50" in processed_text:
        return "IE1", False
    elif "YE3-315M-2" in processed_text:
        return "IE3", False
    elif "YE3-355L-6" in processed_text:
        return "IE3", False
    else:
        return "未知", "未知"


@app.route('/ocr', methods=['POST'])
def ocr() -> Dict[str, Any]:
    file = request.files['image']
    img_bytes = file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    res = OCR_MODEL.ocr(image)

    # 筛选包含 "功率" 或 "型号" 的结果
    filtered_results = [
        item for item in res if re.search(r"YE|ZT250|kw|KW|kW|Kw|SCB|250|型号|功率|TVF|TYPE", item.get("text", ""))
    ]

    # 修改结果格式，并处理文本内容
    for _one in filtered_results:
        _one['position'] = _one['position'].tolist()
        if 'cropped_img' in _one:
            _one.pop('cropped_img')
        # 处理文本内容，去掉中文字符
        _one['processed_text'] = process_text(_one['text'])

    # 返回给前端的数据
    print("Modified Results:", filtered_results)
    return jsonify(OcrResponse(results=filtered_results).dict())

@app.route('/energy_consumption', methods=['POST'])
def energy_consumption():
    try:
        # 获取OCR处理后的结果
        ocr_results = request.get_json().get('results', [])
        is_backward = True
    
        # 在这里使用OCR结果进行处理
        for result in ocr_results.get('results', []):
            if not isinstance(result, dict):
                print(f"Received unexpected result: {result}")
                continue

            processed_text = result.get('processed_text', '')
            
            # 在这里判断型号并设置能效
            if "YE3-160M1-2" in processed_text:
                energy_consumption = "IE3"
                is_backward = False
                return jsonify({"energy_consumption": energy_consumption, "is_backward": is_backward})
            elif "YE2-355M-8" in processed_text:
                energy_consumption = "IE2"
                is_backward = False
                return jsonify({"energy_consumption": energy_consumption, "is_backward": is_backward})
            elif "SCB10-1250" in processed_text:
                energy_consumption="落后产品，不计算能效"
                is_backward=True
                return jsonify({"energy_consumption": energy_consumption, "is_backward": is_backward})
            elif "ZT250VSD-10.4GHN 380/50" in processed_text:
                energy_consumption="X级"
                is_backward=False
                return jsonify({"energy_consumption": energy_consumption, "is_backward": is_backward})
            elif "YE3-315M-2" in processed_text:
                energy_consumption="IE3"
                is_backward=False
                return jsonify({"energy_consumption": energy_consumption, "is_backward": is_backward})
            elif "YE3-355L-6" in processed_text:
                energy_consumption="IE3"
                is_backward=False
                return jsonify({"energy_consumption": energy_consumption, "is_backward": is_backward})
            
        # 如果未找到匹配的结果，返回默认值
        return jsonify({"energy_consumption": "未知", "is_backward": "未知"})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500

# 手动输入的能效计算
@app.route('/handin_energy_consumption', methods=['POST'])
def handin_energy_consumption():
    try:
        # 获取前端传递的参数
        input_content1 = request.get_json().get('results', [])[0].get('processed_text1', '')
        input_content2 = request.get_json().get('results', [])[0].get('processed_text2', '')
        print(input_content1, input_content2)
        # 调用判断能效的函数,这里只用到了型号
        energy_consumption, is_backward = determine_energy_efficiency(f"{input_content1}")
        print(energy_consumption, is_backward)
        # 返回结果给前端
        return jsonify({"energy_consumption": energy_consumption, "is_backward": is_backward})
    except Exception as e:
        # 处理异常情况
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "An error occurred"}), 500



if __name__ == '__main__':
    app.run(debug=True)
