from flask import Flask, jsonify, request
import requests
import datetime
import socket

import os
import secrets
from functools import wraps

from helper import * 

app = Flask(__name__)


API_KEY = os.environ.get('API_KEY', 'my_default_local_secret') 

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

@app.route('/api/access-token/v1/info')
def info():
    return jsonify({
    	'time': datetime.datetime.now().strftime("%I:%M:%S%p  on %B %d, %Y"),
    	'hostname': socket.gethostname(),
        'message': 'access-token-api-info:v1',
        'deployed_on': 'kubernetes'
    })


@app.route('/api/access-token/v1/get-token')
@require_api_key
def getToken():

    url = "https://int.api.service.nhs.uk/oauth2/token"

    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    
    payload = {
        'grant_type': 'client_credentials',
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
        'client_assertion': get_jwt()
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/access-token/v1/healthz')
def health():
	# Do an actual check here
    return jsonify({'status': 'up'}), 200

if __name__ == '__main__':

    app.run(host="0.0.0.0")
