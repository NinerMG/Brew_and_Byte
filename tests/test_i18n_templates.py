# ========================================
# SZKIELETY TESTÓW DLA test_i18n.py
# ========================================
# Nowy plik testowy dla wielojęzyczności (Flask-Babel)

# ==========================================
# ZMIANA JĘZYKA
# ==========================================

def test_set_language_to_english(client):
    """Test: Zmiana języka na angielski."""
    # TODO: GET /set-language/en
    # TODO: Assert status 302 (redirect)
    # TODO: Sprawdź sesję: with client.session_transaction() as sess:
    # TODO:     assert sess['language'] == 'en'
    pass


def test_set_language_to_polish(client):
    """Test: Zmiana języka na polski."""
    # TODO: GET /set-language/pl
    # TODO: Assert sess['language'] == 'pl'
    pass


def test_set_language_invalid_code(client):
    """Test: Próba ustawienia nieobsługiwanego języka."""
    # TODO: GET /set-language/de (nieobsługiwany)
    # TODO: Assert że język NIE zmienił się (lub error)
    pass


def test_language_stored_in_session(client):
    """Test: Język jest przechowywany w sesji."""
    # TODO: GET /set-language/en
    # TODO: GET / (strona główna)
    # TODO: Assert że język nadal 'en' w sesji
    pass


def test_language_persists_across_requests(client):
    """Test: Język utrzymuje się między żądaniami."""
    # TODO: Set language to 'en'
    # TODO: GET / (home)
    # TODO: GET /login
    # TODO: Assert że wszystkie strony są po angielsku
    pass


def test_default_language_is_polish(client):
    """Test: Domyślny język to polski (bez ustawienia)."""
    # TODO: GET / (bez ustawienia języka)
    # TODO: Assert że treść jest po polsku
    pass


# ==========================================
# TŁUMACZENIA UI - STRONA GŁÓWNA
# ==========================================

def test_homepage_in_polish(client):
    """Test: Strona główna wyświetla polskie teksty."""
    # TODO: GET /set-language/pl
    # TODO: GET /
    # TODO: Assert 'Brew & Byte' in response (tytuł)
    # TODO: Assert jakiś polski tekst (np. 'Kawiarnie')
    pass


def test_homepage_in_english(client):
    """Test: Strona główna wyświetla angielskie teksty."""
    # TODO: GET /set-language/en
    # TODO: GET /
    # TODO: Assert angielski tekst (np. 'Cafes')
    pass


# ==========================================
# TŁUMACZENIA FORMULARZY
# ==========================================

def test_login_form_in_polish(client):
    """Test: Formularz logowania po polsku."""
    # TODO: GET /set-language/pl
    # TODO: GET /login
    # TODO: Assert 'Email' in response
    # TODO: Assert 'Hasło' in response
    # TODO: Assert 'Zaloguj' in response (button)
    pass


def test_login_form_in_english(client):
    """Test: Formularz logowania po angielsku."""
    # TODO: GET /set-language/en
    # TODO: GET /login
    # TODO: Assert 'Email' in response
    # TODO: Assert 'Password' in response
    # TODO: Assert 'Login' in response (button)
    pass


def test_register_form_in_polish(client):
    """Test: Formularz rejestracji po polsku."""
    # TODO: GET /register po ustawieniu PL
    # TODO: Assert 'Imię' lub 'Name'
    # TODO: Assert 'Hasło'
    # TODO: Assert 'Potwierdź hasło'
    pass


def test_register_form_in_english(client):
    """Test: Formularz rejestracji po angielsku."""
    # TODO: GET /register po ustawieniu EN
    # TODO: Assert 'Name'
    # TODO: Assert 'Password'
    # TODO: Assert 'Confirm Password'
    pass


def test_add_cafe_form_in_polish(client, auth_user):
    """Test: Formularz dodawania kawiarni po polsku."""
    # TODO: Zaloguj, ustaw język PL
    # TODO: GET /add
    # TODO: Assert polskie labele (np. 'Nazwa kawiarni', 'Lokalizacja')
    pass


