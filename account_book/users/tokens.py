import jwt
import datetime
from config import settings


def generate_token(payload: dict, type: str):
    if type == "access":
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    elif type == "refresh":
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=3)
    else:
        raise Exception("Invalid token")

    payload['exp'] = exp
    payload['iat'] = datetime.datetime.utcnow()
    encoded = jwt.encode(payload, settings.env('JWT_SECRET_KEY'), algorithm="HS256")

    return encoded


def decode_token(access_token, refresh_token):
    access_token = str(access_token).replace('Bearer ', '')
    refresh_token = str(refresh_token).replace('Bearer ', '')
    try:
        decoded = jwt.decode(access_token, settings.env('JWT_SECRET_KEY'), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        try:
            decoded = jwt.decode(refresh_token, settings.env('JWT_SECRET_KEY'), algorithms=["HS256"])
        except Exception as e:
            return False
    except Exception as e:
        return False
    return decoded
