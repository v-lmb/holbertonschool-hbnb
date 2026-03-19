# HBnB - Part 3: Enhanced Backend with Authentication and Database Integration

## 📌 Overview

This is **Part 3** of the HBnB project. Building on the foundation from Part 2, this phase introduces:

- **JWT Authentication** for securing API endpoints
- **Role-Based Access Control (RBAC)** distinguishing admin vs. regular users
- **Database persistence** with SQLAlchemy + SQLite, replacing the in-memory storage
- **SQL scripts** for schema creation and initial data seeding
- **ER Diagram** documenting the database relationships

---

## ✅ What's New in Part 3

| Feature | Part 2 | Part 3 |
|---------|--------|--------|
| **Storage** | In-memory (dict) | SQLite via SQLAlchemy ORM |
| **Authentication** | None | JWT tokens (flask-jwt-extended) |
| **Password security** | None | Hashed with bcrypt |
| **Access control** | Open | RBAC (admin / regular user) |
| **Data persistence** | Lost on restart | Persisted in `development.db` |
| **User creation** | Public | Admin only |

---

## 📁 Project Structure

```
hbnb/
├── app/
│   ├── __init__.py             # Application factory + extensions (db, bcrypt, jwt)
│   ├── api/
│   │   └── v1/
│   │       ├── users.py        # User CRUD (JWT + RBAC protected)
│   │       ├── places.py       # Place CRUD (ownership checks)
│   │       ├── reviews.py      # Review CRUD (author checks)
│   │       ├── amenities.py    # Amenity CRUD (admin only for write)
│   │       └── auth.py         # Login endpoint + /protected test route
│   ├── models/
│   │   ├── base.py             # Abstract SQLAlchemy base (id, created_at, updated_at)
│   │   ├── user.py             # User model with password hashing
│   │   ├── place.py            # Place model with owner FK + amenity M2M
│   │   ├── review.py           # Review model with unique(user_id, place_id)
│   │   └── amenity.py          # Amenity model with unique name
│   ├── services/
│   │   └── facade.py           # Business logic hub (Facade pattern)
│   └── persistence/
│       ├── repository.py       # Abstract Repository + SQLAlchemyRepository
│       └── user_repository.py  # User-specific repo (email lookup)
├── SQL/
│   ├── schema.sql              # DDL script for all tables
│   └── seed.sql                # Admin user + initial amenities
├── tests/                      # Unit tests
├── er_diagram.md               # Mermaid.js ER diagram
├── run.py                      # Entry point (creates tables on startup)
├── config.py                   # App configuration (DB URI, JWT secret)
├── requirements.txt
├── .gitignore
└── README.md
```

### Key Files

| File | Role |
|------|------|
| `app/__init__.py` | Application Factory: creates and configures the Flask app, initializes SQLAlchemy, Bcrypt, and JWTManager |
| `app/api/v1/auth.py` | Login endpoint that returns a JWT token with `is_admin` claim |
| `app/persistence/repository.py` | SQLAlchemy-backed repository implementing the Repository interface |
| `app/persistence/user_repository.py` | User-specific repository with `get_user_by_email()` |
| `app/services/facade.py` | Central hub for all business logic, uses SQLAlchemy repositories |
| `app/models/base.py` | Abstract base model providing `id` (UUID), `created_at`, `updated_at` |
| `SQL/schema.sql` | SQL DDL script to create all tables with constraints |
| `SQL/seed.sql` | Seed data: admin user and initial amenities |

---

## ⚒️ Architecture

The application follows a **3-layer architecture**:

```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER              │
│   Flask-RESTX API + JWT Authentication  │
│   app/api/v1/                           │
├─────────────────────────────────────────┤
│         BUSINESS LOGIC LAYER            │
│   Models (SQLAlchemy ORM) + Facade      │
│   app/models/ + app/services/           │
├─────────────────────────────────────────┤
│         PERSISTENCE LAYER               │
│   SQLAlchemy Repository + SQLite DB     │
│   app/persistence/ + development.db     │
└─────────────────────────────────────────┘
```

#### Facade Pattern
All API endpoints communicate exclusively through a single `HBnBFacade` instance:
```
API → HBnBFacade → SQLAlchemy Repository → SQLite DB
```

#### Authentication Flow
```
Client → POST /auth/login (email + password)
Server → Verify with bcrypt → Create JWT (identity + is_admin claim)
Client → Include "Authorization: Bearer <token>" in subsequent requests
Server → Decode JWT → Check identity + admin status → Allow/Deny
```

---

## 🔐 Endpoint Protection Summary

