from app import db
from app.models.base import BaseModel


# --- Many-to-many association table Place <-> Amenity ---
# This is an intermediate table containing only the FKs.
# SQLAlchemy manages it automatically via the 'secondary' parameter.
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36),
              db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36),
              db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    """
    Represents a rental place.
    """
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # FK to the users table (the owner)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                         nullable=False)

    # --- Relationships ---
    # One-to-many: a Place has multiple Reviews
    reviews = db.relationship('Review', backref='place', lazy=True,
                              cascade='all, delete-orphan')
    # Many-to-many: a Place has multiple Amenities and vice versa
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, title, price, latitude, longitude, owner_id,
                 description=None, **kwargs):
        """
        Initialize a new place instance
        """
        super().__init__(**kwargs)
        self.title = self._validate_title(title)
        self.description = description
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner_id = owner_id

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
        if not isinstance(longitude, (int, float)):
            raise ValueError("longitude must be between -180 and 180")
        if not -180 <= longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")
        return float(longitude)

    def add_review(self, review):
        """Add a review to this place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

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
            "owner_id": self.owner_id,
            "amenities": [{"id": a.id, "name": a.name}
                          for a in self.amenities],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
