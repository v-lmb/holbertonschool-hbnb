from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """
    Base class for all models.
    __abstract__ = True means SQLAlchemy does NOT create a table for BaseModel,
    but the columns defined here are inherited by child classes.
    """
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def save(self):
        """
        Refresh the updated_at to the current date & time
        """
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary
        data: dict, attribute names and values
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
