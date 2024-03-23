from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import and_
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Administrator:XWClassroom20202023@www.ylxteach.net:3366/demo?charset=gbk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MotorFile(db.Model):
    __tablename__ = 'motor_files'

    id = db.Column(db.Integer, primary_key=True)
    motor_type = db.Column(db.String(255))
    efficiency = db.Column(db.Float)
    power = db.Column(db.Float)
    rotate_speed = db.Column(db.Integer)
    energy_consumption = db.Column(db.String(255))

@app.route('/query', methods=['GET'])
def query_motor_files():
    motor_type = request.args.get('motor_type')
    power = request.args.get('power', type=float)
    efficiency = request.args.get('efficiency', type=float)

    if motor_type in ['三相异步电动机', '电容起动异步电动机', '电容运转异步电动机', '双值电容异步电动机', '空调器风扇用异步电动机', '异步起动三相永磁同步电动机']:
        # 使用 SQLAlchemy ORM 进行查询
        result = MotorFile.query.filter(and_(MotorFile.power == power, MotorFile.efficiency < efficiency, MotorFile.motor_type == motor_type)).first()
        if result:
            energy_consumption = result.energy_consumption
            print(energy_consumption)
            return jsonify({'energy_consumption': energy_consumption})
        else:
            return jsonify({'message': 'No results found'})
    elif motor_type in ['空调器风扇用无刷直流电动机', '电梯用永磁同步电动机', '变频驱动永磁同步电动机']:
        # 使用 SQLAlchemy ORM 进行查询，假设表名为 MotorFile
        result = MotorFile.query.filter(and_(MotorFile.power == power, MotorFile.efficiency < efficiency, MotorFile.motor_type == motor_type, MotorFile.rotate_speed <= 500)).first()
        if result:
            energy_consumption = result.energy_consumption
            print(energy_consumption)
            return jsonify({'energy_consumption': energy_consumption})
        else:
            return jsonify({'message': 'No results found'})
    else:
        return jsonify({'message': 'Invalid motor type'})


if __name__ == '__main__':
    app.run(debug=True)
