# HBnB - Part 2

## 📌 Overview

In this phase of the **HBnB project**, you will begin implementing the application based on the architecture defined previously. You will develop the Presentation and Business Logic layers using Python and Flask, creating the project structure, business classes, and API endpoints.

The goal is to make the architecture functional by implementing user, location, review, and equipment management in accordance with REST best practices. JWT authentication and role management will be addressed later with **Flask** and **flask-restx**.

---

## ✅ Objectives

The goal of this project is to enable you to :

- Set Up the Project Structure:
  - Organize the project into a modular architecture, following best practices for Python and Flask applications.
  - Create the necessary packages for the Presentation and Business Logic layers.
  
- Implement the Business Logic Layer:
  - Develop the core classes for the business logic, including User, Place, Review, and Amenity entities.
  - Implement relationships between entities and define how they interact within the application.
  - Implement the facade pattern to simplify communication between the Presentation and Business Logic layers.
 
- Build RESTful API Endpoints:
  - Implement the necessary API endpoints to handle CRUD operations for Users, Places, Reviews, and Amenities.
  - Use flask-restx to define and document the API, ensuring a clear and consistent structure.
  - Implement data serialization to return extended attributes for related objects. For example, when retrieving a Place, the API should include details such as the owner’s first_name, last_name, and relevant amenities.
    
- Test and Validate the API:
  - Ensure that each endpoint works correctly and handles edge cases appropriately.
  - Use tools like Postman or cURL to test your API endpoints.


## 🧾 Learning Objectives

The aim of this stage of the project is to develop the following skills::

- **Modular Design and Architecture**  
- **API Development with Flask and flask-restx**
- **Business Logic Implementation**
- **Data Serialization and Composition Handling**
- **Testing and Debugging**


## 📁 Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── à compléter
│   │   ├── à compléter bis
│   │   └── à compléter bis bis
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

### Key Files

| File | Role |
|------|------|
| `app/__init__.py` | Creates the Flask app and registers all namespaces |
| `app/services/facade.py` | Central hub for all business logic operations |
| `app/persistence/repository.py` | In-memory storage (will be replaced by SQL in Part 3) |
| `app/models/base.py` | Provides `id` (UUID), `created_at`, `updated_at` to all models |


---

## ⚒️​ Architecture

The application follows a 3-layer architecture:
- PRESENTATION LAYER
  - Flask-RESTX API endpoints
  - app/api/v1/

- BUSINESS LOGIC LAYER
  - Models: User, Place, Review
  - Amenity + Facade pattern
  - app/models/ + app/services/ 

- PERSISTENCE LAYER
  - In-memory repository
  - app/persistence/

#### Facade Pattern
All API endpoints communicate exclusively through a single HBnBFacade instance, which acts as the unique entry point to the business logic:
```
API → HBnBFacade → Models / Repository
```

---

## 📥 Installation & Setup

#### Prerequisites
- Python 3.8+
- pip

1. Clone the repository:
```bash
git clone https://github.com/v-lmb/holbertonschool-hbnb.git
```

2. Create a virtual environnement (recommended):
```bash
python3 -m venv venv  
source venv/bin/activate  
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔎 Usage
1. Run the application using this command:
```bash
python run.py
```

2. Open a browser and visit the localhost at:
```
http://127.0.0.1:5000
```
   
4. Swagger documentation is accessible at:
```
http://127.0.0.1:5000/api/v1/
```

---

## 🔁 Tests with cURL

### Users
> 💡 All endpoints are prefixed with `/api/v1/`

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/api/v1/users/` | Register a new user | 201, 400 |
| `GET` | `/api/v1/users/` | Retrieve all users | 200 |
| `GET` | `/api/v1/users/<user_id>` | Retrieve a user by ID | 200, 404 |
| `PUT` | `/api/v1/users/<user_id>` | Update a user | 200, 400, 404 |


#### Create a User
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Sherlock",
    "last_name": "Holmes",
    "email": "sherlock.holmes@detective.com"
  }'
```
**Response (201):**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "Sherlock",
  "last_name": "Holmes",
  "email": "sherlock.holmes@detective.com"
}
```
#### Get All Users
```bash
curl http://127.0.0.1:5000/api/v1/users/
```

#### Get User by ID
```bash
curl http://127.0.0.1:5000/api/v1/users/<user_id>
```

#### Update a User
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/users/<user_id> \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Watson",
    "email": "john.watson@armychronicles.com"
  }'
```
> 💡 Use a **valid user_id**

**Response (200):**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "John",
  "last_name": "Watson",
  "email": "john.watson@armychronicles.com"
}
```

