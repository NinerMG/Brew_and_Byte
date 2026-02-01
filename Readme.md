# ☕ Brew & Byte

**Brew & Byte** to aplikacja webowa pomagająca znaleźć idealne kawiarnie do pracy zdalnej w Twoim mieście. Platforma prezentuje kawiarnie z WiFi, gniazdkami i dobrą kawą.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Funkcjonalności

### Podstawowe
- 📋 **Przeglądanie kawiarni** - lista wszystkich dostępnych miejsc
- ➕ **Dodawanie kawiarni** - użytkownicy mogą dodawać nowe lokalizacje
- ✏️ **Edycja kawiarni** - aktualizacja informacji o miejscach
- 🗑️ **Usuwanie kawiarni** - usuwanie nieaktualnych miejsc
- 🔍 **Szczegółowe informacje** - WiFi, gniazdka, toalety, ceny kawy

### Zarządzanie użytkownikami
- 👤 **Rejestracja** - tworzenie nowych kont użytkowników
- 🔐 **Logowanie** - bezpieczne uwierzytelnianie
- 🔒 **Autoryzacja** - kontrola dostępu do funkcji (tylko właściciel może edytować/usuwać swoje kawiarnie)
- 🛡️ **Hashowanie haseł** - bezpieczne przechowywanie danych (pbkdf2:sha256)

### Dodatkowe
- 🌍 **Wielojęzyczność** - interfejs w języku polskim i angielskim
- 📱 **Responsywny design** - Bootstrap 5
- ✅ **Walidacja formularzy** - zabezpieczenie przed błędnymi danymi
- 🧪 **Testy** - pełny zestaw testów jednostkowych i integracyjnych

## 🛠 Technologie

### Backend
- **Flask 3.0.3** - framework webowy
- **SQLAlchemy 2.0.35** - ORM do obsługi bazy danych
- **Flask-Login 0.6.3** - zarządzanie sesjami użytkowników
- **Flask-WTF 1.2.1** - formularze z walidacją
- **Flask-Babel 4.0.0** - wsparcie wielojęzyczne (i18n)
- **Werkzeug 3.0.3** - narzędzia WSGI, hashowanie haseł

### Frontend
- **Bootstrap 5** - responsywny interfejs użytkownika
- **Jinja2** - silnik szablonów

### Baza danych
- **SQLite** - lekka baza danych (cafes.db)

### Testowanie
- **pytest** - framework do testów
- **pytest-flask** - integracja testów z Flask

## 📦 Instalacja

### Wymagania
- Python 3.8 lub nowszy
- pip (menedżer pakietów Python)

## 🚀 Uruchomienie

### Tryb deweloperski
```bash
python run.py
```

Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:5000`



## 📁 Struktura projektu

```
Brew_and_Byte/
├── run.py                  # Entry point aplikacji
├── config.py               # Konfiguracja (Development/Testing/Production)
├── requirements.txt        # Zależności projektu
├── babel.cfg              # Konfiguracja Babel (tłumaczenia)
├── messages.pot           # Szablon tłumaczeń
├── app/                   # Pakiet główny aplikacji
│   ├── __init__.py        # Application Factory
│   ├── models.py          # Modele SQLAlchemy (User, Cafe)
│   ├── forms.py           # Formularze WTForms
│   ├── extensions.py      # Inicjalizacja rozszerzeń Flask
│   └── routes/            # Blueprinty z endpointami
│       ├── __init__.py
│       ├── main.py        # Strona główna, zmiana języka
│       ├── auth.py        # Rejestracja, logowanie, wylogowanie
│       └── cafe.py        # CRUD dla kawiarni
├── instance/              # Baza danych SQLite
│   └── cafes.db
├── static/                # Pliki statyczne
│   └── style.css
├── templates/             # Szablony HTML
│   ├── base.html
│   ├── index.html
│   ├── add_cafe.html
│   ├── update_cafe.html
│   ├── login.html
│   └── register.html
├── translations/          # Tłumaczenia (PL/EN)
│   ├── en/
│   │   └── LC_MESSAGES/
│   └── pl/
│       └── LC_MESSAGES/
└── tests/                 # Testy jednostkowe i integracyjne
    ├── conftest.py
    ├── test_cafe.py
    ├── test_user.py
    ├── test_security.py
    ├── test_i18n.py
    └── integration_tests.py
```


## 🌍 Wielojęzyczność

Aplikacja obsługuje dwa języki:
- 🇵🇱 **Polski** (domyślny)
- 🇬🇧 **Angielski**

### Zmiana języka
Użytkownicy mogą zmieniać język za pomocą przełącznika w interfejsie lub przez URL:
```
/set-language/pl  # Polski
/set-language/en  # Angielski
```



## 🔒 Bezpieczeństwo

### Zaimplementowane zabezpieczenia
- **Hashowanie haseł** - pbkdf2:sha256 z salt
- **CSRF Protection** - Flask-WTF
- **Walidacja danych** - WTForms validators
- **Ochrona przed XSS** - automatyczne escape'owanie Jinja2
- **Walidacja HTML** - custom validator blokujący znaczniki HTML
- **Zabezpieczenie email** - email-validator
- **Kontrola dostępu** - Flask-Login + dekoratory @login_required
- **Minimalny długość hasła** - 8 znaków


## 📝 Modele danych

### User (Użytkownik)
```python
- id: int (PK)
- email: str (unique)
- password: str (hashed)
- name: str
- cafes: relationship
```

### Cafe (Kawiarnia)
```python
- id: int (PK)
- name: str (unique)
- map_url: str
- img_url: str
- location: str
- seats: str (zakres)
- has_toilet: bool
- has_wifi: bool
- has_sockets: bool
- can_take_calls: bool
- coffee_price: str
- user_id: int (FK)
```


## 👨‍💻 Autor

**NinerMG**
- GitHub: [@NinerMG](https://github.com/NinerMG)


