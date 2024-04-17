import io
import os
import waitress
from copy import deepcopy
from typing import List, Dict, Any
import re
from sqlalchemy import and_
from PIL import Image
from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from cnocr import CnOcr
from cnocr.utils import set_logger
from sqlalchemy import text
import pandas as pd
import asyncio
from flask_cors import CORS
import hashlib
from datetime import datetime

from ventilation_fan import finally_result, get_input_data
from Clearwater_centrifugal_pump import finally_result1
from Centrifugal_pump_for_petrochemical import final_result2
from small_submersible_electric_pump import get_input_data2, real_efficiency

logger = set_logger(log_level='DEBUG')

OCR_MODEL = CnOcr()  # 实例化对象
app = Flask(__name__)  # flask服务
CORS(app)
# 持久层框架，配置数据库连接信息，这里可以查看数据库配置信息

# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Administrator:XWClassroom20202023@www.ylxteach.net:3366/demo?charset=gbk'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)  #


app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Administrator:XWClassroom20202023@www.ylxteach.net:3366/demo?charset=gbk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 创建 SQLAlchemy 实例
db = SQLAlchemy()

# 将 Flask 应用注册到 SQLAlchemy 实例中
db.init_app(app)


# ocr返回类
# 以上都是固定的
@app.route('/')
def hello():
    return 'Hello, World! This is a test function.'


class OcrResponse:
    def __init__(self, results: List[Dict[str, Any]]) -> None:
        self.results = results

    def dict(self) -> Dict[str, Any]:
        return {'results': self.results}


def save_image_and_ocr(file):
    img_bytes = file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    upload_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"receiveImage/{upload_time}.jpg"
    os.makedirs("receiveImage", exist_ok=True)
    image.save(image_filename)

    res = OCR_MODEL.ocr(image)
    for _one in res:
        _one['position'] = _one['position'].tolist()
        if 'cropped_img' in _one:
            _one.pop('cropped_img')

    text_array = [result["text"] for result in OcrResponse(results=res).dict()["results"]]
    return text_array


