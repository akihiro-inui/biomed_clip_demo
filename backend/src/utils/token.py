from jose import JWTError, jwt
from decouple import config
from datetime import datetime, timedelta

from src.utils.custom_logger import logger


def create_access_token(user_id: str,
                        expires_delta: float = config("ACCESS_TOKEN_EXPIRE_MINUTES",
                                                      default=30,
                                                      cast=float)):
    """
    Create access token with JWT
    :param user_id: User ID
    :param expires_delta: Expire time
    :return: Encoded JWT token
    """
    to_encode = {"user_id": user_id}
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"expire": f"{expire}"})

    # Encode JWT
    encoded_jwt = jwt.encode(to_encode,
                             config("SECRET_KEY"),
                             algorithm=config("HASH_ALGORITHM", default="HS256"))
    return encoded_jwt


def decode_access_token(jwt_token: str) -> dict:
    """
    Decode JWT token
    :param jwt_token: JWT token
    :return: Decoded JWT token
    """
    decoded_token = jwt.decode(jwt_token,
                               config("SECRET_KEY"),
                               algorithms=[config("HASH_ALGORITHM", default="HS256")])
    return decoded_token


def validate_access_token(user_id: str, jwt_token: str) -> str:
    """
    Verify user with JWT token
    :param user_id: User ID
    :param jwt_token: JWT token
    :return: Validity of JWT token, can be "valid", "invalid", "outdated"
    """
    try:
        # Decode JWT token
        decoded_token = decode_access_token(jwt_token)

        # Check expiration datetime
        expire = decoded_token.get("expire")
        if expire is None:
            raise Exception("Expire datetime not found")
        expire_datetime = datetime.strptime(expire, "%Y-%m-%d %H:%M:%S.%f")

        if datetime.utcnow() > expire_datetime:
            return "outdated"
        if decoded_token.get("user_id") != user_id:
            raise Exception("User ID does not match")
        return "valid"
    except JWTError:
        return "invalid"
    except Exception as err:
        logger.error(f"Validate access token failed: {err}")
        return "invalid"


if __name__ == "__main__":
    user_id = "test"
    token = create_access_token(user_id=user_id)
    print(token)
    decoded_token = decode_access_token(token)
    print(decoded_token)
