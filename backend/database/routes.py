# API routes

from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok"})

    return app
