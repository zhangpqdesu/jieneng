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
