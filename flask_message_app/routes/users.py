from flask import request, jsonify
from flask_message_app import app, db, bcrypt
from flask_message_app.models import User
from flask_login import login_user, current_user, logout_user, login_required
import flask_message_app.status_codes as status
import re

# =============================================================================
# Create new user
# =============================================================================
@app.route("/user/create_user", methods=['POST'])
def user():
    #Check if user already logged in
    if current_user.is_authenticated:
        return jsonify({'Error': 'User logged in, please logout first'}), status.BAD_REQUEST
    #Check if the request contains a json
    if request.is_json:
        try:
            content = request.get_json()
            
            #To check if user name already exist
            check_username = User.query.filter_by(username=content['username']).first()
            if check_username is not None:
                return jsonify({'Error': 'Username already taken'}), status.BAD_REQUEST
            
            check_email = User.query.filter_by(email=content['email']).first()
            if check_email is not None:
                return jsonify({'Error': 'Email already used'}), status.BAD_REQUEST
            
            #Check if the email structure is valid
            email_regex = """^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
            if re.search(email_regex, content['email']) is None:
                return jsonify({'Error': 'Not valid email'}), status.BAD_REQUEST
            
            hashed_password = bcrypt.generate_password_hash(content['password']).decode('utf-8')
            user = User(username=content['username'], email=content['email'], password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'Success': 'User created'}), status.CREATED
        except Exception as e:
            return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST

    else:
        return jsonify({'Error': 'Request does not contain a json'}), status.BAD_REQUEST
    
# =============================================================================
# Login user   
# =============================================================================
@app.route("/user/login", methods=['GET', 'POST'])
def login():
    #Check if user already logged in
    if current_user.is_authenticated:
        return jsonify({'Error': 'User already logged in'}), status.BAD_REQUEST
    
    #Check if the request contains a json
    if request.is_json:
        try:
            content = request.get_json()
            user = User.query.filter_by(email=content['email']).first()
            if user and bcrypt.check_password_hash(user.password, content['password']):
                login_user(user)
                return jsonify({'Success': 'User logged in'}), status.OK
            else:
                return jsonify({'Error': 'Login Unsuccessful. Please check email and password'}), status.BAD_REQUEST
        except Exception as e:
            return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST
    else:
        return jsonify({'error': 'Request does not contain a json'}), status.BAD_REQUEST
 
# =============================================================================
# Logout user
# =============================================================================
@app.route("/user/logout", methods=['GET', 'POST'])
# @login_required
def logout():
    if not current_user.is_authenticated:
        return jsonify({'Error': 'Login first'}), status.BAD_REQUEST
    logout_user()
    return jsonify({'Success': 'User logged out'}), status.OK

# =============================================================================
# See logged in user details 
# =============================================================================
@app.route("/user/account", methods=['GET'])
# @login_required
def account():
    if not current_user.is_authenticated:
        return jsonify({'Error': 'Login first'}), status.BAD_REQUEST
    return jsonify(current_user.json_repr()), status.OK