def extract_motor_parameters(text_array):
    extracted_power = []
    extracted_efficiency = []
    extracted_rotated_speed = []
    extracted_motor_type = []

    for i, text in enumerate(text_array):
        # 匹配数字、小数点和字母"O"，在"O"的位置添加数字0
        match_power = re.search(r'(\d+\.*\d*)(O?)(?=\s*[kK][Ww])', text)
        if match_power:
            power_digits = match_power.group(1)
            power_letter_o = match_power.group(2)

            # 如果匹配到字母"O"，在其位置添加数字0
            if power_letter_o:
                o_index = match_power.start(2)
                power_digits = power_digits[:o_index] + '0' + power_digits[o_index:]

            # 将结果转换为浮点数
            extracted_power = float(power_digits)

            # 第二次提取，同样对结果进行处理
            extracted_power_second = float(match_power.group(1).replace('O', '0'))
            # 第二次提取，同样对结果进行处理
            extracted_power = float(extracted_power_second)

        if match_power:
            extracted_power = (float(extracted_power))
            break
        elif 'kw' in text.lower():
            # 检查当前带有 "kw" 的文本元素是否包含数字和字母
            if any(char.isdigit() or char.isalpha() for char in text):
                # 如果包含数字或字母，则直接提取当前文本元素中的功率信息
                match_power = re.search(r'(\d+\.*\d*)(O?)(?=\s*[kK][Ww])', text)
                if match_power:
                    power_digits = match_power.group(1)
                    power_letter_o = match_power.group(2)

                    # 如果匹配到字母"O"，在其位置添加数字0
                    if power_letter_o:
                        o_index = match_power.start(2)
                        power_digits = power_digits[:o_index] + '0' + power_digits[o_index:]

                    # 将结果转换为浮点数
                    extracted_power = float(power_digits)

                    # 第二次提取，同样对结果进行处理
                    extracted_power_second = float(match_power.group(1).replace('O', '0'))
                    # 第二次提取，同样对结果进行处理
                    extracted_power = float(extracted_power_second)

                if match_power:
                    extracted_power = float(extracted_power)
                    break
            else:
                # 如果不包含数字或字母，则回退到前一个文本元素中提取功率信息
                if i > 0:
                    previous_text = text_array[i - 1]
                    match_previous_power = re.search(r'(\d+\.*\d*)(O?)(?=\s*[kK][Ww])', previous_text)
                    if match_previous_power:
                        extracted_power = float(match_previous_power.group(1).replace('O', '0'))
                        break

    for text in text_array:
        match_efficiency = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
        if match_efficiency:
            extracted_efficiency = (match_efficiency.group(1))
            break
        elif '%' in text:
            index = text_array.index(text)
            if index > 0:
                if 60 < float(text_array[index - 1]) < 100:
                    extracted_efficiency = (text_array[index - 1])
                    break

    # 转速
    for text in text_array:
        match_speed = re.search(r'(\d+)\s*[rR]/min|rpm', text)
        if match_speed:
            extracted_rotated_speed = (match_speed.group(1))
            break
        elif 'rmin' in text.lower() or 'r/min' in text.lower() or 'rpm' in text.lower():
            index = text_array.index(text)
            if index > 0:
                extracted_rotated_speed = (text_array[index - 1])
                break

    found_motor_type = False  # 标志是否找到型号信息

    # 首先尝试匹配型号
    for text in text_array:
        match_motor_type = re.search(r'型号\s*[:：]?\s*([^：\s]+)', text)
        if match_motor_type:
            extracted_motor_type = match_motor_type.group(1)
            print("情况1：", extracted_motor_type)
            found_motor_type = True
            break

    if not found_motor_type:
        # 如果没有匹配到型号，尝试匹配type
        for i, text in enumerate(text_array):
            print("type",text_array)
            if 'type' in text.lower():
                next_index = i + 1
                if 0 <= next_index < len(text_array):
                    next_text = text_array[next_index]
                    # 检查 type 后面的内容是否合法
                    if re.search(r'^[^\s]+', next_text):
                        extracted_motor_type = next_text
                        print("情况2:", extracted_motor_type)
                        found_motor_type = True
                        break

    if not found_motor_type:
        print("No motor type found.")

    return extracted_power, extracted_efficiency, extracted_rotated_speed, extracted_motor_type


def extract_pump_parameters(text_array):
    extracted_speed = None
    extracted_flow_rate = None
    extracted_head = None
    extracted_model = None

    # 提取转速（单位为r/min）
    for i, text in enumerate(text_array):
        match_speed = re.search(r'(\d+)\s*[rR]/min', text)
        if match_speed:
            extracted_speed = match_speed.group(1)
            break
        elif 'r/min' in text.lower() or 'rmin' in text.lower() or 'rmir' in text.lower():
            if i > 0:
                previous_text = text_array[i - 1]

                extracted_speed = previous_text
                break

    # 提取流量（单位为m³/h）
    for text in text_array:
        match_flow_rate = re.search(r'(\d+)\s*[mM][3³]/h', text)
        if match_flow_rate:
            extracted_flow_rate = match_flow_rate.group(1)
            break
        elif 'm3/h' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]

                extracted_flow_rate = previous_text
                break

    # 提取扬程（单位为m）
    for text in text_array:
        match_head = re.search(r'(\d+)(?=\s*[mM]$)', text)
        if match_head:
            extracted_head = match_head.group(1)
            break
        elif text.lower() == 'm':
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                extracted_head = previous_text
                break

    # 提取型号
    for text in text_array:
        match_model = re.search(r'型号\s*[:：]?\s*([^：\s]+)', text)
        if match_model:
            extracted_model = match_model.group(1)
            print("情况1：", extracted_model)
            break
        elif '型号' in text or 'model' in text:
            index = text_array.index(text)
            if 0 <= index < len(text_array) - 1:
                extracted_model = text_array[index + 1]
                print("情况2", extracted_model)
                break

    return extracted_speed, extracted_flow_rate, extracted_head, extracted_model


