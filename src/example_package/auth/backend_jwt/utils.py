import bcrypt

# import jwt
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret: str
    algorithm: str


if __name__ == "__main__":
    password = b"super secret password"
    user_salt = bcrypt.gensalt()
    print(user_salt)
    hashed = bcrypt.hashpw(password, user_salt)
    print(hashed)
    print(bcrypt.hashpw(password, user_salt) == hashed)
    print("123".encode())
    print(bcrypt.hashpw("123".encode(), user_salt) == hashed)

    jwtsettings = Settings()
    print(jwtsettings)
