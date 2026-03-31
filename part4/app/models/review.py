from app import db
from app.models.base import BaseModel


class Review(BaseModel):
    """
    Represents a review.
    UNIQUE constraint on (user_id, place_id) to prevent
    a user from reviewing the same place twice.
    """
    __tablename__ = 'reviews'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id',
                            name='unique_user_place_review'),
    )

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # FK vers les tables users et places
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                        nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'),
                         nullable=False)

    def __init__(self, text, rating, user_id, place_id, **kwargs):
        """
        Initialize a new review instance
        """
        super().__init__(**kwargs)

        if not text or not isinstance(text, str):
            raise ValueError("text is required")

        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("rating must be an integer between 1 and 5")

        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def to_dict(self):
        """
        Serialize the review instance to a dictionary
        """
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
