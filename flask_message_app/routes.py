from flask import request, jsonify
from flask_message_app import app, db
from flask_message_app.models import Message
import werkzeug
# from flask_login import login_user, current_user, logout_user, login_required

db.create_all()


def get_messages(unread):
    try:
        messages = Message.query.filter_by(read=False).all() if unread == True else Message.query.all()
        return jsonify([l.json_repr() for l in messages]), 200
            
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), 400 


@app.route("/")
@app.route("/home")
def home():
   return 'hello'


@app.route("/message/new_message", methods=['GET', 'POST'])
# @login_required
def new_message():
    if request.is_json:
        try:
            content = request.get_json()
            message = Message(sender=content['sender'], receiver=content['receiver'], message=content['message'], subject=content['subject'])
            db.session.add(message)
            db.session.commit()
            return jsonify({'Success': 'Message added'}), 200
        except Exception as e:
            return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), 400

    else:
        return jsonify({'error': 'Bad Request'}), 400
    

@app.route("/message/all_messages", methods=['GET'])
def get_all_messages():
    return get_messages(unread =False)

@app.route("/message/unread_messages", methods=['GET'])
def get_unread_messages():
    return get_messages(unread = True)

@app.route("/message/get_message/<id>", methods=['GET'])
def get_message(id):
    #I know i coult write <int:id> in the path, but I wanted more accurate error message
    if not id.isnumeric():
        return jsonify({'Error': 'Id message must be an integer'}), 400
    try:
        message = Message.query.get_or_404(id)
        return jsonify(message.json_repr()), 200
    except werkzeug.exceptions.NotFound:
        return jsonify({'Error': 'Message not found'}), 404
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), 400
    
@app.route("/message/delete_message/<id>", methods=['DELETE', 'POST'])
def delete_message(id):
    if not id.isnumeric():
        return jsonify({'Error': 'Id message must be an integer'}), 400
    try:
        message = Message.query.get_or_404(id)
        db.session.delete(message)
        db.session.commit()
        return jsonify({'Success': 'Message deleted'}), 200
    except werkzeug.exceptions.NotFound:
        return jsonify({'Error': 'Message not found'}), 404
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), 400
