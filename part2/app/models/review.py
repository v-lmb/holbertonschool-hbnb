from app.models.base import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text or not isinstance(text, str):
            raise ValueError("text is required")

        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("rating must be an integer between 1 and 5")

        if not isinstance(place, Place):
            raise ValueError("place must be a Place")

        if not isinstance(user, User):
            raise ValueError("user must be a User")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        place.add_review(self)
