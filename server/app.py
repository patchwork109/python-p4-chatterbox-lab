from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()

        messages_dict = [message.to_dict() for message in messages]

        response = make_response(
            jsonify(messages_dict),
            200
        )

        return response

    elif request.method == 'POST':
        data = request.get_json()

        new_message = Message(
            body = data['body'],
            username = data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(
            jsonify(new_message_dict),
            201
        )

        return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message_by_id = Message.query.filter(Message.id == id).first()

    if message_by_id == None:
        response_body = {
            "message": "This id does not exist."
        }

        response = make_response(
            response_body,
            404
        )

        return response

    else:
        if request.method == 'GET':
            message_by_id = Message.query.filter(Message.id == id).first()

            message_by_id_dict = message_by_id.to_dict()

            response = make_response(
                message_by_id_dict,
                200
            )

            return response
        
        elif request.method == 'PATCH':
            message_by_id = Message.query.filter(Message.id == id).first()
            
            for attr in request.get_json():
                setattr(message_by_id, attr, request.get_json()[attr])

            db.session.add(message_by_id)
            db.session.commit()

            message_by_id_dict = message_by_id.to_dict()

            response = make_response(
                message_by_id_dict,
                200
            )

            return response
        
        elif request.method == 'DELETE':
            message_by_id = Message.query.filter(Message.id == id).first()

            db.session.delete(message_by_id)
            db.session.commit()

            response_body = {
                "message": "This has been successfully deleted."
            }
            response = make_response(
                response_body,
                200
            )

            return response


if __name__ == '__main__':
    app.run(port=5550)
