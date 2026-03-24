import os
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# The JWKS URL is typically: https://<your-frontend-api>.clerk.accounts.dev/.well-known/jwks.json
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

jwk_client = jwt.PyJWKClient(CLERK_JWKS_URL) if CLERK_JWKS_URL else None
security = HTTPBearer(auto_error=False)

def verify_clerk_token(token: str) -> str:
    if not jwk_client:
        raise HTTPException(status_code=500, detail="CLERK_JWKS_URL not configured on backend.")
    try:
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
        return payload.get("sub")
    except jwt.PyJWKClientError as e:
        raise HTTPException(status_code=401, detail=f"Unable to fetch JWKS to verify token: {e}")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {e}")


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Security(security)) -> str | None:
    """
    Returns the user_id (sub) from the Clerk JWT if valid.
    Returns None if no token is provided.
    Raises 401 if the token is invalid or expired.
    """
    if credentials:
        token = credentials.credentials
        return verify_clerk_token(token)
    return None
