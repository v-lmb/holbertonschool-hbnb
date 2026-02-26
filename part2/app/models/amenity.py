from app.models.base import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity
    Inherits from Base
    """
    def __init__(self, name):
        """
        Initialize a new amenity instance
        name: str
        Raises: ValueError
        """
        super().__init__()

        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required")
        if len(name) > 50:
            raise ValueError("Amenity name must be at most 50 characters")

        self.name = name
