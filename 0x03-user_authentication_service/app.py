#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home() -> str:
    """Home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """Register user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Login user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        return abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """Logout user
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        return abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
