# HBnB — Part 4: Web Client

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange)
![JWT](https://img.shields.io/badge/Auth-JWT-green)
![License](https://img.shields.io/badge/License-MIT-purple)

A full-stack property rental platform built as the final part of the HBnB project at Holberton School. The backend is a REST API built with Flask-RESTX, and the frontend is a vanilla JS + HTML/CSS web client served as static files.

The app follows a **Victorian mystery aesthetic** — properties are styled as historic estates, manor houses, and enigmatic retreats across London, Paris, Normandy, and beyond.

---

## Features

### Core
- User registration & login with JWT authentication
- Browse properties with live price and country filters
- View property details: description, amenities, photo gallery, interactive map
- Submit and read reviews (one per user per place)
- Auth-gated actions: add review redirects to login if unauthenticated

### Extras
- **Victorian theme** — curated seed data with period-accurate names, locations, and descriptions
- **Photo lightbox** on place pages
- **Interactive map** via Leaflet.js
- **Mystery page** (`/static/mystery.html`) — a hidden case file unlockable via an easter egg
- **Custom 404 page** with theme-consistent design
- **Profile, messages, and my places** pages
- Seed script to populate the database with demo data

---

## Architecture

```
static/               ← HTML/CSS/JS frontend (vanilla)
app/api/v1/           ← Flask-RESTX endpoints (Swagger at /)
app/services/         ← HBnBFacade (all business logic)
app/persistence/      ← SQLAlchemyRepository + UserRepository
app/models/           ← SQLAlchemy ORM models
```

**Patterns used:** App factory, Facade, Repository.

---

## Models

| Model | Key fields |
|-------|-----------|
| `User` | `email`, `password` (bcrypt), `is_admin` |
| `Place` | `title`, `price`, `latitude`, `longitude`, `owner_id` |
| `Review` | `text`, `rating`, `user_id`, `place_id` (unique together) |
| `Amenity` | `name` |

Place ↔ Amenity: many-to-many. Place → Review: cascade delete.

---

## Getting started

```bash
# Install dependencies
pip install -r requirements.txt

# Populate the database with Victorian demo data
python seed.py

# Run the app
python run.py
# → http://localhost:5000
# → Swagger UI at http://localhost:5000/api/v1/
```

### Demo credentials (after seed)

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@hbnb.io` | `admin1234` |
| User | `watson@baker.st` | `watson1234` |

---

## API overview

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/v1/auth/login` | — |
| GET | `/api/v1/places` | optional |
| GET | `/api/v1/places/<id>` | optional |
| POST | `/api/v1/places` | required |
| PUT | `/api/v1/places/<id>` | owner / admin |
| POST | `/api/v1/reviews` | required |
| PUT/DELETE | `/api/v1/reviews/<id>` | author / admin |
| GET/POST | `/api/v1/amenities` | GET public, POST admin |
| GET/POST | `/api/v1/users` | GET public, POST admin |

Full interactive documentation available at `/api/v1/` (Swagger UI).

---

## Project structure

```
part4/
├── app/
│   ├── __init__.py         ← App factory, error handlers
│   ├── api/v1/             ← Blueprints (auth, users, places, reviews, amenities)
│   ├── models/             ← ORM models (base, user, place, review, amenity)
│   ├── persistence/        ← Repositories
│   └── services/facade.py  ← Business logic
├── static/                 ← Frontend (HTML, CSS, JS, images)
├── config.py
├── run.py
├── seed.py
└── requirements.txt
```

---

## Author

**Virginie** — Holberton School, Part 4 (Web Client)