import re


def extract_fan_parameters(text_array):
    extracted_speed = None
    extracted_flow_rate = None
    extracted_pressure = None
    extracted_power = None
    extracted_efficiency = None
    extracted_machine_number = None
    extracted_r = None
    extracted_type = None
    extracted_p1 = None
    extracted_u = None

    # 提取转速（单位为r/min）
    for i, text in enumerate(text_array):
        match_speed = re.search(r'(\d+)\s*[rR]/min', text)
        if match_speed:
            extracted_speed = match_speed.group(1)
            break
        elif 'r/min' in text.lower() or 'rmin' in text.lower() or 'rmir' in text.lower():
            if i > 0:
                previous_text = text_array[i - 1]
                extracted_speed = previous_text
                break

    # 提取流量（单位为m³/h）
    # 提取流量（单位为m³/h或m³/min）
    for text in text_array:
        # 匹配m³/h
        match_flow_rate_h = re.search(r'(\d+)\s*[mM][³3]/h', text)
        if match_flow_rate_h:
            extracted_flow_rate = match_flow_rate_h.group(1)
            break
        # 匹配m³/min
        match_flow_rate_min = re.search(r'(\d+)\s*[mM][3³`]/min', text)
        if match_flow_rate_min:
            extracted_flow_rate = match_flow_rate_min.group(1)
            break
        elif 'm3/h' in text.lower() or 'm`/min' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                extracted_flow_rate = previous_text
                break

    # 提取压力（单位为Mpa）
    for text in text_array:
        match_pressure = re.search(r'(\d+\.?\d*)\s*[Pp]a', text)
        if match_pressure:
            extracted_pressure = match_pressure.group(1)
            break
        elif 'pa' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                extracted_pressure = previous_text
                break

    # 提取功率（单位为kW）
    for text in text_array:
        match_power = re.search(r'(\d+\.?\d*)\s*[kK]w', text)
        if match_power:
            extracted_power = match_power.group(1)
            break
        elif 'kw' in text.lower() or 'kW' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]

                extracted_power = previous_text
                break

    # 提取效率（单位为%）
    for text in text_array:
        match_efficiency = re.search(r'(\d{1,3})\s*%', text)
        if match_efficiency:
            extracted_efficiency = match_efficiency.group(1)
            break
        elif '%' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                extracted_efficiency = previous_text
                break

    # 提取风机号
    for text in text_array:
        match_machine_number = re.search(r'NO(\d+)', text)
        if match_machine_number:
            extracted_machine_number = match_machine_number.group(1)
            break
        elif '%' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                extracted_machine_number = previous_text
                break

    # 提取轮毂比
    for text in text_array:
        match_r = re.search(r'轮毂比\s*[:：]?\s*(\d+(?:\.\d+)?)', text)
        if match_r:
            extracted_r = match_r.group(1)
            break
        elif '%' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                extracted_r = previous_text
                break

    # 提取型号
    for text in text_array:
        match_type = re.search(r'型号\s*[:：]?\s*([^：\s]+)', text)
        if match_type:
            extracted_type = match_type.group(1)
            break
        elif '%' in text.lower():
            index = text_array.index(text)
            if 0 <= index < len(text_array) - 1:
                extracted_type = text_array[index + 1]
                break

    # 提取密度
    for text in text_array:
        match_p1 = re.search(r'(\d+)\s*[mM][3³`]/s', text)
        if match_p1:
            extracted_p1 = match_p1.group(1)
            break
        elif 'm3/h' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                extracted_p1 = previous_text
                break

    # 提取圆周速度
    for text in text_array:
        match_u = re.search(r'(\d+)\s*[mM]/s', text)
        if match_u:
            extracted_u = match_u.group(1)
            break
        elif 'm3/h' in text.lower() or 'm`/min' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                extracted_u = previous_text
                break

    # 提取水泵级数
    for text in text_array:
        match_stage = re.search(r'/(?P<stage>\d)', text)
        if match_stage:
            extracted_stage = match_stage.group(1)
            break

    return extracted_speed, extracted_flow_rate, extracted_pressure, extracted_power, extracted_efficiency, extracted_machine_number, extracted_r, extracted_type, extracted_p1, extracted_u, extracted_stage


