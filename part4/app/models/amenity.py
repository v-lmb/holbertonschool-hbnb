from app import db
from app.models.base import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity.
    Le nom est unique (pas 2 amenities "WiFi").
    """
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name, **kwargs):
        """
        Initialize a new amenity instance
        name: str
        Raises: ValueError
        """
        super().__init__(**kwargs)

        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required")
        if len(name) > 50:
            raise ValueError("Amenity name must be at most 50 characters")

        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
