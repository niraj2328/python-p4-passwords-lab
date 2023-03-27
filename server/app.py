#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):
    def delete(self):
        session.pop('page_views', None)
        session.pop('user_id', None)
        return {}, 204

class Signup(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': '422 Unprocessable Entity'}, 422

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {'error': '422 Unprocessable Entity'}, 422

        user = User(username=username)
        user.password_hash = password
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {}, 204

        user = User.query.get(user_id)
        if not user:
            return {}, 204

        return user.to_dict(), 200

class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': '422 Unprocessable Entity'}, 422

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {'error': '422 Unprocessable Entity'}, 422

        user = User.query.filter_by(username=username).first()
        if not user or not user.authenticate(password):
            return {'error': 'Unauthorized'}, 401

        session['user_id'] = user.id
        return user.to_dict(), 200

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

api.add_resource(ClearSession, '/clear')
api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
