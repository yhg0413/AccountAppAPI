import jwt
import datetime
from config import settings


def generate_token(payload: dict, type: str):
    if type == "access":
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    elif type == "refresh":
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    else:
        raise Exception("Invalid token")

    payload['exp'] = exp
    payload['iat'] = datetime.datetime.utcnow()
    encoded = jwt.encode(payload, settings.env('JWT_SECRET_KEY'), algorithm="HS256")

    return encoded


def decode_token(access_token, refresh_token):
    access_token = str(access_token).replace('Bearer ', '')
    refresh_token = str(refresh_token).replace('Bearer ', '')
    new_access_token = None
    try:
        decoded = jwt.decode(access_token, settings.env('JWT_SECRET_KEY'), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        try:
            refresh_decoded = jwt.decode(refresh_token, settings.env('JWT_SECRET_KEY'), algorithms=["HS256"])
            new_access_token = re_issue_token(refresh_decoded)
            decoded = jwt.decode(new_access_token, settings.env('JWT_SECRET_KEY'), algorithms=["HS256"])
        except Exception:
            return False
    except Exception:
        return False
    return decoded,new_access_token

def re_issue_token(decoded):
    paylaod = decoded
    jwt_token = generate_token(paylaod,"access")
    return jwt_token
