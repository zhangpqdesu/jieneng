import io
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
import math
import pymysql
import pandas as pd
import asyncio
from flask_cors import CORS
logger = set_logger(log_level='DEBUG')

OCR_MODEL = CnOcr()
app = Flask(__name__)
CORS(app, origins="http://localhost:8080")
#持久层框架，配置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Administrator:XWClassroom20202023@www.ylxteach.net:3366/demo?charset=gbk'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ocr返回类
class OcrResponse:
    def __init__(self, results: List[Dict[str, Any]]) -> None:
        self.results = results

    def dict(self) -> Dict[str, Any]:
        return {'results': self.results}




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
    for _one in res:
        _one['position'] = _one['position'].tolist()
        if 'cropped_img' in _one:
            _one.pop('cropped_img')

    text_array = [result["text"] for result in OcrResponse(results=res).dict()["results"]]
    print(text_array)
    # 提取包含 'kW' 或 'KW' 的文本框，并用正则表达式提取数字
    extracted_power = []
    extracted_efficiency = []
    extracted_rotated_speed = []
    for text in text_array:
        # 提取功率
        match_power = re.search(r'(\d+)\s*(?=-?\s*[kK][Ww])', text)

        if match_power:
            extracted_power.append(int(match_power.group(1)))
        elif 'kW' in text or 'KW' in text:
            # 尝试从前一个文本框中提取数字
            index = text_array.index(text)
            if index > 0:
                previous_text = text_array[index - 1]
                if previous_text.isdigit():
                    extracted_power.append(int(previous_text))

        # 提取效率
        match_efficiency = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
        if match_efficiency:
            extracted_efficiency.append(float(match_efficiency.group(1)))
        elif '%' in text:
            index = text_array.index(text)
            if index > 0:
                if 60<float(text_array[index - 1])<100:
                    extracted_efficiency.append(float(text_array[index - 1]))

        match_speed = re.search(r'(\d+(?:\.\d+)?)\s*[rR]/?\s*m\s*i\s*n', text)
        if match_speed:
            extracted_rotated_speed.append(float(match_speed.group(1)))
        elif 'rmin' in text.lower() or 'r/min' in text.lower() or 'rmir' in text.lower():
            index = text_array.index(text)
            if index > 0:
                extracted_rotated_speed.append(float(text_array[index - 1]))

    print("功率：", extracted_power)
    print("效率：", extracted_efficiency)
    print("转速：", extracted_rotated_speed)
    
    # 构建返回给前端的字典
    response_data = {
        "power": extracted_power,
        "efficiency": extracted_efficiency,
        "rotated_speed": extracted_rotated_speed
    }
    
    # 返回 JSON 响应
    return jsonify(response_data)



async def process_file(file):
    df = pd.read_excel(file)
    
    required_columns = ['转速', '效率', '额定功率']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    df['processed_data'] = df['转速'] + df['效率'] + df['额定功率']
    df['能效结果'] = ['合格' if value > 100 else '不合格' for value in df['processed_data']]
    
    return df


async def process_files(files):
    processed_files = []
    for file in files:
        processed_df = await process_file(file)
        processed_files.append(processed_df)
    return processed_files

@app.route('/upload', methods=['POST'])
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
        processed_filename = f"processed_{idx + 1}.xlsx"
        processed_df.to_excel(processed_filename, index=False)
        processed_filenames.append(processed_filename)
    
    # 返回处理后文件的下载链接
    download_links = [f"/download/{filename}" for filename in processed_filenames]
    return {'download_links': download_links}

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # 提供文件下载
    return send_file(filename, as_attachment=True)

class LiSi(db.Model):
    __tablename__ = '李四'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    type = db.Column(db.String(255))
    energy_consumption = db.Column(db.String(255))
    record_place = db.Column(db.String(255))
    record_time = db.Column(db.DateTime)


@app.route('/lisidata', methods=['GET'])
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
