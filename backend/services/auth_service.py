import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import requests
from flask import current_app
from base64 import urlsafe_b64decode
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives import serialization


def get_jwks():
    """Fetch JWKS (JSON Web Key Set) from Auth0"""
    try:
        auth0_domain = current_app.config['AUTH0_DOMAIN']
        jwks_url = f"https://{auth0_domain}/.well-known/jwks.json"
        response = requests.get(jwks_url)
        response.raise_for_status()  # Raise HTTP errors if any
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch JWKS from Auth0: {str(e)}")


def jwk_to_pem(jwk):
    """Convert JWK (JSON Web Key) to PEM format"""
    def decode_base64url(data):
        # Base64url decode (with padding adjustment)
        padding = 4 - (len(data) % 4)
        data += "=" * padding
        return urlsafe_b64decode(data)

    # Decode the 'n' (modulus) and 'e' (exponent) parameters from the JWK
    n = decode_base64url(jwk['n'])
    e = decode_base64url(jwk['e'])

    # Convert to integers
    n = int.from_bytes(n, byteorder='big')
    e = int.from_bytes(e, byteorder='big')

    # Create RSA public numbers and then the public key
    public_numbers = RSAPublicNumbers(e, n)
    public_key = public_numbers.public_key()

    # Convert the public key to PEM format and return as a string
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')


def decode_token(token):
    """Decode and validate the JWT token"""
    try:
        # Fetch JWKS (JSON Web Key Set) from Auth0
        jwks = get_jwks()

        # Get unverified JWT header
        unverified_header = jwt.get_unverified_header(token)
        if not unverified_header:
            raise Exception("Invalid token header")

        rsa_key = None

        # Find the matching key from JWKS using the 'kid' (Key ID)
        for key in jwks.get('keys', []):
            if key.get('kid') == unverified_header.get('kid'):
                rsa_key = key
                break

        if not rsa_key:
            raise Exception("No matching RSA key found in JWKS")

        # Convert the JWK to PEM format for key verification
        pem_key = jwk_to_pem(rsa_key)

        # Configuration values (replace with your actual values if needed)
        auth0_domain = current_app.config['AUTH0_DOMAIN']
        api_identifier = current_app.config['API_IDENTIFIER']
        algorithms = current_app.config.get('ALGORITHMS', ['RS256'])

        # Decode the JWT using the PEM public key and validate it
        payload = jwt.decode(
            token,
            pem_key,
            algorithms=algorithms,
            audience=api_identifier,
            issuer=f"https://{auth0_domain}/"
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token format")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error while fetching JWKS: {str(e)}")
    except Exception as e:
        raise Exception(f"Token validation failed: {str(e)}")