---
   
### Amenity

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/api/v1/amenities/` | Create a new amenity | 201, 400 |
| `GET` | `/api/v1/amenities/` | Retrieve all amenities | 200 |
| `GET` | `/api/v1/amenities/<amenity_id>` | Retrieve an amenity by ID | 200, 404 |
| `PUT` | `/api/v1/amenities/<amenity_id>` | Update an amenity | 200, 400, 404 |


#### Create an Amenity
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```
**Response (201):**
```json
{
  "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "Wi-Fi"
}
```

#### Update an Amenity
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/<amenity_id> \
  -H "Content-Type: application/json" \
  -d '{"name": "Air Conditioning"}'
```
> 💡 Use a **valid amenity_id**

**Response (200):**
```json
{
  "message": "Amenity updated successfully"
}
```

---
### Places 

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/api/v1/places/` | Create a new place | 201, 400 |
| `GET` | `/api/v1/places/` | Retrieve all places | 200 |
| `GET` | `/api/v1/places/<place_id>` | Retrieve a place by ID | 200, 404 |
| `PUT` | `/api/v1/places/<place_id>` | Update a place | 200, 400, 404 |
| `GET` | `/api/v1/places/<place_id>/reviews` | Get all reviews for a place | 200, 404 |

#### Create a Place
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "221B Baker Street",
    "description": "Mind the experiments. And the violin.",
    "price": 221.0,
    "latitude": 51.523767,
    "longitude": -0.158555,
    "owner_id": "<user_id>"
  }'
```
> 💡 Use a **valid user_id**

**Response (201):**
```json
{
  "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "221B Baker Street",
  "description": "Mind the experiments. And the violin.",
  "price": 221.0,
  "latitude": 51.523767,
  "longitude": -0.158555,
  "owner": {
    "id": "<user_id>",
    "first_name": "Sherlock",
    "last_name": "Holmes",
    "email": "sherlock.holmes@detective.com"
  },
  "amenities": [],
  "reviews": []
}
```

#### ⚠️​ Validation Rules for Places

| Field | Rule |
|-------|------|
| `title` | Required, max 100 characters |
| `price` | Required, must be a positive number |
| `latitude` | Required, must be between -90 and 90 |
| `longitude` | Required, must be between -180 and 180 |
| `owner_id` | Required, must reference an existing user |

---
   
### Reviews

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/api/v1/reviews/` | Create a new review | 201, 400 |
| `GET` | `/api/v1/reviews/` | Retrieve all reviews | 200 |
| `GET` | `/api/v1/reviews/<review_id>` | Retrieve a review by ID | 200, 404 |
| `PUT` | `/api/v1/reviews/<review_id>` | Update a review | 200, 400, 404 |
| `DELETE` | `/api/v1/reviews/<review_id>` | Delete a review | 200, 404 |

> ⚠️ `DELETE` is only implemented for reviews in this part of the project.

#### Create a Review
```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Amazing place, highly recommended!",
    "rating": 5,
    "user_id": "<user_id>",
    "place_id": "<place_id>"
  }'
```
> 💡 Use a **valid user_id & place_id**

**Response (201):**
```json
{
  "id": "4fa85f64-5717-4562-b3fc-2c963f66afa6",
  "text": "Amazing place, highly recommended!",
  "rating": 5,
  "user_id": "<user_id>",
  "place_id": "<place_id>"
}
```

#### Delete a Review
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review_id>
```
> 💡 Use a **valid review_id**

**Response (200):**
```json
{
  "message": "Review deleted successfully"
}
```

#### ⚠️ Validation Rules for Reviews

| Field | Rule |
|-------|------|
| `text` | Required, cannot be empty |
| `rating` | Required, integer between 1 and 5 |
| `user_id` | Required, must reference an existing user |
| `place_id` | Required, must reference an existing place |

---

## 📘 Ressources
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)
- [Facade Design Pattern in Python](https://refactoring.guru/design-patterns/facade/python/example)
- [Python OOP Basics](https://realpython.com/python3-object-oriented-programming/)
- [Designing Classes and Relationships:](https://docs.python.org/3/tutorial/classes.html)
- [Why You Should Use UUIDs](https://datatracker.ietf.org/doc/html/rfc4122)
- [Testing REST APIs with cURL](https://everything.curl.dev/)
- [Designing RESTful APIs](https://restfulapi.net/)

---

## 👥 Authors
The Incredible [Victor](https://github.com/victormonnot) and Little [Virginie](https://github.com/v-lmb) 

---
