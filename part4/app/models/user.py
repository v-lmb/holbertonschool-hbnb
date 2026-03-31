import re
from app import db, bcrypt
from app.models.base import BaseModel


class User(BaseModel):
    """
    Represent a user.
    __tablename__ = 'users' maps this class to the SQL table 'users'.
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # --- Relationships (one-to-many) ---
    # A User can own multiple Places
    places = db.relationship('Place', backref='owner', lazy=True)
    # A User can write multiple Reviews
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password,
                 is_admin=False, **kwargs):
        """
        Initialize a new user instance.
        first_name: str, user's first name
        last_name: str, user's last name
        email: str, user's mail
        password: str, user's password (will be hashed)
        is_admin: bool, admin status, false by default
        Raises: ValueError
        """
        super().__init__(**kwargs)

        self.first_name = self._validate_name(first_name, "first_name")
        self.last_name = self._validate_name(last_name, "last_name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password):
        """
        Hash the password before storing it.
        bcrypt generates a unique salted hash on each call.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verify if the provided password matches the hashed password.
        """
        return bcrypt.check_password_hash(self.password, password)

    def _validate_name(self, value, field_name):
        """
        Validate a name field (first or last name)
        value: str, value to validate
        field_name: str, field name used in error message
        Return: validated name value
        Raises: ValueError
        """
        if not value or not isinstance(value, str):
            raise ValueError(f"{field_name} is required")
        if len(value) > 50:
            raise ValueError(f"{field_name} must be at most 50 characters")
        return value

    def _validate_email(self, email):
        """
        Validate a mail address format
        email: str, the email
        Return: validated mail
        Raises: ValueError
        """
        if not email or not isinstance(email, str):
            raise ValueError("email is required")
        regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(regex, email):
            raise ValueError("invalid email format")
        return email

    def to_dict(self):
        """
        Serialize the user instance to dictionnary
        Return: dict
        representation of the user
        The password is NEVER returned!
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
