import pytest
from main import User,Cafe, db

def test_login_add_cafe(client, auth_user):
    client.post('/login',data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.post('/add', data={
        "name": "Testowa Kawiarnia",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN",
        "has_wifi": True,
        "has_sockets": True,
        "has_toilet": True,
        "can_take_calls": False
    }, follow_redirects=True)

    assert "Kawiarnia dodana pomyślnie" in response.data.decode('utf-8')
    assert b"Testowa Kawiarnia" in response.data

def test_delete_cafe_requires_login(client):
    response = client.get('/delete/1')
    assert response.status_code == 302
    assert '/login' in response.location

def test_delete_cafe(client, auth_user, sample_cafe):
    client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)

    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)

    assert response.status_code == 200
    assert "Kawiarnia usunięta!" in response.get_data(as_text=True)

def test_user_cannot_delete_other_user_cafe(client, auth_user, sample_cafe):
    client.post(
        '/register', data={
            "name": "NowyUser",
            "email": "nowy@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True
    )
    client.post('/login', data={'email': 'nowy@example.com', 'password': 'password123'})

    response = client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)

    cafe_still_exists = db.session.get(Cafe, sample_cafe.id)
    assert cafe_still_exists is not None

    assert 'Nie masz uprawnień!' in response.data.decode('utf-8')