@app.route('/ocr', methods=['POST'])
def ocr() -> Dict[str, Any]:
    file = request.files['image']
    text_array = save_image_and_ocr(file)
    print(text_array)

    if any('三相异步' in text or '电动机' in text or 'motors' in text.lower() for text in text_array):
        # 电机相关的逻辑
        extracted_power, extracted_efficiency, extracted_rotated_speed, extracted_motor_type = extract_motor_parameters(
            text_array)
        typeIndex = 1
        print("typeIndex:", typeIndex)
        print("功率：", extracted_power)
        print("效率：", extracted_efficiency)
        print("转速：", extracted_rotated_speed)
        print("型号：", extracted_motor_type)

        response_data = {
            "power": extracted_power,
            "efficiency": extracted_efficiency,
            "rotated_speed": extracted_rotated_speed,
            "model": extracted_motor_type,
            "typeIndex": typeIndex
        }
        print(response_data)
        return jsonify(response_data)
    elif any('风机' in text for text in text_array):
        # 风机相关的逻辑
        extracted_machine_number, extracted_r, extracted_type, extracted_p1, extracted_u, extracted_speed, extracted_flow_rate, extracted_pressure, extracted_power, extracted_efficiency = extract_fan_parameters(
            text_array)
        typeIndex = 0
        print("typeIndex:", typeIndex)
        print("机号：", extracted_machine_number, "")
        print("轮毂比：", extracted_r, "")
        print("型号：", extracted_type, "")
        print("压力：", extracted_pressure, "pa")
        print("密度：", extracted_p1, "m³/s")
        print("速度：", extracted_u, "m/s")
        print("转速：", extracted_speed, "r/min")
        print("流量：", extracted_flow_rate, "m³/h")
        print("功率：", extracted_power, "kW")
        print("效率：", extracted_efficiency)

        response_data = {
            "typeIndex": typeIndex,
            "machine_number": extracted_machine_number,  # 机号
            "r": extracted_r,  # 轮毂比
            "type": extracted_type,  # 型号
            "p1": extracted_p1,  # 密度
            "u": extracted_u,  # 圆周速度
            "rotated_speed": extracted_speed,  # 转速
            "flowRate": extracted_flow_rate,  # 流量
            "pressure": extracted_pressure,  # 压力
            "power": extracted_power,  # 功率
            "efficiency": extracted_efficiency  # 效率
        }
        return jsonify(response_data)


    elif ('泵' in text for text in text_array):
        extracted_speed, extracted_flow_rate, extracted_head, extracted_model = extract_pump_parameters(
            text_array)
        typeIndex = 2
        print("typeIndex:", typeIndex)
        print("转速：", extracted_speed, "r/min")
        print("流量：", extracted_flow_rate, "m³/h")
        print("扬程：", extracted_head, "m")
        print("型号：", extracted_model)
        

        response_data = {
            "typeIndex": typeIndex,
            "rotated_speed": extracted_speed,  # 转速
            "flowRate": extracted_flow_rate,  # 流量
            "head": extracted_head,  # 扬程
            "model": extracted_model,  # 型号
            
        }
        return jsonify(response_data)
    response_data = {
        "typeIndex": 0,
    }
    return response_data


