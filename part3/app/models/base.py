import uuid
from datetime import datetime


class BaseModel:
    """
    Base class
    """
    def __init__(self):
        """
        Initialize a new Base instance"
        id : str, UUID
        created_at : date and time of creation
        update_at : date and time of the last update
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Refresh the update_at to the current date & time
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary
        data: dict, attribute names and values
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
