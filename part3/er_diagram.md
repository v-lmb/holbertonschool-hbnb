# HBnB Database — Entity-Relationship Diagram

## ER Diagram

```mermaid
erDiagram
    User {
        string id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    Place {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
        datetime created_at
        datetime updated_at
    }

    Review {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
        datetime created_at
        datetime updated_at
    }

    Amenity {
        string id PK
        string name
        datetime created_at
        datetime updated_at
    }

    Place_Amenity {
        string place_id FK
        string amenity_id FK
    }

    User ||--o{ Place : "owns"
    User ||--o{ Review : "writes"
    Place ||--o{ Review : "has"
    Place ||--o{ Place_Amenity : "has"
    Amenity ||--o{ Place_Amenity : "belongs to"
```

## Relationships

| Relation | Type | Description |
|----------|------|-------------|
| User → Place | One-to-Many | Un utilisateur peut posséder plusieurs places |
| User → Review | One-to-Many | Un utilisateur peut écrire plusieurs reviews |
| Place → Review | One-to-Many | Une place peut avoir plusieurs reviews |
| Place ↔ Amenity | Many-to-Many | Via la table d'association `Place_Amenity` |

## Constraints

- `User.email` : **UNIQUE** — pas de doublons
- `Review (user_id, place_id)` : **UNIQUE** — un user ne peut reviewer une place qu'une seule fois
- `Place_Amenity (place_id, amenity_id)` : **Composite Primary Key**
- `Review.rating` : **CHECK** entre 1 et 5
