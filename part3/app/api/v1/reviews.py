from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
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
        Create a new review.
        Requires JWT.
        - user_id is extracted from the token
        - Cannot review your own place
        - Cannot review the same place twice
        """
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user

        # Check that the place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404

        # Cannot review your own place
        if place.owner.id == current_user:
            return {"error": "You cannot review your own place"}, 400

        # Cannot review the same place twice
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
        """
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        """
        Update existing review.
        Requires JWT. Only the author can update (admin bypass).
        """
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        # Authorization: only the author or an admin
        if not is_admin and review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            review = facade.update_review(review_id, api.payload)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        """
        Delete review by his ID.
        Requires JWT. Only the author can delete (admin bypass).
        """
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        # Authorization: only the author or an admin
        if not is_admin and review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
