from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True)
})


@api.route("/")
class ReviewList(Resource):
    """
    Ressources for the reviews collection
    """

    @api.expect(review_model)
    def post(self):
        """
        Create a new review
        Return: dict
        code 201 if the review is created
        code 400 if validation fails
        """
        try:
            review = facade.create_review(api.payload)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        """
        Retrieve all reviews
        Return : list
        code 200 with a list of all review disctionnaries
        empty list if no reviews
        """
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route("/<review_id>")
class ReviewResource(Resource):
    """
    Ressource for a single review
    """

    def get(self, review_id):
        """
        Retrieve a review with his ID
        review_id : str, UUID of the review
        Return: dict
        code 200 with review data
        code 404 if not found
        """
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    def put(self, review_id):
        """
        Update existing review
        review_id : str, UUID of the review
        Return: dict
        code 200 with review data
        code 404 if not found
        """
        review = facade.update_review(review_id, api.payload)
        if not review:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully"}, 200

    def delete(self, review_id):
        """
        Delete review by his ID
        review_id : str, UUID of the review
        Return: dict
        code 200 with review data
        code 404 if not found
        """
        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
