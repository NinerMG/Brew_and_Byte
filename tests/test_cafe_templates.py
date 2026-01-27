# ========================================
# SZKIELETY TESTÓW DLA test_cafe.py
# ========================================
# Skopiuj te testy do test_cafe.py i wypełnij TODO

# ==========================================
# 🔥 KRYTYCZNE - SECURITY (NAPISZ NAJPIERW!)
# ==========================================

def test_user_cannot_delete_other_user_cafe(client, auth_user, sample_cafe):
    """Test: Użytkownik NIE może usunąć kawiarni innego użytkownika."""
    # TODO: Utwórz drugiego użytkownika w bazie
    # second_user = User(email="user2@example.com", password=hashed_pw, name="User2")
    # db.session.add(second_user)
    # db.session.commit()
    
    # TODO: Wyloguj pierwszego użytkownika (jeśli zalogowany)
    # client.get('/logout')
    
    # TODO: Zaloguj się jako drugi użytkownik
    # client.post('/login', data={'email': 'user2@example.com', 'password': '...'})
    
    # TODO: Spróbuj usunąć sample_cafe (która należy do auth_user, nie user2!)
    # response = client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)
    
    # TODO: Assert że kawiarnia NADAL istnieje w bazie
    # cafe_still_exists = db.session.get(Cafe, sample_cafe.id)
    # assert cafe_still_exists is not None
    
    # TODO: Assert flash message o braku uprawnień
    # assert 'Nie masz uprawnień' in response.data.decode('utf-8')
    pass


def test_user_cannot_update_other_user_cafe(client, auth_user, sample_cafe):
    """Test: Użytkownik NIE może edytować kawiarni innego użytkownika."""
    # TODO: Utwórz drugiego użytkownika
    # TODO: Zaloguj jako drugi użytkownik
    # TODO: Spróbuj POST do /update/cafe/{sample_cafe.id} z nowymi danymi
    # TODO: Assert że dane kawiarni NIE zostały zmienione
    # TODO: Assert flash message o braku uprawnień
    pass


def test_user_can_only_delete_own_cafe(client, auth_user, sample_cafe):
    """Test: Użytkownik MOŻE usunąć SWOJĄ kawiarnię."""
    # TODO: Zaloguj jako auth_user (właściciel sample_cafe)
    # TODO: DELETE sample_cafe
    # TODO: Assert że kawiarnia ZOSTAŁA usunięta
    # TODO: Assert flash message sukcesu
    pass


def test_user_can_only_update_own_cafe(client, auth_user, sample_cafe):
    """Test: Użytkownik MOŻE edytować SWOJĄ kawiarnię."""
    # TODO: Zaloguj jako auth_user
    # TODO: POST do /update/cafe/{id} z nowymi danymi
    # TODO: Assert że dane zostały zmienione w bazie
    pass


# ==========================================
# CRUD - UPDATE (Edycja)
# ==========================================

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
