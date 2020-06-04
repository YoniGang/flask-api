from flask import request, jsonify
from flask_message_app import app, db
from flask_message_app.models import Message
import werkzeug
import flask_message_app.status_codes as status
# from flask_login import login_user, current_user, logout_user, login_required

#Create Tables
db.create_all()



def get_messages(unread, receiver):
    try:
        messages = Message.query.filter_by(read=False, receiver=receiver).all() if unread == True else Message.query.filter_by(receiver=receiver).all()
        if len(messages) == 0:
            #If we are reading all messages or only unread
            if not unread:
                return jsonify({'No messages': 'User name ' + receiver + ' did not receive messages'}), status.OK
            return jsonify({'No messages': 'User name ' + receiver + ' did not have unread messages'}), status.OK
        #To mark that all the messages we showed are read
        for msg in messages:
            msg.read = True
        db.session.commit()
        return jsonify([l.json_repr() for l in messages]), status.OK
            
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST 


@app.route("/")
@app.route("/home")
def home():
   return 'Welcome'


@app.route("/message/new_message", methods=['GET', 'POST'])
# @login_required
def new_message():
    #Check if the request contains a json
    if request.is_json:
        try:
            content = request.get_json()
            message = Message(sender=content['sender'], receiver=content['receiver'], message=content['message'], subject=content['subject'])
            db.session.add(message)
            db.session.commit()
            return jsonify({'Success': 'Message added'}), status.CREATED
        except Exception as e:
            return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST

    else:
        return jsonify({'error': 'Bad Request'}), status.BAD_REQUEST
    

@app.route("/message/all_messages/<receiver>", methods=['GET'])
def get_all_messages(receiver):
    return get_messages(unread = False, receiver = receiver)


@app.route("/message/unread_messages/<receiver>", methods=['GET'])
def get_unread_messages(receiver):
    return get_messages(unread = True, receiver = receiver)


@app.route("/message/get_message/<id>", methods=['GET'])
def get_message(id):
    #I know i coult write <int:id> in the path, but I wanted more accurate error message
    if not id.isnumeric():
        return jsonify({'Error': 'Id message must be an integer'}), status.BAD_REQUEST
    try:
        message = Message.query.get_or_404(id) #return 404 status if not found
        message.read = True
        db.session.commit()
        return jsonify(message.json_repr()), status.OK
    except werkzeug.exceptions.NotFound:
        return jsonify({'Error': 'Message not found'}), status.NOT_FOUND
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST
    
@app.route("/message/delete_message/<id>", methods=['DELETE', 'POST'])
def delete_message(id):
    if not id.isnumeric():
        return jsonify({'Error': 'Id message must be an integer'}), status.BAD_REQUEST
    try:
        message = Message.query.get_or_404(id) #return 404 status if not found
        db.session.delete(message)
        db.session.commit()
        return jsonify({'Success': 'Message deleted'}), status.OK
    except werkzeug.exceptions.NotFound:
        return jsonify({'Error': 'Message not found'}), status.NOT_FOUND
    except Exception as e:
        return jsonify({'exception type': str(type(e).__name__), 'exception message': str(e)}), status.BAD_REQUEST
