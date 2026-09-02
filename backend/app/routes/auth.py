from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime
import uuid

from app.core.deps import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user_from_token)):
    return current_user


@router.post("/verify-email")
def verify_email(email: str = Query(...), otp: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or OTP")

    if user.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid email or OTP")

    if user.otp_expires_at and user.otp_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    user.email_verified = True
    user.otp = None
    user.otp_expires_at = None
    db.commit()
    return {"message": "Email verified successfully"}


@router.post("/resend-verification")
def resend_verification(current_user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    if current_user.email_verified:
        raise HTTPException(status_code=400, detail="Email is already verified")

    from app.routes.users import generate_otp
    from datetime import timedelta

    current_user.otp = generate_otp()
    current_user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
    db.commit()
    db.refresh(current_user)

    try:
        html = f"""
        <html>
          <body>
            <h2>Verify your email</h2>
            <p>Your OTP is: <strong>{current_user.otp}</strong></p>
            <p>This OTP will expire in 10 minutes.</p>
          </body>
        </html>
        """
        from app.services.email import send_email
        send_email(current_user.email, "Verify your email", html)
    except Exception:
        pass

    return {"message": "Verification OTP sent to your email"}