def test_user_cannot_update_other_user_cafe(client, auth_user, sample_cafe):
    client.post(
        '/register', data={
            "name": "NowyUser",
            "email": "nowy@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True
    )
    client.post('/login', data={'email': 'nowy@example.com', 'password': 'password123'})

    response = client.get(f'/update/cafe/{sample_cafe.id}', follow_redirects=True)

    cafe_still_exists = db.session.get(Cafe, sample_cafe.id)
    assert cafe_still_exists is not None

    assert 'Nie masz uprawnień!' in response.data.decode('utf-8')


def test_user_can_only_update_own_cafe(client, auth_user, sample_cafe, app):
    client.get(f'/update/cafe/{sample_cafe.id}', follow_redirects=True)

    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.post(f'/update/cafe/{sample_cafe.id}', data={
        "name": "Zaktualizowana Kawiarnia",
        "location": "Gdańsk",
        "map_url": "https://maps.google.com/updated",
        "img_url": "https://images.com/updated.jpg",
        "seats": "30-40",
        "coffee_price": "15 PLN",
        "has_wifi": True,
        "has_sockets": True,
        "has_toilet": True,
        "can_take_calls": True
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "zaktualizowana" in response.data.decode(
        'utf-8').lower() or "Kawiarnia została edytowana" in response.data.decode('utf-8')

    with app.app_context():
        updated_cafe = db.session.get(Cafe, sample_cafe.id)
        assert updated_cafe.name == "Zaktualizowana Kawiarnia"
        assert updated_cafe.location == "Gdańsk"
        assert updated_cafe.seats == "30-40"
        assert updated_cafe.coffee_price == "15 PLN"


def test_update_cafe_page_loads(client, auth_user, sample_cafe):
    """Test: Strona edycji kawiarni ładuje się poprawnie."""
    # TODO: Zaloguj użytkownika
    # TODO: GET /update/cafe/{sample_cafe.id}
    # TODO: Assert status 200
    # TODO: Assert że formularz jest na stronie
    pass


def test_update_cafe_form_prepopulated(client, auth_user, sample_cafe):
    """Test: Formularz edycji ma obecne dane kawiarni."""
    # TODO: Zaloguj użytkownika
    # TODO: GET /update/cafe/{sample_cafe.id}
    # TODO: Assert że response zawiera sample_cafe.name
    # TODO: Assert że response zawiera sample_cafe.location
    pass


def test_update_cafe_changes_name(client, auth_user, sample_cafe):
    """Test: Zmiana nazwy kawiarni działa."""
    # TODO: Zaloguj użytkownika
    # TODO: POST /update/cafe/{id} z nową nazwą
    # TODO: Pobierz kawiarnię z bazy: cafe = db.session.get(Cafe, sample_cafe.id)
    # TODO: Assert że cafe.name == nowa nazwa
    pass


def test_update_cafe_changes_location(client, auth_user, sample_cafe):
    """Test: Zmiana lokalizacji działa."""
    # TODO: Similar to above, ale zmień location
    pass


def test_update_cafe_changes_all_fields(client, auth_user, sample_cafe):
    """Test: Zmiana wszystkich pól naraz działa."""
    # TODO: POST z nowymi wartościami dla WSZYSTKICH pól
    # TODO: Assert że wszystkie pola się zmieniły
    pass


def test_update_cafe_toggles_boolean_fields(client, auth_user, sample_cafe):
    """Test: Zmiana checkboxów (WiFi, gniazdka, etc.) działa."""
    # TODO: Odwróć wartości has_wifi, has_sockets, etc.
    # TODO: Assert że wartości się zmieniły
    pass


def test_update_cafe_without_name(client, auth_user, sample_cafe):
    """Test: Walidacja - brak nazwy."""
    # TODO: POST bez pola 'name'
    # TODO: Assert status 200 (pozostaje na formularzu)
    # TODO: Assert komunikat błędu walidacji
    pass


def test_update_cafe_with_invalid_url(client, auth_user, sample_cafe):
    """Test: Walidacja URL przy edycji."""
    # TODO: POST z map_url="invalid-url" (bez http)
    # TODO: Assert błąd walidacji
    pass


def test_update_cafe_redirects_to_home(client, auth_user, sample_cafe):
    """Test: Po udanej edycji przekierowanie do home."""
    # TODO: POST z poprawnymi danymi
    # TODO: Assert status 302 lub follow_redirects i sprawdź że jesteś na home
    pass


def test_update_nonexistent_cafe_returns_404(client, auth_user):
    """Test: Edycja nieistniejącej kawiarni zwraca 404."""
    # TODO: Zaloguj użytkownika
    # TODO: GET /update/cafe/99999
    # TODO: Assert status 404
    pass


# ==========================================
# CRUD - DELETE (Usuwanie)
# ==========================================

def test_delete_cafe_removes_from_database(client, auth_user, sample_cafe):
    """Test: Usunięcie kawiarni faktycznie usuwa z bazy."""
    # TODO: Zaloguj użytkownika
    # TODO: DELETE cafe
    # TODO: Spróbuj pobrać z bazy: cafe = db.session.get(Cafe, sample_cafe.id)
    # TODO: Assert że cafe is None
    pass


def test_delete_cafe_redirects_to_home(client, auth_user, sample_cafe):
    """Test: Po usunięciu przekierowanie do home."""
    # TODO: DELETE cafe
    # TODO: Assert redirect do home
    pass


def test_delete_nonexistent_cafe(client, auth_user):
    """Test: Usunięcie nieistniejącej kawiarni."""
    # TODO: Spróbuj DELETE /delete/99999
    # TODO: Assert 404 lub odpowiedni flash message
    pass


def test_delete_cafe_shows_flash_message(client, auth_user, sample_cafe):
    """Test: Flash message po usunięciu."""
    # TODO: DELETE cafe
    # TODO: Assert 'Kawiarnia usunięta!' in response
    pass


# ==========================================
# CRUD - ADD (Dodawanie) - Walidacja
# ==========================================

def test_add_cafe_without_login(client):
    """Test: Próba dodania bez logowania przekierowuje."""
    # TODO: POST /add bez logowania
    # TODO: Assert redirect do /login
    pass


def test_add_cafe_without_name(client, auth_user):
    """Test: Walidacja - brak nazwy."""
    # TODO: Zaloguj użytkownika
    # TODO: POST /add bez pola 'name'
    # TODO: Assert błąd walidacji
    pass


def test_add_cafe_without_location(client, auth_user):
    """Test: Walidacja - brak lokalizacji."""
    # TODO: POST bez 'location'
    pass


def test_add_cafe_without_map_url(client, auth_user):
    """Test: Walidacja - brak map_url."""
    # TODO: POST bez 'map_url'
    pass


def test_add_cafe_without_img_url(client, auth_user):
    """Test: Walidacja - brak img_url."""
    pass


def test_add_cafe_without_seats(client, auth_user):
    """Test: Walidacja - brak seats."""
    pass


def test_add_cafe_without_coffee_price(client, auth_user):
    """Test: Walidacja - brak ceny kawy."""
    pass


def test_add_cafe_with_invalid_map_url(client, auth_user):
    """Test: Nieprawidłowy format URL dla mapy."""
    # TODO: POST z map_url='not-a-url'
    # TODO: Assert 'Invalid URL' lub podobny komunikat
    pass


def test_add_cafe_with_invalid_img_url(client, auth_user):
    """Test: Nieprawidłowy format URL dla obrazka."""
    pass


def test_add_cafe_with_duplicate_name(client, auth_user, sample_cafe):
    """Test: Dodanie kawiarni z już istniejącą nazwą (unique constraint)."""
    # TODO: Spróbuj dodać kawiarnię z name=sample_cafe.name
    # TODO: Assert błąd (IntegrityError albo flash message)
    pass


def test_add_cafe_displays_in_list(client, auth_user):
    """Test: Nowa kawiarnia pojawia się na liście."""
    # TODO: Dodaj nową kawiarnię
    # TODO: GET /
    # TODO: Assert że nazwa nowej kawiarni jest w response
    pass


def test_cafe_belongs_to_user(client, auth_user):
    """Test: Nowa kawiarnia ma przypisany user_id."""
    # TODO: Dodaj kawiarnię
    # TODO: Pobierz z bazy i sprawdź cafe.user_id == auth_user.id
    pass


# ==========================================
# WYŚWIETLANIE (Home page)
# ==========================================

def test_home_displays_all_cafes(client, auth_user):
    """Test: Strona główna wyświetla wszystkie kawiarnie."""
    # TODO: Dodaj 3 kawiarnie
    # TODO: GET /
    # TODO: Assert że wszystkie 3 nazwy są w response
    pass


def test_home_displays_cafe_details(client, sample_cafe):
    """Test: Szczegóły kawiarni widoczne na stronie."""
    # TODO: GET /
    # TODO: Assert że location, coffee_price są w response
    pass


def test_home_with_no_cafes(client):
    """Test: Pusta lista kawiarni."""
    # TODO: GET / (bez żadnych kawiarni w bazie)
    # TODO: Assert komunikat 'Brak kawiarni' lub pusta lista
    pass


def test_home_displays_multiple_cafes(client, auth_user):
    """Test: Wiele kawiarni wyświetla się poprawnie."""
    # TODO: Dodaj 5 kawiarni
    # TODO: Assert wszystkie widoczne
    pass


def test_cafe_boolean_fields_display_correctly(client, sample_cafe):
    """Test: Ikony/checkmarki WiFi, gniazdek wyświetlają się."""
    # TODO: GET /
    # TODO: Assert że są ikony/tekst dla has_wifi, has_sockets
    pass


# ==========================================
# CAFE MODEL
# ==========================================

def test_cafe_model_string_representation(sample_cafe):
    """Test: __repr__ lub __str__ modelu Cafe."""
    # TODO: cafe_str = str(sample_cafe) lub repr(sample_cafe)
    # TODO: Assert że zawiera nazwę kawiarni
    pass


def test_cafe_unique_name_constraint():
    """Test: Constraint unique na nazwie działa na poziomie bazy."""
    # TODO: Dodaj 2 kawiarnie z tą samą nazwą bezpośrednio do bazy
    # TODO: Assert że pojawi się IntegrityError
    pass


def test_cafe_foreign_key_relationship(auth_user, sample_cafe):
    """Test: Foreign key do User działa."""
    # TODO: Assert sample_cafe.user_id == auth_user.id
    # TODO: Assert sample_cafe.owner == auth_user (przez relationship)
    pass


# ==========================================
# EDGE CASES
# ==========================================

def test_add_cafe_with_empty_strings(client, auth_user):
    """Test: Puste stringi (nie None) w polach."""
    # TODO: POST z name='', location=''
    # TODO: Assert błąd walidacji
    pass


def test_add_cafe_with_whitespace_only(client, auth_user):
    """Test: Same spacje w polach."""
    # TODO: POST z name='   ', location='   '
    # TODO: Assert błąd walidacji
    pass


def test_very_long_cafe_name(client, auth_user):
    """Test: Nazwa dłuższa niż 250 znaków."""
    # TODO: POST z name='a'*300
    # TODO: Assert błąd (przekroczenie max length)
    pass


def test_unicode_characters_in_cafe_name(client, auth_user):
    """Test: Emoji i znaki specjalne w nazwie."""
    # TODO: POST z name='Kawiarnia ☕🎉'
    # TODO: Assert że działa poprawnie
    pass


# ==========================================
# DATABASE ERRORS
# ==========================================

def test_database_rollback_on_error(client, auth_user, monkeypatch):
    """Test: Rollback przy błędzie bazy danych."""
    # TODO: Użyj monkeypatch żeby zasymulować db.session.commit() error
    # TODO: Spróbuj dodać kawiarnię
    # TODO: Assert że kawiarnia NIE została zapisana
    pass
