from flask import request, jsonify
from flask_message_app import app, db
from flask_message_app.models import Message, User
import werkzeug
import flask_message_app.status_codes as status
from flask_login import current_user, login_required

#Create Tables
db.create_all()



def get_messages(unread, receiver):
    try:
        #check if return all messages or only unread messages
        messages = receiver.messages if unread == False else [msg for msg in receiver.messages if msg.read==False]
        if len(messages) == 0:
            #If we are reading all messages or only unread
            if not unread:
                return jsonify({'No messages': 'User ' + receiver.username + ' did not receive messages'}), status.OK
            return jsonify({'No messages': 'User ' + receiver.username + ' did not have unread messages'}), status.OK
        #To mark that all the messages we showed are read
        for msg in messages:
            msg.read = True
        db.session.commit()
        return jsonify([l.json_repr() for l in messages]), status.OK
        # return str(messages)
            
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST 

# =============================================================================
# Basic home screen
# =============================================================================
@app.route("/")
@app.route("/home")
def home():
   return 'Welcome'

# =============================================================================
# Write new messgae
# =============================================================================
@app.route("/message/new_message", methods=['GET', 'POST'])
# @login_required
def new_message():
    if not current_user.is_authenticated:
        return jsonify({'Error': 'Login first'}), status.BAD_REQUEST
    #Check if the request contains a json
    if request.is_json:
        try:
            content = request.get_json()
            receiver = User.query.filter_by(username=content['receiver']).first()
            if receiver is None:
                return jsonify({'Error': 'Receiver user ' + content['receiver'] + ' does not exist'}), status.BAD_REQUEST
            message = Message(sender=current_user.username, receiver=receiver, message=content['message'], subject=content['subject'])
            db.session.add(message)
            db.session.commit()
            return jsonify({'Success': 'Message added'}), status.CREATED
        except Exception as e:
            return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST

    else:
        return jsonify({'Error': 'Request does not contain a json'}), status.BAD_REQUEST
    
# =============================================================================
# Get all messages by user
# =============================================================================
@app.route("/message/all_messages", methods=['GET'])
# @login_required
def get_all_messages():
    if not current_user.is_authenticated:
        return jsonify({'Error': 'Login first'}), status.BAD_REQUEST
    return get_messages(unread = False, receiver = current_user)

# =============================================================================
# Get all unread messages by user
# =============================================================================
@app.route("/message/unread_messages", methods=['GET'])
# @login_required
def get_unread_messages():
    if not current_user.is_authenticated:
        return jsonify({'Error': 'Login first'}), status.BAD_REQUEST
    return get_messages(unread = True, receiver = current_user)


# =============================================================================
# Get message by id
# =============================================================================
@app.route("/message/get_message/<id>", methods=['GET'])
# @login_required
def get_message(id):
    if not current_user.is_authenticated:
        return jsonify({'Error': 'Login first'}), status.BAD_REQUEST
    #I know i coult write <int:id> in the path, but I wanted more accurate error message
    if not id.isnumeric():
        return jsonify({'Error': 'Id message must be an integer'}), status.BAD_REQUEST
    try:
        message = Message.query.get_or_404(id) #return 404 status if not found
        #check if the user is the sender of the receiver of the message
        if message.user_id != current_user.id and message.sender != current_user.username:
            return jsonify({'Error': 'The user is not the sender or the receiver of the message'}), status.NOT_FOUND
        message.read = True
        db.session.commit()
        return jsonify(message.json_repr()), status.OK
    except werkzeug.exceptions.NotFound:
        return jsonify({'Error': 'Message not found'}), status.NOT_FOUND
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST

# =============================================================================
# Delete message by id   
# =============================================================================
@app.route("/message/delete_message/<id>", methods=['DELETE', 'POST'])
# @login_required
def delete_message(id):
    if not current_user.is_authenticated:
        return jsonify({'Error': 'Login first'}), status.BAD_REQUEST
    if not id.isnumeric():
        return jsonify({'Error': 'Id message must be an integer'}), status.BAD_REQUEST
    try:
        message = Message.query.get_or_404(id) #return 404 status if not found
        #check if the user is the sender of the receiver of the message
        if message.user_id != current_user.id and message.sender != current_user.username:
            return jsonify({'Error': 'The user is not the sender or the receiver of the message'}), status.NOT_FOUND
        db.session.delete(message)
        db.session.commit()
        return jsonify({'Success': 'Message deleted'}), status.OK
    except werkzeug.exceptions.NotFound:
        return jsonify({'Error': 'Message not found'}), status.NOT_FOUND
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST


# =============================================================================
############### For development env!!!######################
# =============================================================================
# @app.route("/message/delete_all_messages", methods=['DELETE', 'POST'])
# def delete_all_messages():
#     try:
#         message = Message.query.all()
#         for msg in message:
#             db.session.delete(msg)
#         db.session.commit()
#         return jsonify({'Success': 'All messages deleted'}), status.OK
#     except Exception as e:
#         return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST
    
# @app.route("/message/delete_all_users", methods=['DELETE', 'POST'])
# def delete_all_users():
#     try:
#         users = User.query.all()
#         for user in users:
#             db.session.delete(user)
#         db.session.commit()
#         return jsonify({'Success': 'All users deleted'}), status.OK
#     except Exception as e:
#         return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST
