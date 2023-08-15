from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message
from sqlalchemy import desc
import ipdb
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "gettin started and shit"

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    # ipdb.set_trace()
    if request.method == 'GET':
        messages = []
        for message in Message.query.order_by(Message.created_at).all():
            message_dict = message.to_dict()
            messages.append(message_dict)
        response = make_response(
            messages,
            200
        )
        return response
    elif request.method == 'POST':
        # ipdb.set_trace()
        requestin_stuff=request.get_json()
        new_message = Message(
            body = requestin_stuff["body"],
            username = requestin_stuff["username"]
        )
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        response = make_response(
            message_dict,
            201
        )
        return response

@app.route('/messages/<int:id>',methods=['GET', 'PATCH', 'DELETE'] )
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if message == None:
        response_body = {
            "message": "This record does not exist in our database. Please go fuck yourself."
        }
        response = make_response(response_body, 404)
        return response
    else:
        if request.method=="GET":
            message_dict = message.to_dict()
            response = make_response(
                message_dict,
                200
            )
            return response 
        

        # elif request.method=='PATCH':
        #     for attr in request.form:
        #         setattr(message, attr, message.form.get(attr))
        #     db.session.add(message)
        #     db.session.commit()
        #     message_dict = message.to_dict()
        #     response = make_response(
        #         message_dict,
        #         200
        #     )
        #     return response
        
        elif request.method == 'PATCH': 
            data = request.get_json() 
            for attr in data: 
                setattr(message, attr, data[attr]) 
                db.session.add(message) 
                db.session.commit() 
                message_dict = message.to_dict() 
                response = make_response( message_dict, 200 ) 
                return response



        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()
            response_body={
                "delete_succesful":True,
                "message": "Message deleted mothafuka"
            }

            response = make_response(
                response_body,
                200
            )
            return response



if __name__ == '__main__':
    app.run(port=5555)

