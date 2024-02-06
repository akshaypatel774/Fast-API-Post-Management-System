from passlib.context import CryptContext

pwd = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash(password: str):
    return pwd.hash(password)

def verify(raw_password, hashed_password):
    return pwd.verify(raw_password, hashed_password)