from . import api_bp
from flask import request
from .models.gateway import Gateway
from .models.action import Action
from .models.data import Data
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
    if not verify_user(request.headers.get('Authorization'), user_id):
        return {"message": "Unauthorized"}, 401

    gateways_ref = db.collection('gateways')
    docs = gateways_ref.stream()

    gateways = [Gateway.from_dict(doc.to_dict()) for doc in docs]

    return {"gateways": [gateway.to_dict() for gateway in gateways]}, 200
    gateways_ref = db.collection('gateways')
    query = gateways_ref.where('userID', '==', user_id).stream()

    gateways = [Gateway.from_dict(doc.to_dict()) for doc in query]

    if not gateways:
        return {"message": "No gateway found for this user ID"}, 404

    return {"gateways": [gateway.to_dict() for gateway in gateways]}, 200

@api_bp.patch('/gateways/<gateway_id>')
def update_gateway(gateway_id):
    data = request.get_json()
    gateway_ref = db.collection('gateways').document(gateway_id)
    gateway_doc = gateway_ref.get()

    if not gateway_doc.exists:
        return {"message": "Gateway not found"}, 404

    gateway_data = gateway_doc.to_dict()

    if not gateway_data['linked']:
        if not verify_user(request.headers.get('Authorization'), data['userID']):
            return {"message": "Unauthorized"}, 401

        if data['linkCode'] != gateway_data['linkCode']:
            return {"message": "Invalid link code"}, 400
    
        data['linked'] = True
    elif not verify_user(request.headers.get('Authorization'), gateway_data['userID']):
        return {"message": "Unauthorized"}, 401

    gateway_ref.update(data)

    return {"message": "Gateway updated successfully"}, 200


@api_bp.delete('/gateways/<gateway_id>')
def delete_gateway(gateway_id):
    gateway_ref = db.collection('gateways').document(gateway_id)
    gateway_doc = gateway_ref.get()

    if not gateway_doc.exists:
        return {"message": "Gateway not found"}, 404

    gateway_data = gateway_doc.to_dict()
    if not verify_user(request.headers.get('Authorization'), gateway_data['userID']):
        return {"message": "Unauthorized"}, 401
    
    gateway_ref.delete()

    return {"message": "Gateway deleted successfully"}, 200


@api_bp.get('/data')
def get_data():
    data_ref = db.collection('data')
    docs = data_ref.stream()

    data = [doc.to_dict() for doc in docs]

    return {"data": data}, 200

@api_bp.get('/data/<gateway_id>')
def get_data_by_gateway_id(gateway_id):
    data_ref = db.collection('data')
    query = data_ref.where('gatewayID', '==', gateway_id).stream()

    gateway_ref = db.collection('gateways').document(gateway_id)
    gateway_doc = gateway_ref.get()

    if not gateway_doc.exists:
        return {"message": "Gateway not found"}, 404

    if not verify_user(request.headers.get('Authorization'), gateway_doc.to_dict()['userID']):
        return {"message": "Unauthorized"}, 401

    data = [doc.to_dict() for doc in query]

    if not data:
        return {"message": "No data found for this gateway ID"}, 404

    return {"data": data}, 200

@api_bp.post('/data')
def create_data():
    data = request.get_json()
    
    data_ref = db.collection('data')
    data_ref.add(data)

    return {"message": "Data created successfully"}, 201


@api_bp.get('/users/<user_id>/data')
def get_data_by_user_id(user_id):
    if not verify_user(request.headers.get('Authorization'), user_id):
        return {"message": "Unauthorized"}, 401

    gateways_ref = db.collection('gateways')
    query = gateways_ref.where('userID', '==', user_id).stream()

    gateway_ids = [doc.id for doc in query]

    data_ref = db.collection('data')
    data = []
    for gateway_id in gateway_ids:
        data_query = data_ref.where('gatewayID', '==', gateway_id).stream()
        data.extend([doc.to_dict() for doc in data_query])

    if not data:
        return {"message": "No data found for this user ID"}, 404

    return {"data": data}, 200

@api_bp.get('/users/<user_id>/gateways')
def get_gateways_by_user_id(user_id):
    if not verify_user(request.headers.get('Authorization'), user_id):
        return {"message": "Unauthorized"}, 401

    gateways_ref = db.collection('gateways')
    query = gateways_ref.where('userID', '==', user_id).stream()

    gateways = [Gateway.from_dict(doc.to_dict()) for doc in query]

    if not gateways:
        return {"message": "No gateway found for this user ID"}, 404

    return {"gateways": [gateway.to_dict() for gateway in gateways]}, 200

@api_bp.post('/actions')
def create_action():
    data = request.get_json()
    
    actions_ref = db.collection('actions')
    actions_ref.add(data)

    return {"message": "Action created successfully"}, 201

@api_bp.get('/actions/<gateway_id>')
def get_actions_by_gateway_id(gateway_id):
    actions_ref = db.collection('actions')
    query = actions_ref.where('gatewayID', '==', gateway_id).stream()

    gateway_ref = db.collection('gateways').document(gateway_id)
    gateway_doc = gateway_ref.get()

    if not gateway_doc.exists:
        return {"message": "Gateway not found"}, 404

    if not verify_user(request.headers.get('Authorization'), gateway_doc.to_dict()['userID']):
        return {"message": "Unauthorized"}, 401

    actions = [doc.to_dict() for doc in query]

    if not actions:
        return {"message": "No action found for this gateway ID"}, 404

    return {"actions": actions}, 200


@api_bp.patch('/actions/<action_id>')
def update_action(action_id):
    data = request.get_json()
    action_ref = db.collection('actions').document(action_id)
    action_doc = action_ref.get()

    if not action_doc.exists:
        return {"message": "Action not found"}, 404

    action_data = action_doc.to_dict()
    gateway_ref = db.collection('gateways').document(action_data['gatewayID'])
    gateway_doc = gateway_ref.get()

    if not gateway_doc.exists:
        return {"message": "Gateway not found"}, 404

    if not verify_user(request.headers.get('Authorization'), gateway_doc.to_dict()['userID']):
        return {"message": "Unauthorized"}, 401
    
    action_ref.update(data)

    return {"message": "Action updated successfully"}, 200

@api_bp.delete('/actions/<action_id>')
def delete_action(action_id):
    action_ref = db.collection('actions').document(action_id)
    action_doc = action_ref.get()

    if not action_doc.exists:
        return {"message": "Action not found"}, 404

    action_data = action_doc.to_dict()
    gateway_ref = db.collection('gateways').document(action_data['gatewayID'])
    gateway_doc = gateway_ref.get()

    if not gateway_doc.exists:
        return {"message": "Gateway not found"}, 404

    if not verify_user(request.headers.get('Authorization'), gateway_doc.to_dict()['userID']):
        return {"message": "Unauthorized"}, 401
    
    action_ref.delete()

    return {"message": "Action deleted successfully"}, 200


