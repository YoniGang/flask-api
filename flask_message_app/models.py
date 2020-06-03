from datetime import datetime
from flask_message_app import db#, login_manager
# from flask_login import UserMixin


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20), nullable=False)
    receiver = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    subject = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, nullable=False, default = False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Message('{self.subject}', '{self.creation_date}')"
    
    def json_repr(self):
        json_msg = {}
        json_msg['id'] = self.id
        json_msg['sender'] = self.sender
        json_msg['receiver'] = self.receiver
        json_msg['message'] = self.message
        json_msg['subject'] = self.subject
        json_msg['read'] = self.read
        json_msg['creation_date'] = self.creation_date
        
        return json_msg
        