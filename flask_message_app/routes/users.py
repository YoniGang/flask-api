import logging
from flask import request, jsonify
from flask_message_app import app, db
from flask_message_app.models import User
import werkzeug
import flask_message_app.status_codes as status

@app.route("/user/create_user", methods=['POST'])
def user():
    #Check if the request contains a json
    if request.is_json:
        try:
            content = request.get_json()
            user = User(username=content['username'], email=content['email'], password=content['password'])
            db.session.add(user)
            db.session.commit()
            return jsonify({'Success': 'User created'}), status.CREATED
        except Exception as e:
            return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST

    else:
        return jsonify({'error': 'Request does not contain a json'}), status.BAD_REQUEST