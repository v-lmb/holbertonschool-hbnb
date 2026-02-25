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

---

## 🧾 Learning Objectives

The aim of this stage of the project is to develop the following skills::

- **Modular Design and Architecture**  
- **API Development with Flask and flask-restx**
- **Business Logic Implementation**
- **Data Serialization and Composition Handling**
- **Testing and Debugging**

---

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
---

## 🔁 Flowchart

(Optional but recommended)

You can add:

* an image
* or an ASCII diagram

Example:

```
input → parse → process → output
```

---

## ⚙️ Prerequisites

* GCC compiler (GNU89)
* Linux environment (recommended)
* Git

---

## 📥 Installation

1. Clone the repository:

```bash
git clone <repository_url>
```

2. Navigate to the project directory:

```bash
cd project_name
```

---

## 🛠 Compilation

Explain how to compile the project.

Example:

```bash
gcc -Wall -Werror -Wextra -pedantic -std=gnu89 *.c -o program_name
```

---

## 💡 Usage

Explain how to run the program.

### Example

```bash
./program_name
```

If relevant, show:

* interactive mode
* non-interactive mode

---

## 🔒 Allowed Functions

List **explicitly** the authorized functions and system calls.

Example:

* `malloc`
* `free`
* `write`
* `fork`
* `execve`

---

## ⚠️ Limitations

Be honest and precise.

Example:

* No pipes handling
* No redirections
* No wildcard expansion

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
The incredible ones
[Victor](https://github.com/victormonnot) | [Virginie](https://github.com/v-lmb) 

---
