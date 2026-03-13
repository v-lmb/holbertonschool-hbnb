from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace("places", description="Place operations")

# Model for amenity
amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(),
    "name": fields.String()
})

# Model for owner of a place
user_model = api.model("PlaceUser", {
    "id": fields.String(),
    "first_name": fields.String(),
    "last_name": fields.String(),
    "email": fields.String()
})

# Model for review
review_model = api.model("PlaceReview", {
    "id": fields.String(),
    "text": fields.String(),
    "rating": fields.Integer(),
    "user_id": fields.String()
})

# Model for place input validation and doc
place_model = api.model("Place", {
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "amenities": fields.List(fields.String)
})


@api.route("/")
class PlaceList(Resource):
    """
    Ressource for places collection
    """

    @api.expect(place_model)
    @jwt_required()
    def post(self):
        """
        Create a new place.
        Requires JWT: owner_id is automatically set
        to the authenticated user (extracted from token).
        """
        current_user = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user  # Owner = authenticated user

        try:
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        """
        Retrieve all places.
        Public.
        """
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    """
    Ressource for a single place
    """

    def get(self, place_id):
        """
        Retrieve place with his ID.
        Public.
        """
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @jwt_required()
    def put(self, place_id):
        """
        Update an existing place.
        Requires JWT.
        Only the owner can update (admin bypass).
        """
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Ownership check (admin bypass)
        if not is_admin and place.owner.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            place = facade.update_place(place_id, api.payload)
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    """
    Retrieve all reviews for a specific place.
    """

    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [r.to_dict() for r in reviews], 200
