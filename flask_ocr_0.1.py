import io
import os
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
#ocr函数
@app.route('/ocr', methods=['POST'])
def ocr() -> Dict[str, Any]:
    file = request.files['image']
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

#以上功能：将文件存到receiveImage目录下，并调用ocr函数进行文字识别
    text_array = [result["text"] for result in OcrResponse(results=res).dict()["results"]]#基于ocr服务返回的原始格式修改，提取出所有文字，并整理为数组
    print(text_array)
    
    # 提取电机功率（这里需要添加判断逻辑，根据水泵、电机、风机的类型不同，编写不同的正则表达式进行参数提取，目前只写了电机的）
    extracted_power = []
    for text in text_array:
        match_power = re.search(r'(\d+)\s*(?=-?\s*[kK][Ww])', text)#情况1：参数与单位在统一文本框中
        #具体来说，它查找一个或多个数字字符（\d+），后面可能跟着零个或多个空格（\s*），然后是一个可选的负号（-?），再后面是零个或多个空格（\s*），
        # 最后是一个表示功率单位的字符串（[kK][Ww]）。这个正则表达式使用了非捕获组（(?:)）来匹配负号和空格，以避免将它们包含在最终的匹配结果中。
        if match_power:
            extracted_power.append(int(match_power.group(1)))
            break
        elif 'kW' in text or 'KW' in text:#情况2：参数值与单位中间分隔部分太大，被识别为两个文本框
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                if previous_text.isdigit():
                    extracted_power.append(int(previous_text))
                    break
    
    # 提取效率
    extracted_efficiency = []
    for text in text_array:
        match_efficiency = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
        #这段代码使用正则表达式从文本中提取效率值。具体来说，它查找一个或多个数字字符（\d+），后面可能跟着一个小数点和一个或多个数字字符（.\d+），
        # 然后是一个可选的百分号（%）。这个正则表达式使用了非捕获组（(?:)）来匹配小数点和百分号，以避免将它们包含在最终的匹配结果中。
        if match_efficiency:
            extracted_efficiency.append(match_efficiency.group(1))#情况1
            break
        elif '%' in text:#情况2
            index = text_array.index(text)
            if index > 0:
                if 60 < float(text_array[index - 1]) < 100:
                    extracted_efficiency.append(text_array[index - 1])
                    break
    
    # 提取转速
    extracted_rotated_speed = []
    for text in text_array:
        match_speed = re.search(r'(\d+(?:\.\d+)?)\s*[rR]\s*m\s*i\s*n', text)
        if match_speed:
            extracted_rotated_speed.append(match_speed.group(1))#情况1
            #具体来说，它查找一个或多个数字字符（\d+），后面可能跟着一个小数点和一个或多个数字字符（.\d+），然后是一个表示速度单位的字符串（[rR] m i n）
            # 这个正则表达式使用了非捕获组（(?:)）来匹配小数点和速度单位，以避免将它们包含在最终的匹配结果中。
            break
        elif 'rmin' in text.lower() or 'r/min' in text.lower() or 'rmir' in text.lower():#情况2
            index = text_array.index(text)
            if index > 0:
                extracted_rotated_speed.append(text_array[index - 1])
                break
    
    # 提取电机型号
    extracted_motor_type = []
    for text in text_array:
        match_motor_type = re.search(r'型号\s*[:：]?\s*([^：\s]+)', text)#情况1
        #具体来说，它查找一个字符串“型号”，后面可能跟着一个冒号（：）或中文冒号（：），然后是一个或多个非空白字符（[^：\s]+）
        # 这个正则表达式使用了非捕获组（(?:)）来匹配冒号和空格，以避免将它们包含在最终的匹配结果中。
        if match_motor_type:
            extracted_motor_type = match_motor_type.group(1)
            print("情况1：", extracted_motor_type)
            break
        elif '型号' in text or 'type' in text:#情况2
            index = text_array.index(text)
            if 0 <= index < len(text_array) - 1:
                extracted_motor_type = text_array[index + 1]
                print("情况2", extracted_motor_type)
                break
    
    print("功率：", extracted_power)
    print("效率：", extracted_efficiency)
    print("转速：", extracted_rotated_speed)
    print("型号：", extracted_motor_type)
    
    # 构建返回给前端的字典
    response_data = {
        "power": extracted_power,
        "efficiency": extracted_efficiency,
        "rotated_speed": extracted_rotated_speed,
        "motor_type": extracted_motor_type
    }
    
    # 返回 JSON 响应
    return jsonify(response_data)

class backward_devices(db.Model):
    __tablename__ = '落后设备'

    name = db.Column(db.String(50), primary_key=True)
    batch = db.Column(db.String(50))

from flask import jsonify

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
        # 如果设备名在data['motor_type']中（无视大小写）但如何处理有中文的设备？待修正
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

class LiSi(db.Model):#持久层框架样例，用于显示某用户的所有拍摄记录
    __tablename__ = '李四'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    type = db.Column(db.String(255))
    energy_consumption = db.Column(db.String(255))
    record_place = db.Column(db.String(255))
    record_time = db.Column(db.DateTime)

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

@app.route('/lisidata', methods=['GET'])#获取李四的历史拍摄数据
def get_lisi_data():
    lisi_data = LiSi.query.all()
    lisi_json = []
    for data in lisi_data:
        lisi_json.append({
            'id': data.id,
            'url': data.url,
            'type': data.type,
            'energy_consumption': data.energy_consumption,
            'record_place': data.record_place,
            'record_time': data.record_time.strftime('%Y-%m-%d %H:%M:%S') if data.record_time else None
        })
    return jsonify(lisi_json)

if __name__ == '__main__':
    app.run(debug=True)
