from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """
    Ressource for the amenities collection
    """
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new amenity
        Return: dict
        code 201 with created amenity
        code 400 if validation fails
        """
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve all amenities
        Return: list
        code 200 with a list of all amenity disctionnaries
        empty list if no amenities exist
        """
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Ressource for a single amenity
    """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Retrieve an amenity with his ID
        amenity_id : str, UUID
        Return: disct
        code 200 with amenity data
        code 404 if not found
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an existing amenity
        amenity_id : str, UUID
        Return: disct
        code 200 if success
        code 404 if not found
        code 400 if data is invalid
        """
        amenity_data = api.payload
        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            return {'message': 'Amenity updated successufully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
