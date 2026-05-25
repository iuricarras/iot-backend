from flask import request
from firebase_admin import auth
from . import api_bp
import json, requests
import dotenv

FIREBASE_WEB_API_KEY = dotenv.get_key(".env", "FIREBASE_WEB_API_KEY");

def verify_user(id_token, user_id=None) -> bool:
    try:
        decoded_token = auth.verify_id_token(id_token)
        if user_id and decoded_token.get("user_id") != user_id:
            return False
        return True
    except Exception as e:
        return False

def sign_in_with_email_and_password(email, password):
    payload = json.dumps(
        {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }
    )
    rest_api_url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    )

    r = requests.post(rest_api_url, params={"key": FIREBASE_WEB_API_KEY}, data=payload)

    print(f"Firebase sign-in response: {r.status_code} - {r.text}")
    return r.json()


@api_bp.post("/login")
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    try:
        user = sign_in_with_email_and_password(email, password)
        return {"message": "Login successful", "uid": user["localId"], "token": user["idToken"]}, 200
    except Exception as e:
        return {"message": "Error logging in", "error": str(e)}, 400


@api_bp.post("/register")
def register():
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")

    try:
        user = auth.create_user(email=email, password=password, display_name=username)

        return {"message": "User created successfully", "uid": user.uid}, 201
    except Exception as e:
        return {"message": "Error creating user", "error": str(e)}, 400
