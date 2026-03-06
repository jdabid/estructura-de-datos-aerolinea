from src.features.auth import commands, models, schemas
from src.features.auth.commands import pwd_context
from src.features.auth.jwt import ALGORITHM, SECRET_KEY, create_access_token
from src.shared.exceptions import ConflictException, ForbiddenException, UnauthorizedException

import pytest
from jose import jwt


# ---------------------------------------------------------------------------
# Tests para create_user
# ---------------------------------------------------------------------------

class TestCreateUser:
    def test_creacion_exitosa(self, db_session):
        user_data = schemas.UserCreate(email="test@example.com", password="secret123", full_name="Test User")
        user = commands.create_user(db_session, user_data)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True

    def test_password_hasheado(self, db_session):
        user_data = schemas.UserCreate(email="hash@example.com", password="secret123", full_name="Hash User")
        user = commands.create_user(db_session, user_data)

        assert user.hashed_password != "secret123"
        assert pwd_context.verify("secret123", user.hashed_password)

    def test_email_duplicado_lanza_conflict(self, db_session):
        user_data = schemas.UserCreate(email="dup@example.com", password="secret123", full_name="First")
        commands.create_user(db_session, user_data)

        with pytest.raises(ConflictException):
            commands.create_user(db_session, user_data)


# ---------------------------------------------------------------------------
# Tests para authenticate_user
# ---------------------------------------------------------------------------

class TestAuthenticateUser:
    def _create_user(self, db_session, email="auth@example.com", password="secret123", is_active=True):
        user_data = schemas.UserCreate(email=email, password=password, full_name="Auth User")
        user = commands.create_user(db_session, user_data)
        if not is_active:
            user.is_active = False
            db_session.commit()
            db_session.refresh(user)
        return user

    def test_credenciales_correctas(self, db_session):
        self._create_user(db_session)
        user = commands.authenticate_user(db_session, "auth@example.com", "secret123")

        assert user.email == "auth@example.com"

    def test_password_incorrecto_lanza_unauthorized(self, db_session):
        self._create_user(db_session)

        with pytest.raises(UnauthorizedException):
            commands.authenticate_user(db_session, "auth@example.com", "wrongpassword")

    def test_email_inexistente_lanza_unauthorized(self, db_session):
        with pytest.raises(UnauthorizedException):
            commands.authenticate_user(db_session, "noexiste@example.com", "secret123")

    def test_usuario_inactivo_lanza_forbidden(self, db_session):
        self._create_user(db_session, is_active=False)

        with pytest.raises(ForbiddenException):
            commands.authenticate_user(db_session, "auth@example.com", "secret123")


# ---------------------------------------------------------------------------
# Tests para JWT
# ---------------------------------------------------------------------------

class TestJWT:
    def test_create_access_token_retorna_string(self):
        token = create_access_token({"sub": "1"})

        assert isinstance(token, str)

    def test_token_contiene_sub_correcto(self):
        token = create_access_token({"sub": "42"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["sub"] == "42"

    def test_token_contiene_exp(self):
        token = create_access_token({"sub": "1"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert "exp" in payload
