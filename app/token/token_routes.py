from flask import request, jsonify
from . import token
from app import db, jwt
from sqlalchemy import exc
from datetime import datetime
from app.models.usermodels import UserSchema, User
from app.models.revoked_token import RevokedToken
from flask_jwt_extended import create_access_token, create_refresh_token, \
    get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies

us = UserSchema() # Importing User Schema to convert the data 


# Loading JWT user claims
@jwt.user_lookup_loader
def add_claims_to_access_token(user):
    print(user)
    resp = {
        'role': user['user_role'],
        'id': user['userid'],
    }
    return resp

# Loadind the jwt identity value
@jwt.user_identity_loader
def user_identity_lookup(username):
    return username

# Checking if the token in blacklist
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    rt = RevokedToken.query.filter_by(jti=jti).first()
    return bool(rt)


@token.route("/register", methods=['POST'])
def register():
    """
    This is the endpoint to register a new user

    ---
    tags:
      - Authentication
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: The username of the new user
      - name: email
        in: formData
        type: string
        required: true
        description: The email of the new user
      - name: password
        in: formData
        type: string
        required: true
        description: The password of the new user
    responses:
      201:
        description: User registered successfully
      409:
        description: Email already exists or database error
    """
    test = User.query.filter_by(email=request.form['email']).first()

    if test:
        resp = {
            "message": "Email Already Exists"
        }
        return jsonify(resp), 409

    try:
        user = User(
            username = request.form['username'],
            email = request.form['email'],
            password = request.form['password'],
            user_role = 1,
            created_date = datetime.now()
        )
        db.session.add(user)
        db.session.commit()

        resp = jsonify({"message": "User Registered Successfully"})
        return resp, 201

    except exc.IntegrityError:
        db.session.rollback()
        resp = jsonify({"message": "Database Error"})
        return resp, 409


@token.route('/login', methods=['POST'])
def login():
    """
    User Login Endpoint.

    This endpoint allows a registered user to log in and receive a JWT access token and a refresh token.

    ---
    tags:
      - Authentication
    produces:
      - application/json
    parameters:
      - name: email
        in: formData
        type: string
        required: true
        description: The user's email address.
      - name: password
        in: formData
        type: string
        required: true
        description: The user's password.
    responses:
      200:
        description: A JSON object containing the access and refresh tokens.
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: The JWT access token.
            refresh_token:
              type: string
              description: The JWT refresh token.
      401:
        description: Authentication failed due to invalid credentials.

    """    
    user = User.query.filter_by(email= request.form['email']).first()

    if user is not None and user.verify_password(request.form['password']) and \
        user.user_role==1:
        user = us.dump(user)
        # Creating access tokens
        access_token = create_access_token(identity=user['username'])
        refresh_token = create_refresh_token(identity=user['username'])
        resp = jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
        })
        # Adding tokens to response
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        return resp, 200
    else:
        resp = jsonify({
            "message": "Wrong Email or Password"
        })
        return resp, 401


