import flask
from flask_restful import Resource, reqparse
from werkzeug.exceptions import abort

from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"user {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position')
parser.add_argument('speciality')
parser.add_argument('address')
parser.add_argument('email', required=True)


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_user_not_found(users_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(users_id)
        return flask.jsonify({'user': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address'))
        })

    def delete(self, users_id):
        abort_if_user_not_found(users_id)
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        session.delete(user)
        session.commit()
        return flask.jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return flask.jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            id=args['id'],
            surname=args['id'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email']
        )
        session.add(users)
        session.commit()
        return flask.jsonify({'id': users.id})
