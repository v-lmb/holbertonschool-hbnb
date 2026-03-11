from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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
    @jwt_required()
    def post(self):
        """
        Create a new review
        Return: dict
        code 201 if the review is created
        code 400 if validation fails
        """
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404
        if place.owner.id == current_user:
            return {"error": "You cannot review your own place"}, 400
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        if existing_reviews:
            for r in existing_reviews:
                if r.user.id == current_user:
                    return {"error": "You have already reviewed this place"}, 400

        try:
            review = facade.create_review(review_data)
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
    @jwt_required()
    def put(self, review_id):
        """
        Update existing review
        review_id : str, UUID of the review
        Return: dict
        code 200 with review data
        code 404 if not found
        """
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        review = facade.update_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user.id != current_user:
            return {"error": "Unauthorized action"}, 403

        try:
            review = facade.update_review(review_id, api.payload)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        """
        Delete review by his ID
        review_id : str, UUID of the review
        Return: dict
        code 200 with review data
        code 404 if not found
        """
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if not is_admin and review.user.id != current_user:
            return {"error": "Unauthorized action"}, 403

        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