| Endpoint | Auth | Who can access |
|----------|------|----------------|
| `POST /auth/login` | Public | Anyone |
| `GET /users/`, `GET /users/<id>` | Public | Anyone |
| `POST /users/` | JWT | Admin only |
| `PUT /users/<id>` | JWT | Own profile (no email/pwd) or Admin (full) |
| `GET /places/`, `GET /places/<id>` | Public | Anyone |
| `POST /places/` | JWT | Authenticated users |
| `PUT /places/<id>` | JWT | Owner or Admin |
| `GET /amenities/`, `GET /amenities/<id>` | Public | Anyone |
| `POST /amenities/`, `PUT /amenities/<id>` | JWT | Admin only |
| `GET /reviews/`, `GET /reviews/<id>` | Public | Anyone |
| `POST /reviews/` | JWT | Authenticated (not own place, max 1 per place) |
| `PUT /reviews/<id>` | JWT | Author or Admin |
| `DELETE /reviews/<id>` | JWT | Author or Admin |

---

## 📥 Installation & Setup

#### Prerequisites
- Python 3.8+
- pip

1. Clone the repository:
```bash
git clone https://github.com/v-lmb/holbertonschool-hbnb.git
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔎 Usage

1. Run the application:
```bash
python run.py
```
> The SQLite database (`development.db`) is automatically created on first startup.

2. Swagger documentation is accessible at:
```
http://127.0.0.1:5000/
```

---

## 🔁 Testing with cURL

### Step 1: Login (get a JWT token)

#### Admin login
```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin1234"}'
```
**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

> Save the token for use in authenticated requests below.

---

### Users

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/v1/users/` | Public | Retrieve all users |
| `GET` | `/api/v1/users/<user_id>` | Public | Retrieve a user by ID |
| `POST` | `/api/v1/users/` | Admin | Register a new user |
| `PUT` | `/api/v1/users/<user_id>` | JWT | Update a user |

#### Create a User (Admin only)
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -d '{
    "first_name": "Sherlock",
    "last_name": "Holmes",
    "email": "sherlock@detective.com",
    "password": "elementary"
  }'
```
**Response (201):**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "Sherlock",
  "last_name": "Holmes",
  "email": "sherlock@detective.com"
}
```

> Note: The password is **never** returned in any API response.

---

### Amenities

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/v1/amenities/` | Public | Retrieve all amenities |
| `GET` | `/api/v1/amenities/<id>` | Public | Retrieve an amenity |
| `POST` | `/api/v1/amenities/` | Admin | Create a new amenity |
| `PUT` | `/api/v1/amenities/<id>` | Admin | Update an amenity |

#### Create an Amenity (Admin only)
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -d '{"name": "Wi-Fi"}'
```

---

### Places

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/v1/places/` | Public | Retrieve all places |
| `GET` | `/api/v1/places/<id>` | Public | Retrieve a place |
| `POST` | `/api/v1/places/` | JWT | Create a place (owner = you) |
| `PUT` | `/api/v1/places/<id>` | JWT | Update (owner or admin) |

#### Create a Place (Authenticated)
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "title": "221B Baker Street",
    "description": "Mind the experiments. And the violin.",
    "price": 221.0,
    "latitude": 51.523767,
    "longitude": -0.158555
  }'
```
> `owner_id` is automatically extracted from the JWT token — no need to pass it.

**Validation Rules:**

| Field | Rule |
|-------|------|
| `title` | Required, max 100 characters |
| `price` | Required, positive number |
| `latitude` | Required, between -90 and 90 |
| `longitude` | Required, between -180 and 180 |

---

### Reviews

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/v1/reviews/` | Public | Retrieve all reviews |
| `GET` | `/api/v1/reviews/<id>` | Public | Retrieve a review |
| `POST` | `/api/v1/reviews/` | JWT | Create a review |
| `PUT` | `/api/v1/reviews/<id>` | JWT | Update (author or admin) |
| `DELETE` | `/api/v1/reviews/<id>` | JWT | Delete (author or admin) |

#### Create a Review (Authenticated)
```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "text": "Amazing place, highly recommended!",
    "rating": 5,
    "place_id": "<place_id>"
  }'
```
> `user_id` is automatically extracted from the JWT token.

**Review constraints:**
- You **cannot** review your own place
- You **cannot** review the same place twice
- Rating must be an integer between 1 and 5

---

## 🗄️ Database

### ER Diagram

See [er_diagram.md](er_diagram.md) for the full Mermaid.js Entity-Relationship diagram.

**Relationships:**
- **User → Place**: One-to-many (a user owns multiple places)
- **User → Review**: One-to-many (a user writes multiple reviews)
- **Place → Review**: One-to-many (a place has multiple reviews)
- **Place ↔ Amenity**: Many-to-many (via `place_amenity` junction table)

### SQL Scripts

- `SQL/schema.sql` — Creates all tables with constraints and foreign keys
- `SQL/seed.sql` — Inserts the admin user (`admin@hbnb.io` / `admin1234`) and 3 initial amenities (WiFi, Swimming Pool, Air Conditioning)

---

## 📘 Resources
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Bcrypt Documentation](https://flask-bcrypt.readthedocs.io/en/latest/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Facade Design Pattern](https://refactoring.guru/design-patterns/facade/python/example)
- [Testing REST APIs with cURL](https://everything.curl.dev/)

---

## 👥 Authors
The Incredible [Victor](https://github.com/victormonnot) and Little [Virginie](https://github.com/v-lmb)

---