class backward_devices(db.Model):
    __tablename__ = '落后设备'

    name = db.Column(db.String(50), primary_key=True)
    batch = db.Column(db.String(50))


@app.route('/is_backward', methods=['POST'])
def is_backward():
    data = request.json
    print('Received data in is_backward:', data)
    # 查询数据库中所有的落后设备记录
    backward_devices_list = backward_devices.query.all()

    # 初始化结果列表
    results = []
    is_backward = "不是落后设备"
    batch = "无"

    for device in backward_devices_list:
        # 检查设备名中是否包含中文字符
        contains_chinese = re.search(r'[\u4e00-\u9fff]+', device.name)

        # 如果设备名包含中文字符，则直接比对
        if contains_chinese:
            if data['model'] is not None and device.name == data['model'].strip():
                # 将is_backward设为"是落后设备"
                is_backward = "是落后设备"
                # 返回设备名和对应的batch属性
                batch = device.batch
        # 如果设备名没有中文字符，则转换为小写后比对
        else:
            if data['model'] is not None and device.name.lower() == data['model'].lower().strip():
                # 将is_backward设为"是落后设备"
                is_backward = "是落后设备"
                # 返回设备名和对应的batch属性
                batch = device.batch

    print(is_backward, batch)
    return jsonify({'is_backward': is_backward, 'batch': batch})


async def process_file(file):  # 文件处理功能，等待能效计算函数中
    df = pd.read_excel(file)

    required_columns = ['转速', '效率', '额定功率']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df['processed_data'] = df['转速'] + df['效率'] + df['额定功率']
    df['能效结果'] = ['合格' if value > 100 else '不合格' for value in df['processed_data']]

    return df


async def process_files(files):  # 文件处理功能，等待能效计算函数中
    processed_files = []
    for file in files:
        processed_df = await process_file(file)
        processed_files.append(processed_df)
    return processed_files


@app.route('/upload', methods=['POST'])  # 上传多个文件的函数，调用上面的两个处理文件的函数并返回给前端下载
def upload_files():
    uploaded_files = request.files.getlist('files[]')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        processed_files = loop.run_until_complete(process_files(uploaded_files))
    except Exception as e:
        return {'error': str(e)}, 500  # 返回包含错误信息的响应，状态码为500表示服务器内部错误
    finally:
        loop.close()

    processed_filenames = []
    for idx, processed_df in enumerate(processed_files):
        processed_filename = f"处理文件{idx + 1}.xlsx"
        processed_df.to_excel(processed_filename, index=False)
        processed_filenames.append(processed_filename)

    # 返回处理后文件的下载链接
    download_links = [f"/download/{filename}" for filename in processed_filenames]
    return {'download_links': download_links}


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # 提供文件下载
    return send_file(filename, as_attachment=True)


class User(db.Model):  # 用户表
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    workplace = db.Column(db.String(120), nullable=False)
    identity = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)


def hash_password(password):  # md5加密密码
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


@app.route('/register', methods=['POST'])  # 注册功能
def register():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    workplace = data.get('workplace')
    identity = data.get('identity')
    raw_password = data.get('password')
    # , phone, workplace, identity,
    if not all([name, raw_password]):
        return jsonify({'error': '缺少必填字段'}), 400

    # md5密码加密
    hashed_password = hash_password(raw_password)

    # 创建用户对象
    new_user = User(name=name, phone=phone, workplace=workplace, identity=identity, password=hashed_password)

    # 将用户对象添加到数据库会话中
    db.session.add(new_user)

    # 提交会话以将用户添加到数据库
    db.session.commit()

    return jsonify({'message': '注册成功'})


@app.route('/login', methods=['POST'])  # 登录功能
def login():
    data = request.json

    name = data.get('name')
    raw_password = data.get('password')

    if not all([name, raw_password]):
        return jsonify({'error': '缺少必填字段'}), 400

    # md5密码加密
    hashed_password = hash_password(raw_password)

    # 查询数据库中是否存在匹配的用户记录
    user = User.query.filter_by(name=name, password=hashed_password).first()

    if user:
        return jsonify({'message': '登录成功'})
    else:
        return jsonify({'error': '姓名或密码错误'}), 401


