import json, base64, hmac, hashlib

BILLDESK_SECRET = b"YourSecretKey".encode()
BILLDESK_CLIENTID = "YourClientID"

def create_jws_hmac(payload):
    header = {
        "alg": "HS256",
        "clientid": BILLDESK_CLIENTID
    }
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    data = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(BILLDESK_SECRET, data.encode(), hashlib.sha256).digest()
    signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{data}.{signature_encoded}"
