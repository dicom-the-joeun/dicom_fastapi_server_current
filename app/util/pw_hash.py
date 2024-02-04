from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_pw(pw : str):
    return password_context.hash(pw)

def verify_pw(pw:str, hashed_pass: str):
    return password_context.verify(pw,hashed_pass)
