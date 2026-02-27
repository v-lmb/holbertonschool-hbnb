from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """
    Central hub for all business logic operations
    """
    def __init__(self):
        """
        Initialize the facade with one repository per entity
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ====== USER ======
    def create_user(self, user_data):
        """
        Create and store a new user
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by their unique ID
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # ====== PLACE ======
    def create_place(self, data):
        """
        Create and store a new place
        """
        owner = self.user_repo.get(data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=data["title"],
            description=data.get("description"),
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner=owner
        )

        for amenity_id in data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a place by its unique ID
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieve all registered places
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        """
        Update an existing place's attributes
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        place.update(data)
        return place

    # ====== REVIEW ======
    def create_review(self, data):
        """
        Create and store a new review
        """
        user = self.user_repo.get(data["user_id"])
        place = self.place_repo.get(data["place_id"])

        if not user or not place:
            raise ValueError("User or Place not found")

        review = Review(
            text=data["text"],
            rating=data["rating"],
            user=user,
            place=place
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by its unique ID
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews associated with a specific place
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, data):
        """
        Update an existing review's attributes
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None

        review.update(data)
        return review

    def delete_review(self, review_id):
        """
        Delete a review from the repository
        """
        review = self.review_repo.get(review_id)
        if not review:
            return False

        self.review_repo.delete(review_id)
        return True

    # ====== AMENITIES ======
    def create_amenity(self, amenity_data):
        """
        Create and store a new amenity
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by its unique ID
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all registered amenities
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity's attributes
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity
