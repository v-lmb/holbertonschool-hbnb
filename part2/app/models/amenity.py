from app.models.base import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

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
