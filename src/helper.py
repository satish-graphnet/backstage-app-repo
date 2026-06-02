import jwt
import time
import random
import string
import json
import os
import uuid

def get_jwt():
    # external vars
    kid = os.environ.get('NHS_KID', 'default_kid') 
    apiKey = os.environ.get('NHS_API_KEY', 'default_nhs_api_key') 
    privateKey = os.environ.get('NHS_PRIVATE_KEY', 'default_nhs_private_key') 

    jti = str(uuid.uuid4())

    # Expiry: now + 5 minutes
    current_time = int(time.time())
    exp = current_time + (5 * 60)

    header = {
        "alg": "RS512",
        "typ": "JWT",
        "kid": kid
    }

    payload = {
        "exp": exp,
        "iss": apiKey,
        "sub": apiKey,
        "aud": "https://int.api.service.nhs.uk/oauth2/token",
        "jti": jti
    }

    # Sign JWT (RS512)
    token = jwt.encode(
        payload,
        privateKey,
        algorithm="RS512",
        headers=header
    )

    return token