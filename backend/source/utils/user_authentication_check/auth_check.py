from typing import Dict, Any

import jwt
import requests
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer


class FirebaseUser:
    def __init__(self, payload: Dict[str, Any]):
        self.user_id = payload.get('user_id') or payload.get('sub')
        self.email = payload.get('email')
        self.email_verified = payload.get('email_verified', False)
        self.auth_time = payload.get('auth_time')
        self.firebase = payload.get('firebase', {})
        self.exp = payload.get('exp')
        self.full_payload = payload

    def __str__(self):
        return f"FirebaseUser(id={self.user_id}, email={self.email})"


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
        self.firebase_project_id = "group-project-e509b"
        self.jwks_uri = f"https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com"
        self.jwks = None

    async def __call__(self, request: Request) -> FirebaseUser:
        creds = await super().__call__(request)

        try:
            unverified_header = jwt.get_unverified_header(creds.credentials)
            kid = unverified_header.get('kid')

            if not kid:
                raise HTTPException(status_code=400, detail="Invalid token: No key ID in header")

            if not self.jwks:
                jwks_response = requests.get(self.jwks_uri)
                self.jwks = jwks_response.json()

            rsa_key = None
            for key in self.jwks.get('keys', []):
                if key.get('kid') == kid:
                    rsa_key = key
                    break

            if not rsa_key:
                raise HTTPException(status_code=400, detail="Invalid token: Key ID not found")

            payload = jwt.decode(
                creds.credentials,
                jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key),
                algorithms=["RS256"],
                audience=self.firebase_project_id,
                issuer=f"https://securetoken.google.com/{self.firebase_project_id}"
            )

            return FirebaseUser(payload)

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=400, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error validating token: {str(e)}")