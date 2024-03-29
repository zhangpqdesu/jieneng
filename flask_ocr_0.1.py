import io
import os
import waitress
from copy import deepcopy
from typing import List, Dict, Any
import re
from pydantic import BaseModel
from PIL import Image
from flask import Flask, jsonify, request,send_file
from flask_sqlalchemy import SQLAlchemy
from cnocr import CnOcr
from cnocr.utils import set_logger
from sqlalchemy import text
import pandas as pd
import asyncio
from flask_cors import CORS
import hashlib
from datetime import datetime
logger = set_logger(log_level='DEBUG')

OCR_MODEL = CnOcr()#实例化对象
app = Flask(__name__)#flask服务
CORS(app, origins="http://localhost:8080")
#持久层框架，配置数据库连接信息，这里可以查看数据库配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Administrator:XWClassroom20202023@www.ylxteach.net:3366/demo?charset=gbk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)#

# ocr返回类
#以上都是固定的
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

    for text in text_array:
        match_power = re.search(r'(\d+)\s*(?=-?\s*[kK][Ww])', text)
        
        if match_power:
            extracted_power=(int(match_power.group(1)))
            break
        elif 'kW' in text or 'KW' in text:
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                if previous_text.isdigit():
                    extracted_power=(int(previous_text))
                    break

    for text in text_array:
        match_efficiency = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
        if match_efficiency:
            extracted_efficiency=(match_efficiency.group(1))
            break
        elif '%' in text:
            index = text_array.index(text)
            if index > 0:
                if 60 < float(text_array[index - 1]) < 100:
                    extracted_efficiency=(text_array[index - 1])
                    break

    for text in text_array:
        match_speed = re.search( r'(\d+)\s*[rR]/min', text)
        if match_speed:
            extracted_rotated_speed=(match_speed.group(1))
            break
        elif 'rmin' in text.lower() or 'r/min' in text.lower() or 'rmir' in text.lower():
            index = text_array.index(text)
            if index > 0:
                extracted_rotated_speed=(text_array[index - 1])
                break

    for text in text_array:
        match_motor_type = re.search(r'型号\s*[:：]?\s*([^：\s]+)', text)
        if match_motor_type:
            extracted_motor_type = match_motor_type.group(1)
            print("情况1：", extracted_motor_type)
            break
        elif '型号' in text or 'type' in text:
            index = text_array.index(text)
            if 0 <= index < len(text_array) - 1:
                extracted_motor_type = text_array[index + 1]
                print("情况2", extracted_motor_type)
                break

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
                # if previous_text.isdigit():
                extracted_speed = previous_text
                break

    # 提取流量（单位为m³/h）
    for text in text_array:
        match_flow_rate = re.search(r'(\d+)\s*[mM]³/h', text)
        if match_flow_rate:
            extracted_flow_rate = match_flow_rate.group(1)
            break
        elif 'm3/h' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                if previous_text.isdigit():
                    extracted_flow_rate = previous_text
                    break

    # 提取扬程（单位为m）
    for text in text_array:
        match_head = re.search(r'(\d+)(?=\s*[mM]$)', text)
        if match_head:
            extracted_head = match_head.group(1)
            break
        elif text.lower()=='m':
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                if previous_text.isdigit():
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

import re

def extract_fan_parameters(text_array):
    extracted_speed = None
    extracted_flow_rate = None
    extracted_pressure = None
    extracted_power = None
    extracted_efficiency = None

    # 提取转速（单位为r/min）
    for i, text in enumerate(text_array):
        match_speed = re.search(r'(\d+)\s*[rR]/min', text)
        if match_speed:
            extracted_speed = match_speed.group(1)
            break
        elif 'r/min' in text.lower() or 'rmin' in text.lower() or 'rmir' in text.lower():
            if i > 0:
                previous_text = text_array[i - 1]
                if previous_text.isdigit():
                    extracted_speed = previous_text
                    break

    # 提取流量（单位为m³/h）
    # 提取流量（单位为m³/h或m³/min）
    for text in text_array:
        # 匹配m³/h
        match_flow_rate_h = re.search(r'(\d+)\s*[mM]³/h', text)
        if match_flow_rate_h:
            extracted_flow_rate = match_flow_rate_h.group(1)
            break
        # 匹配m³/min
        match_flow_rate_min = re.search(r'(\d+)\s*[mM]³/min', text)
        if match_flow_rate_min:
            extracted_flow_rate = match_flow_rate_min.group(1)
            break
        elif 'm3/h' in text.lower() or 'm3/min' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                if previous_text.isdigit():
                    extracted_flow_rate = previous_text
                    break

    # 提取压力（单位为Mpa）
    for text in text_array:
        match_pressure = re.search(r'(\d+\.?\d*)\s*[Mm]pa', text)
        if match_pressure:
            extracted_pressure = match_pressure.group(1)
            break
        elif '[Mm]pa' in text.lower():
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                if previous_text.isdigit():
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
                if previous_text.isdigit():
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
                if previous_text.isdigit():
                    extracted_efficiency = previous_text
                    break

    return extracted_speed, extracted_flow_rate, extracted_pressure, extracted_power, extracted_efficiency


