from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # 保存上传的文件
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # 在实际应用中，你可能需要进行一些额外的处理，例如保存文件路径到数据库，生成缩略图等

        return jsonify({'message': 'File successfully uploaded', 'filename': file.filename})
    else:
        return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(debug=True)
