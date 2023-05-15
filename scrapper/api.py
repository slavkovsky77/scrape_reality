from flask import jsonify, request, Blueprint
from scrapper.db import Database, ScrappedFlat, FlatHistory

bp = Blueprint('api', __name__, url_prefix='/api')
db = Database()


@bp.route('/flats', methods=['GET'])
def get_flats():
    flats = db.get_flats()
    flats_dicts = [flat.to_dict() for flat in flats]
    return jsonify(flats_dicts)


@bp.route('/flats/<string:apartment_number>', methods=['GET'])
def get_flat(apartment_number):
    flat = db.get_flat(apartment_number)
    if flat is not None:
        return jsonify(flat.to_dict())
    else:
        return jsonify({'message': 'Flat not found'}), 404


@bp.route('/flats/<string:apartment_number>/history', methods=['GET'])
def get_flat_history(apartment_number):
    flat_history = db.session.query(FlatHistory).filter_by(apartment_number=apartment_number).all()
    return jsonify([fh.to_dict() for fh in flat_history])


@bp.route('/flats/create_flat', methods=['POST'])
def create_flat():
    flat_dict = request.get_json()
    db.create_flat(ScrappedFlat(**flat_dict))
    return jsonify(flat_dict), 201


@bp.route('/flats/<string:apartment_number>', methods=['PUT'])
def update_flat(apartment_number):
    print(f'Received request to update flat {apartment_number}')

    flat_dict = request.get_json()
    flat = db.update_flat(apartment_number, flat_dict)
    if flat is None:
        return jsonify({'message': 'Flat not found'}), 404

    return jsonify(flat.to_dict())


@bp.route('/flats/<string:apartment_number>', methods=['DELETE'])
def delete_flat(apartment_number):
    success = db.delete_flat(apartment_number)
    if success:
        return jsonify({'message': 'Flat deleted'})
    else:
        return jsonify({'message': 'Flat not found'}), 404