def test_add_cafe_form_in_english(client, auth_user):
    """Test: Formularz dodawania kawiarni po angielsku."""
    # TODO: Zaloguj, ustaw język EN
    # TODO: GET /add
    # TODO: Assert angielskie labele ('Cafe Name', 'Location')
    pass


# ==========================================
# TŁUMACZENIA FLASH MESSAGES
# ==========================================

def test_flash_messages_translated_polish(client):
    """Test: Flash messages są po polsku."""
    # TODO: Ustaw język PL
    # TODO: Spróbuj zalogować z błędnym hasłem
    # TODO: Assert 'Nieprawidłowy email, lub hasło' in response
    pass


def test_flash_messages_translated_english(client):
    """Test: Flash messages są po angielsku."""
    # TODO: Ustaw język EN
    # TODO: Spróbuj zalogować z błędnym hasłem
    # TODO: Assert angielski komunikat błędu
    pass


def test_success_messages_translated(client):
    """Test: Komunikaty sukcesu są tłumaczone."""
    # TODO: Ustaw język EN
    # TODO: Zarejestruj użytkownika
    # TODO: Assert angielski komunikat sukcesu
    pass


# ==========================================
# TŁUMACZENIA BŁĘDÓW WALIDACJI
# ==========================================

def test_form_errors_translated_polish(client):
    """Test: Błędy formularzy po polsku."""
    # TODO: Ustaw język PL
    # TODO: POST /register z za krótkim hasłem
    # TODO: Assert 'Hasło musi mieć minimum 8 znaków'
    pass


def test_form_errors_translated_english(client):
    """Test: Błędy formularzy po angielsku."""
    # TODO: Ustaw język EN
    # TODO: POST /register z za krótkim hasłem
    # TODO: Assert 'Password must be at least 8 characters'
    pass


def test_required_field_error_translated(client):
    """Test: 'To pole jest wymagane' tłumaczone."""
    # TODO: Ustaw język EN
    # TODO: POST /register bez email
    # TODO: Assert 'This field is required' (lub podobny)
    pass


# ==========================================
# TŁUMACZENIA NAVIGATION/MENU
# ==========================================

def test_navigation_translated_polish(client):
    """Test: Menu nawigacji po polsku."""
    # TODO: Ustaw PL
    # TODO: GET /
    # TODO: Assert linki: 'Strona główna', 'Zaloguj', 'Rejestracja'
    pass


def test_navigation_translated_english(client):
    """Test: Menu nawigacji po angielsku."""
    # TODO: Ustaw EN
    # TODO: GET /
    # TODO: Assert linki: 'Home', 'Login', 'Register'
    pass


# ==========================================
# TŁUMACZENIA PÓL BOOLEAN (Cafe details)
# ==========================================

def test_cafe_boolean_fields_translated_polish(client, sample_cafe):
    """Test: 'Ma WiFi', 'Ma gniazdka' po polsku."""
    # TODO: Ustaw PL
    # TODO: GET / (lista kawiarni)
    # TODO: Assert 'WiFi', 'Gniazdka', 'Toaleta'
    pass


def test_cafe_boolean_fields_translated_english(client, sample_cafe):
    """Test: 'Has WiFi', 'Has Sockets' po angielsku."""
    # TODO: Ustaw EN
    # TODO: GET /
    # TODO: Assert 'WiFi', 'Sockets', 'Toilet'
    pass


# ==========================================
# EDGE CASES I18N
# ==========================================

def test_language_switch_with_user_logged_in(client, auth_user):
    """Test: Zmiana języka gdy użytkownik jest zalogowany."""
    # TODO: Zaloguj
    # TODO: Zmień język na EN
    # TODO: Assert że przywitanie jest po angielsku
    pass


def test_language_remains_after_logout(client, auth_user):
    """Test: Język pozostaje po wylogowaniu."""
    # TODO: Zaloguj, ustaw EN, wyloguj
    # TODO: GET /login
    # TODO: Assert że nadal EN
    pass


def test_accept_language_header_fallback(client):
    """Test: Fallback do Accept-Language header przeglądarki."""
    # TODO: GET / z headerem Accept-Language: en
    # TODO: Assert że treść jest po angielsku
    # (Sprawdź implementację get_locale() w main.py)
    pass
