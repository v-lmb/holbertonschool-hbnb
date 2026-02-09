# Holberton School - HBnB

## 📌 Overview

Description

---

##  Architecture Overview

### Layered Architecture

Yhe application follows a **3-tier architecture** that ensures modularity, testability, and maintainability:

```
┌─────────────────────────────────────────┐
│     PRESENTATION LAYER (API)            │
│  • REST API Endpoints                   │
│  • Request/Response Handling            │
│  • Input Validation                     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     BUSINESS LOGIC LAYER                │
│  ┌────────────────────────────────┐     │
│  │         FACADE PATTERN         │     │
│  │  (Unified Interface)           │     │
│  └────────────┬───────────────────┘     │
│               │                         │
│  ┌────────────┴───────────────────┐     │
│  │  • UserService                 │     │
│  │  • PlaceService                │     │
│  │  • ReviewService               │     │
│  │  • AmenityService              │     │
│  └────────────────────────────────┘     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     PERSISTENCE LAYER                   │
│  • Database Management                  │
│  • Repository Pattern                   │
│  • Data Access Objects (DAO)            │
└─────────────────────────────────────────┘
```

###  Description des 3 couches
presentatins
business logic
persistence

###  comment ça communique entre ces couches

---

##  Diagram de class

+ explication des classes
| Feature | Description |
|---------|-------------|
|  **User** | Complete user registration, authentication, and profile management |
|  **Place** | Create, update, and browse property listings with geolocation |
|  **Review** | Submit and view ratings and reviews for properties |
|  **Amenity** | Flexible amenity system for property features |
|  **Base** |  |

###  relations entre classes qui à quoi etc

---
##  Diagramme Sequence

###  API 1 - User Registration
Montrer les interactions entre les 3 couches pour chaque appel API

###  API 2 - Place Creation
Montrer les interactions entre les 3 couches pour chaque appel API

###  API 3 - Review Submission
Montrer les interactions entre les 3 couches pour chaque appel API

###  API 4 - Fetch Places List 
Montrer les interactions entre les 3 couches pour chaque appel API

---

## Technologie & Toll Used

- **Mermaid.js** - Diagrams
- **UML Standards** - sequence diagram

---

## Authors

| Name | GitHub |
|------|--------|
| Victor | [GitHub](https://github.com/victormonnot) |
| Virginie | [GitHub](https://github.com/v-lmb) |

---
