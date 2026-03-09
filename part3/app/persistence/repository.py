from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract base class defining the interface for all repositories
    """
    @abstractmethod
    def add(self, obj):
        """
        Store a new object in the repository
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its unique identifier
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects stored in the repository
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an existing object with new data
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object from the repository
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve the first object matching a specific attribute value
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository interface
    """
    def __init__(self):
        """
        Initialize an empty in-memory storage dictionary
        """
        self._storage = {}

    def add(self, obj):
        """
        Store an object using its ID as the key
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieve an object by its ID
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Retrieve all stored objects as a list
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an object's attributes from a dictionary
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Remove an object from storage
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Find the first object matching a specific attribute value
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
