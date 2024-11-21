from flask import jsonify
from app.api import bp

@bp.route('/test')
def test():
    return jsonify({'message': 'API is working'})