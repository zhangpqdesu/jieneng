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
