from flask import Flask, jsonify, request
import datetime
import socket

import os
import secrets
from functools import wraps

app = Flask(__name__)


# API_KEY = os.environ.get("MY_API_KEY", "fallback-default-key-for-local-dev")
API_KEY = "dmj@unb6GHD0egb6bxuwfjPNv3ELFs49yRh*MEf"

def require_api_key(f):
    """Decorator to restrict endpoint access to valid API keys."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract token from the custom 'x-api-key' request header
        provided_key = request.headers.get("x-api-key")
        
        if not provided_key:
            return jsonify({"error": "API key is missing"}), 401
            
        if provided_key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 403
            
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/v1/info')
def info():
    return jsonify({
    	'time': datetime.datetime.now().strftime("%I:%M:%S%p  on %B %d, %Y"),
    	'hostname': socket.gethostname(),
        'message': 'You are doing great, little human!!!',
        'deployed_on': 'kubernetes'
    })


@app.route('/api/v1/get_token')
@require_api_key
def getToken():
	# Do an actual check here
    return jsonify({'token': 'xyz'}), 200

@app.route('/api/v1/healthz')
def health():
	# Do an actual check here
    return jsonify({'status': 'up'}), 200

if __name__ == '__main__':

    app.run(host="0.0.0.0")
