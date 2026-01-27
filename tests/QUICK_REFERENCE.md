# 🎯 QUICK REFERENCE - Najczęściej używane kody

## 🔑 Importy (na górze pliku testowego)

```python
from main import app, db, User, Cafe
from werkzeug.security import generate_password_hash
import pytest
```

---

## 👤 Tworzenie użytkownika w teście

```python
hashed_pw = generate_password_hash("password123", method='pbkdf2:sha256', salt_length=8)
user = User(email="test@example.com", password=hashed_pw, name="Test User")
db.session.add(user)
db.session.commit()
db.session.refresh(user)  # Odśwież aby mieć ID
```

---

## 🏪 Tworzenie kawiarni w teście

```python
cafe = Cafe(
    name="Test Cafe",
    map_url="https://maps.google.com/test",
    img_url="https://images.com/test.jpg",
    location="Warsaw",
    has_sockets=True,
    has_toilet=True,
    has_wifi=True,
    can_take_calls=False,
    seats="20-30",
    coffee_price="15 PLN",
    user_id=auth_user.id  # ID właściciela
)
db.session.add(cafe)
db.session.commit()
db.session.refresh(cafe)
```

---

## 🔐 Logowanie w teście

```python
response = client.post('/login', data={
    'email': 'test@example.com',
    'password': 'password123'
}, follow_redirects=True)
```

---

## 📝 Rejestracja w teście

```python
response = client.post('/register', data={
    'name': 'New User',
    'email': 'new@example.com',
    'password': 'password123',
    'confirm_password': 'password123'
}, follow_redirects=True)
```

---

## ➕ Dodawanie kawiarni w teście

```python
response = client.post('/add', data={
    "name": "My Cafe",
    "location": "Warsaw",
    "map_url": "https://maps.google.com/test",
    "img_url": "https://images.com/test.jpg",
    "seats": "10-20",
    "coffee_price": "15 PLN",
    "has_wifi": True,
    "has_sockets": True,
    "has_toilet": True,
    "can_take_calls": False
}, follow_redirects=True)
```

---

## ✏️ Edycja kawiarni w teście

```python
response = client.post(f'/update/cafe/{cafe_id}', data={
    "name": "Updated Name",
    "location": "New Location",
    "map_url": "https://maps.google.com/new",
    "img_url": "https://images.com/new.jpg",
    "seats": "20-30",
    "coffee_price": "20 PLN",
    "has_wifi": False,  # Zmienione
    "has_sockets": True,
    "has_toilet": True,
    "can_take_calls": True
}, follow_redirects=True)
```

---

## 🗑️ Usuwanie kawiarni w teście

```python
response = client.get(f'/delete/{cafe_id}', follow_redirects=True)
```

---

## 🚪 Wylogowanie w teście

```python
response = client.get('/logout', follow_redirects=True)
```

---

## 🌍 Zmiana języka w teście

```python
response = client.get('/set-language/en', follow_redirects=True)

# Sprawdź sesję
with client.session_transaction() as sess:
    assert sess['language'] == 'en'
```

---

## ✅ Asserty - Podstawowe

```python
# Status code
assert response.status_code == 200
assert response.status_code == 302  # Redirect

# Zawartość response
assert "Tekst" in response.data.decode('utf-8')
assert b"Tekst" in response.data  # Jako bytes

# Redirect
assert response.location == '/login'
assert '/login' in response.location
assert response.location.startswith('/login')

# Baza danych
cafe = db.session.get(Cafe, cafe_id)
assert cafe is not None  # Istnieje
assert cafe is None  # Nie istnieje
assert cafe.name == "Expected Name"

# User
user = db.session.query(User).filter_by(email="test@example.com").first()
assert user is not None
assert user.email == "test@example.com"
```

---

## 📖 Pobieranie z bazy

```python
# Po ID
cafe = db.session.get(Cafe, cafe_id)

# Query
user = db.session.query(User).filter_by(email="test@example.com").first()
cafes = db.session.query(Cafe).filter_by(location="Warsaw").all()

# Wszystkie
all_cafes = db.session.query(Cafe).all()
all_users = db.session.query(User).all()

# Count
count = db.session.query(Cafe).count()
```

---

## 🔍 Sprawdzanie response

```python
# Jako tekst
text = response.data.decode('utf-8')
assert "Kawiarnia dodana" in text

# Lub
text = response.get_data(as_text=True)
assert "Kawiarnia dodana" in text

# Jako bytes
assert b"Kawiarnia dodana" in response.data
```

---

## 🎭 Sprawdzanie flash messages

```python
response = client.post('/add', data={...}, follow_redirects=True)

assert "Kawiarnia dodana pomyślnie" in response.data.decode('utf-8')
assert "Błąd" in response.data.decode('utf-8')
```

