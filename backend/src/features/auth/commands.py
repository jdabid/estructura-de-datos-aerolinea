from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
from src.shared.exceptions import ConflictException, UnauthorizedException, ForbiddenException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise ConflictException("El email ya esta registrado")

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise UnauthorizedException("Credenciales incorrectas")
    if not user.is_active:
        raise ForbiddenException("Usuario desactivado")
    return user