class UserPhoto(db.Model):
    __tablename__ = 'user_photos'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), default=None)
    type = db.Column(db.String(255), default=None)
    energy_consumption = db.Column(db.String(255), default=None)
    record_place = db.Column(db.String(255), default=None)
    record_time = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    is_backward = db.Column(db.String(255), default=None)
    extra_info = db.Column(db.String(255), default=None)


@app.route('/listdata', methods=['GET'])
def list_user_photos():
    # 获取前端传递的用户名参数
    username = request.args.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    # 查询该用户名对应的所有user_photos记录
    user_photos = UserPhoto.query.filter_by(username=username).all()
    print("user数据：")
    for photo in user_photos:
        print("id:", photo.id)
        print("url:", photo.url)
        print("record_place:", photo.record_place)
        print("type:", photo.type)
        print("energy_consumption:", photo.energy_consumption)
        print("record_time:", photo.record_time)
        print("is_backward:", photo.is_backward)
        print("extra_info", photo.extra_info)
    # 将查询到的数据转换为适合前端的格式
    photos_data = [{
        'id': photo.id,
        'url': photo.url,
        'record_place': photo.record_place,
        'type': photo.type,
        'is_backward': photo.is_backward,
        "extra_info": photo.extra_info,
        'energy_consumption': photo.energy_consumption,
        'record_time': photo.record_time.strftime('%Y-%m-%d %H:%M:%S') if photo.record_time else None
    } for photo in user_photos]

    return jsonify({'data': photos_data})


@app.route('/save_photo_data', methods=['POST'])
def save_photo_data():
    data = request.json
    photo = UserPhoto(
        username=data.get('username'),
        url=data.get('imgUrl'),
        type=data.get('type'),  # 根据你的业务逻辑提供类型
        energy_consumption=data.get('energy_consumption'),  # 你可能需要调整字段名称和数据来源
        record_place=data.get('record_place'),  # 根据你的业务逻辑提供记录地点
        is_backward=data.get('is_backward'),  # 你可能需要计算 is_backward 或者从前端传递
        extra_info=data.get('extraInfo')
    )
    db.session.add(photo)
    db.session.commit()

    # 返回存储成功的提示或者其他数据
    return jsonify({'message': 'Photo data stored successfully'})


class MotorFile(db.Model):
    __tablename__ = 'triple_motor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    power = db.Column(db.Float(precision=2))
    efficiency = db.Column(db.Float(precision=2))
    rotate_speed = db.Column(db.Integer)
    energy_consumption = db.Column(db.String(255))


