from fastapi import APIRouter, Depends, HTTPException
from src.db.db import get_db
from src.models.user import User
from src.schemas.user_schema import RegisterSchema, LoginSchema, RefreshTokenSchema
from src.utils.hash import hash_password, verify_password
from src.utils.jwt_util import create_access_token, decode_access_token
from src.core.dependencies import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register')
async def register(register_data: RegisterSchema, db: Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.email == register_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        # hash pass before storing
        register_data.password = hash_password(register_data.password)
        new_user = User(
            email=register_data.email,
            hashed_password=register_data.password,
            username=register_data.username if register_data.username else register_data.email.split('@')[0]
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully", "user_id": new_user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/login')
async def login(user_data: LoginSchema, db: Session=Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create JWT token
        access_token = create_access_token(data={"user_id": user.id})
        refresh_token = create_access_token(data={"user_id": user.id}, expires_delta=7 * 24 * 60)  # 7 days
        return {"message": "Login successful", "access_token": access_token, "refresh_token": refresh_token ,"token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/refresh')
async def refresh_token(body: RefreshTokenSchema , db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(body.refresh_token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        # Create new access token
        access_token = create_access_token(data={"user_id": user_id})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get('/me')
async def profile(current_user : User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    