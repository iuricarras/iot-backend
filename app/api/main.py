from . import api_bp
from flask import request
from . import db
from .models import Gateway
from .auth import verify_user

@api_bp.post('/gateways')
def create_gateway():
    data = request.get_json()
    
    gate = Gateway.from_dict(data)

    db.collection('gateways').add(gate.to_dict())

    return {"message": "Gateway created successfully"}, 201

@api_bp.get('/gateways')
def get_gateways():
    gateways_ref = db.collection('gateways')
    docs = gateways_ref.stream()

    gateways = [Gateway.from_dict(doc.to_dict()) for doc in docs]

    return {"gateways": [gateway.to_dict() for gateway in gateways]}, 200

@api_bp.get('/gateways/<user_id>')
def get_gateway_by_user_id(user_id):
    verify_user(request.headers.get('Authorization'), user_id)
    gateways_ref = db.collection('gateways')
    query = gateways_ref.where('userID', '==', user_id).stream()

    gateways = [Gateway.from_dict(doc.to_dict()) for doc in query]

    if not gateways:
        return {"message": "No gateway found for this user ID"}, 404

    return {"gateways": [gateway.to_dict() for gateway in gateways]}, 200

@api_bp.patch('/gateways/<gateway_id>')
def update_gateway(gateway_id):
    verify_user(request.headers.get('Authorization'), gateway_data['userID'])
    data = request.get_json()
    gateway_ref = db.collection('gateways').document(gateway_id)
    gateway_doc = gateway_ref.get()

    if not gateway_doc.exists:
        return {"message": "Gateway not found"}, 404

    gateway_data = gateway_doc.to_dict()
    
    gateway_ref.update(data)

    return {"message": "Gateway updated successfully"}, 200