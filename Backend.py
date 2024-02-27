from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='app.log', level=logging.INFO)

cars = []

@app.route('/cars', methods=['POST'])
def register_car():
    data = request.form
    license_plate = data.get('license_plate')
    color = data.get('color')
    entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtiene la hora actual
    # Guarda los datos en memoria
    cars.append({'license_plate': license_plate, 'color': color, 'entry_time': entry_time})
    # Loggea el registro del carro
    logging.info(f"Car registered: {license_plate}")
    return jsonify({'message': 'Car registered successfully'}), 201

@app.route('/cars', methods=['GET'])
def list_cars():
    return jsonify(cars)

@app.route('/cars', methods=['PATCH'])
def withdraw_car():
    data = request.json
    license_plate = data.get('license_plate')
    # Elimina el carro de la lista en memoria
    removed_cars = [car for car in cars if car.get('license_plate') == license_plate]
    cars[:] = [car for car in cars if car.get('license_plate') != license_plate]
    # Loggea el retiro del carro
    if removed_cars:
        logging.info(f"Car withdrawn: {license_plate}")
        return jsonify({'message': 'Car withdrawn successfully'}), 200
    else:
        return jsonify({'error': 'Car not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
