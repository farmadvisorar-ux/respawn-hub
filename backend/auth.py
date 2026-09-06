import hashlib
import secrets
import os
from typing import Optional
from fastapi import Header, HTTPException
from backend.database import get_db_cursor

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${key}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, key = stored_hash.split('$')
        computed_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(key, computed_key)
    except Exception:
        return False

def create_session(user_id: int, cur=None) -> str:
    token = secrets.token_urlsafe(32)
    if cur is not None:
        cur.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id))
    else:
        with get_db_cursor(commit=True) as c:
            c.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id))
    return token

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication token required")
    
    token = authorization
    if token.startswith("Bearer "):
        token = token[7:]
    
    with get_db_cursor(commit=False) as cur:
        cur.execute("""
            SELECT u.* FROM users u
            JOIN sessions s ON u.id = s.user_id
            WHERE s.token = ?
        """, (token,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        return dict(user)

def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    if not authorization:
        return None
    try:
        return get_current_user(authorization)
    except HTTPException:
        return None
