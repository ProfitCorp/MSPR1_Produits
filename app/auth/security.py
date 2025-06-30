from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from auth.auth import SECRET_KEY, ALGORITHM
import logging
import bcrypt

logger = logging.getLogger("uvicorn")

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            payload = self.verify_jwt(credentials.credentials)
            print(payload)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token")
            elif payload.get("role") != "admin":
                raise HTTPException(status_code=403, detail="You don't have admin privilege")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

    def verify_jwt(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')