# 电机
@app.route('/query_motor_files', methods=['GET'])
def query_motor_files():
    rotated_speed = request.args.get('rotated_speed', type=int)
    power = request.args.get('power', type=float)
    efficiency = request.args.get('efficiency', type=float)
    print("转速:", rotated_speed)
    # 查询请求的功率是否在数据库中有记录
    existing_record = MotorFile.query.filter_by(power=power).first()
    if not existing_record:
        # 如果请求的功率不在数据库中有记录，则找到比该功率小的最近一条记录，并将请求的功率用这个值代替
        below_power = MotorFile.query.filter(MotorFile.power < power).order_by(MotorFile.power.desc()).first()
        if below_power:
            power = below_power.power

    # 按照之前的逻辑进行查询

    if rotated_speed is None or rotated_speed >= 0:
        result = MotorFile.query.filter(and_(MotorFile.power == power, efficiency >= MotorFile.efficiency)) \
            .order_by(MotorFile.efficiency.desc()).first()

    if rotated_speed is None or rotated_speed == 0:
        result = MotorFile.query.filter(and_(MotorFile.power == power, efficiency >= MotorFile.efficiency)) \
            .order_by(MotorFile.efficiency.desc()).first()

        if result:
            energy_consumption = result.energy_consumption
            return jsonify({'energy_consumption': energy_consumption})
    elif 1300 >= rotated_speed > 0:
        result = MotorFile.query.filter(
            and_(MotorFile.power == power, efficiency >= MotorFile.efficiency, rotated_speed <= MotorFile.rotate_speed)
        ).order_by(MotorFile.rotate_speed.asc(), MotorFile.efficiency.desc()).first()
        if result:
            energy_consumption = result.energy_consumption
            return jsonify({'energy_consumption': energy_consumption})
    elif rotated_speed > 1300:
        rotated_speed = 1301
        result = MotorFile.query.filter(
            and_(MotorFile.power == power, efficiency >= MotorFile.efficiency, rotated_speed <= MotorFile.rotate_speed)
        ).order_by(MotorFile.rotate_speed.asc(), MotorFile.efficiency.desc()).first()

        if result:
            energy_consumption = result.energy_consumption
            return jsonify({'energy_consumption': energy_consumption})
    return jsonify({'energy_consumption': '低于3级'})


# 风机
@app.route('/ventilation_fan', methods=['GET'])
def ventilation_fan():
    MachineNumber = float(request.args.get('machine_number')) if request.args.get('machine_number') else None
    r = float(request.args.get('r')) if request.args.get('r') else None
    type = str(request.args.get('type')) if request.args.get('type') else None
    Pf = float(request.args.get('pressure')) if request.args.get('pressure') else None
    p1 = float(request.args.get('p1')) if request.args.get('p1') else None
    u = float(request.args.get('u')) if request.args.get('u') else None
    n = int(request.args.get('rotated_speed')) if request.args.get('rotated_speed') else None
    q = float(request.args.get('flowRate')) if request.args.get('flowRate') else None
    pr = float(request.args.get('power')) if request.args.get('power') else None
    pe = float(request.args.get('power')) if request.args.get('power') else None
    Nm = float(request.args.get('efficiency')) if request.args.get('efficiency') else None

    get_input_data(MachineNumber, r, type, Pf, p1, u, n, q, pr, pe, Nm)

    grade = finally_result(MachineNumber, r, type, Pf, p1, u, n, q, pr, pe, Nm)
    print("风机能效等级", grade)
    return jsonify({'energy_consumption': grade})


# 水泵
@app.route('/water_pump', methods=['GET'])
def water_pump():
    Rho = float(request.args.get('P1')) if request.args.get('P1') else None
    n = float(request.args.get('rotated_speed')) if request.args.get('rotated_speed') else None
    Q = float(request.args.get('flowRate')) if request.args.get('flowRate') else None
    H = float(request.args.get('head')) if request.args.get('head') else None
    P = float(request.args.get('power')) if request.args.get('power') else None
    Type = str(request.args.get('model')) if request.args.get('model') else None
    stage = int(request.args.get('stage')) if request.args.get('stage') else None
    Efficiency = float(request.args.get('efficiency')) if request.args.get('efficiency') else None

    if '清水' in Type:
        pump1 = finally_result1(Rho, n, Q, H, P, Type, Efficiency)
        print("水泵1", pump1)
        return jsonify({'energy_consumption': pump1})
    elif '石油' in Type or '化工' in Type:
        pump2 = final_result2(n, Q, H, P, Rho, Type, Efficiency)
        print("水泵2", pump2)
        return jsonify({'energy_consumption': pump2})
    elif '小型潜水' in Type:
        get_input_data2(n, Q, H, stage, P, Type, Efficiency)
        pump3 = real_efficiency(n, Q, H, stage, P, Type, Efficiency)
        print("水泵3", pump3)
        return jsonify({'energy_consumption': pump3})


if __name__ == '__main__':
    waitress.serve(app, host='127.0.0.1', port=5000)
