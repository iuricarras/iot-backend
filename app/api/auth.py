from flask import request
from . import api_bp

def sign_in_with_email_and_password(email, password, return_secure_token=True):
    payload = json.dumps({"email":email, "password":password, "return_secure_token":return_secure_token})
    #FIREBASE_WEB_API_KEY = '' 
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    r = requests.post(rest_api_url,
                  params={"key": FIREBASE_WEB_API_KEY},
                  data=payload)

    return r.json()

@api_bp.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        user = sign_in_with_email_and_password(email, password)
        return {'message': 'Login successful', 'uid': user['localId']}, 200
    except Exception as e:
        return {'message': 'Error logging in', 'error': str(e)}, 400


@api_bp.post('/register')
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username
        )
        
        return {'message': 'User created successfully', 'uid': user.uid}, 201
    except Exception as e:
        return {'message': 'Error creating user', 'error': str(e)}, 400

        