from flask import Flask, request, send_file, send_from_directory, make_response
import pandas as pd
import os
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def process_file(file, filename):
    # 读取 Excel 文件
    df = pd.read_excel(file)
    
    # 检查文件是否包含所需的列
    required_columns = ['转速', '效率', '额定功率']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # 计算每行的结果并添加到新列
    df['结果'] = df['转速'] + df['效率'] + df['额定功率']
    
    # 打印文件内容
    print(f"File content for {filename}:")
    print(df)
    return df

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            return 'No selected file'
        
        # 调用 process_file 函数处理文件
        processed_df = process_file(file, file.filename)
        
        # 将处理后的数据转换为二进制流
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        processed_df.to_excel(writer, index=False)
        writer.save()
        output.seek(0)
        
        # 构建响应对象
        response = make_response(send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        response.headers['Content-Disposition'] = 'attachment; filename=processed_file.xlsx'
        return response

    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
