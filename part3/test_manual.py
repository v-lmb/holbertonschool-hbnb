# test_manual.py — à la racine du projet (hbnb/)
# Lance avec : python test_manual.py

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

print("=" * 50)
print("TEST 1 : Création d'un User valide")
print("=" * 50)

user = User("Alice", "Dupont", "alice@test.com", "secret123")
print(f"✅ User créé : {user.first_name} {user.last_name}")
print(f"   ID       : {user.id}")
print(f"   Email    : {user.email}")
print(f"   Admin    : {user.is_admin}")
print(f"   Dict     : {user.to_dict()}")
print()

print("=" * 50)
print("TEST 2 : Email invalide → doit lever ValueError")
print("=" * 50)

try:
    bad_user = User("Bob", "Martin", "pas-un-email", "secret123")
    print("❌ Erreur : aurait dû lever une ValueError !")
except ValueError as e:
    print(f"✅ ValueError levée correctement : {e}")
print()

print("=" * 50)
print("TEST 3 : Création d'une Amenity")
print("=" * 50)

wifi = Amenity("WiFi")
piscine = Amenity("Piscine")
print(f"✅ Amenity créée : {wifi.name} (id: {wifi.id})")
print(f"✅ Amenity créée : {piscine.name} (id: {piscine.id})")
print()

print("=" * 50)
print("TEST 4 : Création d'un Place")
print("=" * 50)

place = Place(
    title="Belle villa avec vue mer",
    price=150.0,
    latitude=43.2965,
    longitude=5.3698,
    owner=user,            # ← on passe l'objet user directement
    description="Magnifique logement à deux pas de la plage"
)

# Ajout des amenities
place.add_amenity(wifi)
place.add_amenity(piscine)

print(f"✅ Place créée : {place.title}")
print(f"   Prix       : {place.price}€/nuit")
print(f"   Amenities  : {[a.name for a in place.amenities]}")
print()

print("=" * 50)
print("TEST 5 : Latitude hors bornes → ValueError")
print("=" * 50)

try:
    bad_place = Place("Titre", "Desc", 100, 95.0, 5.0, user.id)
    print("❌ Erreur : aurait dû lever une ValueError !")
except ValueError as e:
    print(f"✅ ValueError levée correctement : {e}")
print()

print("=" * 50)
print("TEST 6 : Création d'une Review")
print("=" * 50)

review = Review(
    text="Logement parfait, je recommande vivement !",
    rating=5,
    place=place,
    user=user
)
print(f"✅ Review créée : '{review.text[:30]}...'")
print(f"   Note    : {review.rating}/5")
print()

print("=" * 50)
print("TEST 7 : Note invalide → ValueError")
print("=" * 50)

try:
    bad_review = Review("Texte", 6, place.id, user.id)
    print("❌ Erreur : aurait dû lever une ValueError !")
except ValueError as e:
    print(f"✅ ValueError levée correctement : {e}")
print()

print("=" * 50)
print("TEST 8 : Mise à jour d'un User (update)")
print("=" * 50)

print(f"Avant : {user.first_name} / {user.email}")
user.update({"first_name": "Alicia", "last_name": "Martin"})
print(f"Après : {user.first_name} / {user.last_name}")
print(f"✅ Mise à jour réussie")
print()

print("=" * 50)
print("🎉 Tous les tests sont passés !")
print("=" * 50)
