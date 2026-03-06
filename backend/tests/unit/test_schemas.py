import pytest
from pydantic import ValidationError

from src.features.auth.schemas import UserCreate


class TestUserCreateSchema:
    def test_datos_validos(self):
        user = UserCreate(email="valid@example.com", password="secret123", full_name="Valid User")

        assert user.email == "valid@example.com"
        assert user.password == "secret123"
        assert user.full_name == "Valid User"

    def test_email_sin_arroba_lanza_error(self):
        with pytest.raises(ValidationError, match="email debe ser valido"):
            UserCreate(email="invalidemail", password="secret123", full_name="Test")

    def test_password_corto_lanza_error(self):
        with pytest.raises(ValidationError, match="password debe tener al menos 6 caracteres"):
            UserCreate(email="test@example.com", password="12345", full_name="Test")