---

## 🛡️ Testy security - XSS

```python
# Dodaj z <script>
response = client.post('/add', data={
    "name": "<script>alert('XSS')</script>",
    # ... inne pola
}, follow_redirects=True)

# Sprawdź że jest escaped
text = response.data.decode('utf-8')
assert "&lt;script&gt;" in text or "<script>" not in text
```

---

## 💉 Testy security - SQL Injection

```python
# Próba SQL injection
response = client.post('/login', data={
    'email': "admin'--",
    'password': 'anything'
})

# Assert że NIE zadziałało (ORM chroni)
assert response.status_code != 200 or "Nieprawidłowy" in response.data.decode()
```

---

## 🔐 Test hashowania hasła

```python
# Zarejestruj
client.post('/register', data={
    'name': 'User',
    'email': 'user@test.com',
    'password': 'plaintext123',
    'confirm_password': 'plaintext123'
})

# Pobierz z bazy
user = db.session.query(User).filter_by(email='user@test.com').first()

# Assert że jest zahashowane
assert user.password != 'plaintext123'
assert user.password.startswith('pbkdf2:sha256')
```

---

## 🔄 Test relacji User ↔ Cafe

```python
# Assert że user ma kawiarnie
assert len(auth_user.cafes) > 0
assert sample_cafe in auth_user.cafes

# Assert że cafe ma ownera
assert sample_cafe.owner == auth_user
assert sample_cafe.user_id == auth_user.id
```

---

## 🎪 Fixture usage (jeśli dodasz do conftest.py)

```python
def test_example(client, auth_user, sample_cafe):
    # auth_user - zalogowany user (ale trzeba zalogować w kliencie!)
    # sample_cafe - przykładowa kawiarnia należąca do auth_user
    
    # Zaloguj auth_user
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Teraz możesz używać sample_cafe
    response = client.get(f'/update/cafe/{sample_cafe.id}')
    assert response.status_code == 200
```

---

## 🧪 Pytest markers (opcjonalnie)

```python
@pytest.mark.skip("Pomiń ten test")
def test_something():
    pass

@pytest.mark.parametrize("input,expected", [
    ("test@example.com", True),
    ("not-email", False),
])
def test_email_validation(input, expected):
    # Test z różnymi parametrami
    pass
```

---

## 🏃 Uruchamianie testów

```bash
# Wszystkie testy
pytest

# Konkretny plik
pytest tests/test_cafe.py

# Konkretny test
pytest tests/test_cafe.py::test_user_cannot_delete_other_user_cafe

# Z verbose
pytest -v

# Z output
pytest -s

# Z coverage
pytest --cov=main tests/
```

---

## 🐛 Debugging testów

```python
# Print w teście (użyj pytest -s)
print(f"Response: {response.data.decode()}")
print(f"Status: {response.status_code}")
print(f"Cafe: {cafe.name}")

# Breakpoint
def test_something(client):
    response = client.get('/')
    import pdb; pdb.set_trace()  # Debugger zatrzyma się tutaj
    assert True
```

---

## ✨ PROTIP: Template funkcji testowej

```python
def test_description_of_what_youre_testing(client, auth_user):
    """Test: Clear description of test purpose."""
    
    # ARRANGE (Przygotowanie)
    # Setup: Zaloguj, utwórz dane, etc.
    client.post('/login', data={'email': '...', 'password': '...'})
    
    # ACT (Akcja)
    # Execute: Wykonaj akcję którą testujesz
    response = client.post('/add', data={...})
    
    # ASSERT (Sprawdzenie)
    # Verify: Sprawdź wynik
    assert response.status_code == 200
    assert "Expected text" in response.data.decode()
```

---

## 🎯 NAJCZĘSTSZE BŁĘDY I ROZWIĄZANIA

### ❌ `db.session.get(Cafe, None)` - error
✅ **Rozwiązanie:** `cafe_id` jest None. Sprawdź czy cafe została stworzona: `db.session.refresh(cafe)`

### ❌ Test przechodzi ale kawiarnia nie została dodana
✅ **Rozwiązanie:** Zapomniałeś zalogować użytkownika przed POST /add

### ❌ `AttributeError: 'NoneType' object has no attribute 'id'`
✅ **Rozwiązanie:** Obiekt nie istnieje w bazie. Sprawdź czy `db.session.commit()` został wywołany

### ❌ Test działa lokalnie, nie działa w pytest
✅ **Rozwiązanie:** Sprawdź czy używasz `app.app_context()` i fixtures

### ❌ Flash message nie pojawia się w response
✅ **Rozwiązanie:** Użyj `follow_redirects=True` w request

---

**GOTOWE DO UŻYCIA!** 🚀

Skopiuj te snippety do testów i modyfikuj według potrzeb!
