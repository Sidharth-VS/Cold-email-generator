from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import random

from app.core.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.routes.auth import get_current_user_from_token
from app.services.email import send_email

router = APIRouter()


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = generate_otp()
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        email_verified=False,
        otp=otp,
        otp_expires_at=datetime.utcnow() + timedelta(minutes=10),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    try:
        html = f"""
        <html>
          <body>
            <h2>Verify your email</h2>
            <p>Your OTP is: <strong>{otp}</strong></p>
            <p>This OTP will expire in 10 minutes.</p>
          </body>
        </html>
        """
        send_email(user.email, "Verify your email", html)
    except Exception as e:
        logger.warning(f"Failed to send verification email to {user.email}: {e}")

    return {
        "user": UserResponse.model_validate(user),
        "message": "Registration successful. Please verify your email with the OTP sent to your inbox.",
    }


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.email_verified:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify your email before logging in.")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user_from_token)):
    return current_user
