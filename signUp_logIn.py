from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 跨域问题
from flask import Flask, jsonify
from flask_cors import CORS

import hashlib

app = Flask(__name__)

# 跨域问题
CORS(app, origins="http://192.168.43.64:8080", supports_credentials=True, methods=["OPTIONS", "POST"])



engine = create_engine('mysql+pymysql://root:Zhang0080@localhost/MingPai', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    phone = Column(String(15), nullable=False)
    workplace = Column(String(120), nullable=False)
    identity = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def hash_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

@app.route('/register', methods=['POST'])
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

    session = Session()
    new_user = User(name=name, phone=phone, workplace=workplace, identity=identity, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.close()

    return jsonify({'message': '注册成功'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    name = data.get('name')
    raw_password = data.get('password')

    if not all([name, raw_password]):
        return jsonify({'error': '缺少必填字段'}), 400

    # md5密码加密
    hashed_password = hash_password(raw_password)

    session = Session()
    user = session.query(User).filter_by(name=name, password=hashed_password).first()
    session.close()

    if user:
        return jsonify({'message': '登录成功'})
    else:
        return jsonify({'error': '姓名或密码错误'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='192.168.43.64', port=8080)

