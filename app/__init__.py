import logging
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from app.mpu6050 import mpu6050

app = Flask(__name__)
socketio = SocketIO(app)
sensor = mpu6050(address=0x68, bus=0)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', interval=100)


@socketio.on('connect', namespace='/mpu6050')
def on_mpu6050_connect():
    print(f'Client {request.remote_addr} connected')


@socketio.on('get_data', namespace='/mpu6050')
def on_mpu6050_get_data():
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    temp = sensor.get_temp()
    emit('recv_data_mpu6050', dict(
        accel_data=accel_data,
        gyro_data=gyro_data,
        centidegree=temp
    ))

