# dunders and encodings below with author showing as Daulet


import json
import requests
from jose import jwt
from fastapi import HTTPException
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer



AUTH0_DOMAIN = "dev-52cl1dvvr1vlazaj.us.auth0.com"
API_IDENTIFIER = "lPkzDKPpUh65qd9SGeMCgYbxDxvuC41Y"
ALGORITHMS = ["RS256"]

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/user")
async def read_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = validate_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")

def validate_token(token: str):
    json_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    r = requests.get(json_url)
    jwks = json.loads(r.text)
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise HTTPException(status_code=400, detail="Invalid token")
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Token expired")
        except jwt.JWTClaimsError:
            raise HTTPException(status_code=400, detail="Incorrect claims")
        except Exception:
            raise HTTPException(status_code=400, detail="Unable to parse authentication token.")
    raise HTTPException(status_code=400, detail="Unable to find appropriate key")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
