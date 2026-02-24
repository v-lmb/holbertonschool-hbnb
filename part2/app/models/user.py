import re
from app.models.base import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        self.first_name = self._validate_name(first_name, "first_name")
        self.last_name = self._validate_name(last_name, "last_name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin

    def _validate_name(self, value, field_name):
        if not value or not isinstance(value, str):
            raise ValueError(f"{field_name} is required")
        if len(value) > 50:
            raise ValueError(f"{field_name} must be at most 50 characters")
        return value

    def _validate_email(self, email):
        if not email or not isinstance(email, str):
            raise ValueError("email is required")

        regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(regex, email):
            raise ValueError("invalid email format")

        return email

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
