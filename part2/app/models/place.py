from app.models.base import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """
    Represents a rental place
    """
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        """
        Initialize a new place instance
        """
        super().__init__()

        self.title = self._validate_title(title)
        self.description = description
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = self._validate_owner(owner)

        self.reviews = []
        self.amenities = []

    def _validate_title(self, title):
        """
        Validate the title of the place
        """
        if not title or not isinstance(title, str):
            raise ValueError("title is required")
        if len(title) > 100:
            raise ValueError("title must be at most 100 characters")
        return title

    def _validate_price(self, price):
        """
        Validate the price per night
        """
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be a positive number")
        return float(price)

    def _validate_latitude(self, latitude):
        """
        Validate the GPS latitude coordinate
        """
        if not isinstance(latitude, (int, float)) or not -90 <= latitude <= 90:
            raise ValueError("latitude must be between -90 and 90")
        return float(latitude)

    def _validate_longitude(self, longitude):
        """
        Validate the GPS longitude coordinate
        """
        if not isinstance(longitude, (int, float)) or not -180 <= longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")
        return float(longitude)

    def _validate_owner(self, owner):
        """
        Validate that the owner is a user instance
        """
        if not isinstance(owner, User):
            raise ValueError("owner must be a User")
        return owner

    def add_review(self, review):
        """
        Add a review to this place
        """
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """
        Add an amenity to this place
        """
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def to_dict(self):
        """
        Serialize the place instance to a dictionary
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict(),
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews": [r.to_dict() for r in self.reviews],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