@app.route('/ocr', methods=['POST'])
def ocr() -> Dict[str, Any]:
    file = request.files['image']
    text_array = save_image_and_ocr(file)
    print(text_array)
    
    if any('三相异步' in text or '电动机' in text for text in text_array):
    # 电机相关的逻辑
        extracted_power, extracted_efficiency, extracted_rotated_speed, extracted_motor_type = extract_motor_parameters(text_array)
        typeIndex=1
        print("typeIndex:",typeIndex)
        print("功率：", extracted_power)
        print("效率：", extracted_efficiency)
        print("转速：", extracted_rotated_speed)
        print("型号：", extracted_motor_type)
        
        response_data = {
            "power": extracted_power,
            "efficiency": extracted_efficiency,
            "rotated_speed": extracted_rotated_speed,
            "motor_type": extracted_motor_type,
            "typeIndex":typeIndex
        }
        print(response_data)
        return jsonify(response_data)
    elif any('空压机' in text for text in text_array):
        # 风机相关的逻辑
        typeIndex = 0
        print("typeIndex:", typeIndex)
        extracted_speed, extracted_flow_rate, extracted_pressure, extracted_power, extracted_efficiency = extract_fan_parameters(text_array)
        print("转速：", extracted_speed, "r/min")
        print("流量：", extracted_flow_rate, "m³/h")
        print("压力：", extracted_pressure, "Mpa")
        print("功率：", extracted_power, "kW")
        print("效率：", extracted_efficiency)
        
        response_data = {
            "typeIndex": typeIndex,
            "rotated_speed": extracted_speed,  # 转速
            "flowRate": extracted_flow_rate,  # 流量
            "pressure": extracted_pressure,  # 压力
            "power": extracted_power,  # 功率
            "efficiency": extracted_efficiency  # 效率
        }
        return jsonify(response_data)
        
        
    elif ('泵' in text for text in text_array):
        typeIndex=2
        print("typeIndex:",typeIndex)
        extracted_speed, extracted_flow_rate, extracted_head, extracted_model = extract_pump_parameters(text_array)
        print("转速：", extracted_speed, "r/min")
        print("流量：", extracted_flow_rate, "m³/h")
        print("扬程：", extracted_head, "m")
        print("型号：", extracted_model)
        
        response_data = {
        "typeIndex": typeIndex,
        "rotated_speed": extracted_speed,  # 转速
        "flowRate": extracted_flow_rate,  # 流量
        "head": extracted_head,  # 扬程
        "model": extracted_model  # 型号
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
    print('Received data:', data)
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
            if device.name in data['motor_type']:
                # 将is_backward设为"是落后设备"
                is_backward = "是落后设备"
                # 返回设备名和对应的batch属性
                batch = device.batch
        # 如果设备名没有中文字符，则转换为小写后比对
        else:
            if device.name.lower() in data['motor_type'].lower():
                # 将is_backward设为"是落后设备"
                is_backward = "是落后设备"
                # 返回设备名和对应的batch属性
                batch = device.batch

    print(is_backward, batch)
    return jsonify({'is_backward': is_backward, 'batch': batch})

async def process_file(file):#文件处理功能，等待能效计算函数中
    df = pd.read_excel(file)
    
    required_columns = ['转速', '效率', '额定功率']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    df['processed_data'] = df['转速'] + df['效率'] + df['额定功率']
    df['能效结果'] = ['合格' if value > 100 else '不合格' for value in df['processed_data']]
    
    return df


async def process_files(files):#文件处理功能，等待能效计算函数中
    processed_files = []
    for file in files:
        processed_df = await process_file(file)
        processed_files.append(processed_df)
    return processed_files

@app.route('/upload', methods=['POST'])#上传多个文件的函数，调用上面的两个处理文件的函数并返回给前端下载
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

class User(db.Model):#用户表
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    workplace = db.Column(db.String(120), nullable=False)
    identity = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

def hash_password(password):#md5加密密码
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()
@app.route('/register', methods=['POST'])#注册功能
def register():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    workplace = data.get('workplace')
    identity = data.get('identity')
    raw_password = data.get('password')

    if not all([name, phone, workplace, identity, raw_password]):
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

@app.route('/login', methods=['POST'])#登录功能
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
    record_time = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_backward= db.Column(db.String(255), default=None)
    extra_info=db.Column(db.String(255),default=None)
    
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
        print("url:",photo.url)
        print("record_place:", photo.record_place)
        print("type:", photo.type)
        print("energy_consumption:", photo.energy_consumption)
        print("record_time:", photo.record_time)
        print("is_backward:",photo.is_backward)
        print("extra_info",photo.extra_info)
    # 将查询到的数据转换为适合前端的格式
    photos_data = [{
        'id': photo.id,
        'url':photo.url,
        'record_place': photo.record_place,
        'type': photo.type,
        'is_backward':photo.is_backward,
        "extra_info":photo.extra_info,
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
        energy_consumption=data.get('efficiency'),  # 你可能需要调整字段名称和数据来源
        record_place=data.get('record_place'),  # 根据你的业务逻辑提供记录地点
        is_backward=data.get('is_backward'),  # 你可能需要计算 is_backward 或者从前端传递
        extra_info=data.get('extraInfo')
    )
    db.session.add(photo)
    db.session.commit()
    
    # 返回存储成功的提示或者其他数据
    return jsonify({'message': 'Photo data stored successfully'})


if __name__ == '__main__':
    waitress.serve(app, host='127.0.0.1', port=5000)
