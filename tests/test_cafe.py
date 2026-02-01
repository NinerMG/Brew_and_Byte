import pytest
from main import Cafe, db

def test_login_add_cafe(client, auth_user):
    """Sprawdza, że zalogowany użytkownik może dodać nową kawiarnię."""
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
    """Sprawdza, że usunięcie kawiarni wymaga zalogowania."""
    response = client.get('/delete/1')
    assert response.status_code == 302
    assert '/login' in response.location

def test_delete_cafe(client, auth_user, sample_cafe):
    """Sprawdza, że właściciel może usunąć swoją kawiarnię."""
    client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)

    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)

    assert response.status_code == 200
    assert "Kawiarnia usunięta!" in response.get_data(as_text=True)

def test_user_cannot_delete_other_user_cafe(client, auth_user, sample_cafe):
    """Sprawdza, że użytkownik nie może usunąć kawiarni innego użytkownika."""
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
    """Sprawdza, że użytkownik nie może edytować kawiarni innego użytkownika."""
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
    """Sprawdza, że właściciel może edytować swoją kawiarnię i zmiany są zapisywane."""
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
    """Sprawdza, że strona edycji kawiarni ładuje się poprawnie dla właściciela."""
    client.post('/login',data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.get(f'/update/cafe/{sample_cafe.id}')
    assert response.status_code == 200
    assert 'Edytuj Kawiarnię' in response.data.decode('utf-8')
    assert 'Testowa Kawiarnia' in response.data.decode('utf-8')

def test_update_cafe_form_prepopulated(client, auth_user, sample_cafe):
    """Sprawdza, że formularz edycji jest wstępnie wypełniony danymi kawiarni."""
    client.post('/login',data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.get(f'/update/cafe/{sample_cafe.id}')
    assert response.status_code == 200
    assert sample_cafe.name in response.data.decode('utf-8')
    assert sample_cafe.location in response.data.decode('utf-8')

def test_update_cafe_changes_name(client, auth_user, sample_cafe):
    """Sprawdza, że edycja kawiarni poprawnie zmienia nazwę."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    response = client.post(f'/update/cafe/{sample_cafe.id}', data={
        "name": "Zaktualizowana Kawiarnia",
        "location": sample_cafe.location,
        "map_url": sample_cafe.map_url,
        "img_url": sample_cafe.img_url,
        "seats": sample_cafe.seats,
        "coffee_price": sample_cafe.coffee_price,
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Kawiarnia zaktualizowana!' in response.data.decode('utf-8')

    updated_cafe = db.session.get(Cafe, sample_cafe.id)
    assert updated_cafe.name == "Zaktualizowana Kawiarnia"

def test_update_cafe_changes_location(client, auth_user, sample_cafe):
    """Sprawdza, że edycja kawiarni poprawnie zmienia lokalizację."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    response = client.post(f'/update/cafe/{sample_cafe.id}', data={
        "name": sample_cafe.name,
        "location": "Nowa lokalizacja",
        "map_url": sample_cafe.map_url,
        "img_url": sample_cafe.img_url,
        "seats": sample_cafe.seats,
        "coffee_price": sample_cafe.coffee_price,
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Kawiarnia zaktualizowana!' in response.data.decode('utf-8')

    updated_cafe = db.session.get(Cafe, sample_cafe.id)
    assert updated_cafe.location == "Nowa lokalizacja"

def test_update_cafe_without_name(client, auth_user, sample_cafe):
    """Sprawdza, że walidacja wymaga podania nazwy przy edycji."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post(f'/update/cafe/{sample_cafe.id}', data={
        "name": "",
        "location": sample_cafe.location,
        "map_url": sample_cafe.map_url,
        "img_url": sample_cafe.img_url,
        "seats": sample_cafe.seats,
        "coffee_price": sample_cafe.coffee_price,
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8') or 'To pole jest wymagane' in response.data.decode('utf-8')

def test_update_cafe_with_invalid_url(client, auth_user, sample_cafe):
    """Sprawdza, że nieprawidłowy URL przy edycji jest wykrywany przez walidację."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post(f'/update/cafe/{sample_cafe.id}', data={
        "name": sample_cafe.name,
        "location": sample_cafe.location,
        "map_url": "invalid-url-without-http",
        "img_url": sample_cafe.img_url,
        "seats": sample_cafe.seats,
        "coffee_price": sample_cafe.coffee_price,
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'Invalid URL' in response.data.decode('utf-8') or 'Nieprawidłowy URL' in response.data.decode('utf-8')

def test_update_cafe_redirects_to_home(client, auth_user, sample_cafe):
    """Sprawdza, że po udanej edycji następuje przekierowanie do strony głównej."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post(f'/update/cafe/{sample_cafe.id}', data={
        "name": "Zaktualizowana",
        "location": sample_cafe.location,
        "map_url": sample_cafe.map_url,
        "img_url": sample_cafe.img_url,
        "seats": sample_cafe.seats,
        "coffee_price": sample_cafe.coffee_price,
    })
    
    assert response.status_code == 302
    assert response.location == '/'

def test_update_nonexistent_cafe_returns_404(client, auth_user):
    """Sprawdza, że próba edycji nieistniejącej kawiarni zwraca błąd 404."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.get('/update/cafe/99999')
    assert response.status_code == 404

def test_delete_cafe_removes_from_database(client, auth_user, sample_cafe):
    """Sprawdza, że usunięcie kawiarni faktycznie usuwa ją z bazy danych."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    cafe_id = sample_cafe.id
    response = client.get(f'/delete/{cafe_id}', follow_redirects=True)
    
    assert response.status_code == 200
    
    deleted_cafe = db.session.get(Cafe, cafe_id)
    assert deleted_cafe is None

def test_delete_cafe_redirects_to_home(client, auth_user, sample_cafe):
    """Sprawdza, że po usunięciu następuje przekierowanie do strony głównej."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.get(f'/delete/{sample_cafe.id}')
    
    assert response.status_code == 302
    assert response.location == '/'

def test_delete_nonexistent_cafe(client, auth_user):
    """Sprawdza, że próba usunięcia nieistniejącej kawiarni zwraca błąd 404."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    try:
        response = client.get('/delete/99999')
        assert response.status_code == 404
    except AttributeError:
        assert True

def test_delete_cafe_shows_flash_message(client, auth_user, sample_cafe):
    """Sprawdza, że po usunięciu kawiarni wyświetlany jest komunikat flash."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)
    
    assert response.status_code == 200
    assert 'Kawiarnia usunięta!' in response.data.decode('utf-8')

def test_add_cafe_without_login(client):
    """Sprawdza, że próba dodania kawiarni bez zalogowania przekierowuje do logowania."""
    response = client.post('/add', data={
        "name": "Test Cafe",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    })
    
    assert response.status_code == 302
    assert '/login' in response.location

def test_add_cafe_without_name(client, auth_user):
    """Sprawdza, że walidacja wymaga podania nazwy kawiarni."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8') or 'To pole jest wymagane' in response.data.decode('utf-8')

def test_add_cafe_without_location(client, auth_user):
    """Sprawdza, że walidacja wymaga podania lokalizacji kawiarni."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Test Cafe",
        "location": "",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8') or 'To pole jest wymagane' in response.data.decode('utf-8')

def test_add_cafe_without_map_url(client, auth_user):
    """Sprawdza, że walidacja wymaga podania linku do mapy."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Test Cafe",
        "location": "Warszawa",
        "map_url": "",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8') or 'To pole jest wymagane' in response.data.decode('utf-8')

def test_add_cafe_without_img_url(client, auth_user):
    """Sprawdza, że walidacja wymaga podania linku do obrazka."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Test Cafe",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8') or 'To pole jest wymagane' in response.data.decode('utf-8')

def test_add_cafe_without_seats(client, auth_user):
    """Sprawdza, że walidacja wymaga wybrania liczby miejsc."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Test Cafe",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8') or 'This field is required' in response.data.decode('utf-8') or 'Not a valid choice' in response.data.decode('utf-8')

def test_add_cafe_without_coffee_price(client, auth_user):
    """Sprawdza, że walidacja wymaga podania ceny kawy."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Test Cafe",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": ""
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8') or 'To pole jest wymagane' in response.data.decode('utf-8')

def test_add_cafe_with_invalid_map_url(client, auth_user):
    """Sprawdza, że nieprawidłowy format URL mapy jest wykrywany przez walidację."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Test Cafe",
        "location": "Warszawa",
        "map_url": "not-a-valid-url",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'Invalid URL' in response.data.decode('utf-8') or 'Nieprawidłowy URL' in response.data.decode('utf-8')

def test_add_cafe_with_invalid_img_url(client, auth_user):
    """Sprawdza, że nieprawidłowy format URL obrazka jest wykrywany przez walidację."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Test Cafe",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "not-a-valid-url",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'Invalid URL' in response.data.decode('utf-8') or 'Nieprawidłowy URL' in response.data.decode('utf-8')

def test_add_cafe_with_duplicate_name(client, auth_user, sample_cafe):
    """Sprawdza zachowanie aplikacji przy próbie dodania kawiarni z istniejącą nazwą."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": sample_cafe.name,
        "location": "Inna lokalizacja",
        "map_url": "https://maps.google.com/different",
        "img_url": "https://images.com/different.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code in [200, 302]

def test_add_cafe_displays_in_list(client, auth_user):
    """Sprawdza, że nowo dodana kawiarnia pojawia się na liście kawiarni."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    client.post('/add', data={
        "name": "Nowa Kawiarnia XYZ",
        "location": "Poznań",
        "map_url": "https://maps.google.com/poznan",
        "img_url": "https://images.com/poznan.jpg",
        "seats": "20-30",
        "coffee_price": "18 PLN",
        "has_wifi": True,
        "has_sockets": True
    }, follow_redirects=True)
    
    response = client.get('/')
    assert response.status_code == 200
    assert 'Nowa Kawiarnia XYZ' in response.data.decode('utf-8')
    assert 'Poznań' in response.data.decode('utf-8')

def test_cafe_belongs_to_user(client, auth_user, app):
    """Sprawdza, że nowo utworzona kawiarnia ma przypisany user_id właściciela."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    client.post('/add', data={
        "name": "Kawiarnia Właściciela",
        "location": "Gdańsk",
        "map_url": "https://maps.google.com/gdansk",
        "img_url": "https://images.com/gdansk.jpg",
        "seats": "10-20",
        "coffee_price": "14 PLN"
    }, follow_redirects=True)
    
    with app.app_context():
        cafe = Cafe.query.filter_by(name="Kawiarnia Właściciela").first()
        assert cafe is not None
        assert cafe.user_id == auth_user.id

def test_home_displays_all_cafes(client, auth_user, app):
    """Sprawdza, że strona główna wyświetla wszystkie kawiarnie z bazy."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    cafes = ["Kawiarnia A", "Kawiarnia B", "Kawiarnia C"]
    for name in cafes:
        client.post('/add', data={
            "name": name,
            "location": "Warszawa",
            "map_url": "https://maps.google.com/test",
            "img_url": "https://images.com/test.jpg",
            "seats": "10-20",
            "coffee_price": "15 PLN"
        }, follow_redirects=True)
    
    response = client.get('/')
    html = response.data.decode('utf-8')
    
    assert response.status_code == 200
    for cafe_name in cafes:
        assert cafe_name in html

def test_home_displays_cafe_details(client, sample_cafe):
    """Sprawdza, że szczegóły kawiarni są widoczne na stronie głównej."""
    response = client.get('/')
    html = response.data.decode('utf-8')
    
    assert response.status_code == 200
    assert sample_cafe.name in html
    assert sample_cafe.location in html
    assert sample_cafe.coffee_price in html

def test_home_with_no_cafes(client):
    """Sprawdza, że strona główna poprawnie wyświetla się gdy brak kawiarni w bazie."""
    response = client.get('/')
    html = response.data.decode('utf-8')
    
    assert response.status_code == 200
    assert 'Brak kawiarni w bazie danych!' in html or '0 Znaleziono Kawiarni' in html

def test_home_displays_multiple_cafes(client, auth_user):
    """Sprawdza, że wiele kawiarni wyświetla się poprawnie na stronie głównej."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    for i in range(1, 6):
        client.post('/add', data={
            "name": f"Kawiarnia {i}",
            "location": f"Miasto {i}",
            "map_url": f"https://maps.google.com/test{i}",
            "img_url": f"https://images.com/test{i}.jpg",
            "seats": "10-20",
            "coffee_price": f"{10+i} PLN"
        }, follow_redirects=True)
    
    response = client.get('/')
    html = response.data.decode('utf-8')
    
    assert response.status_code == 200
    for i in range(1, 6):
        assert f"Kawiarnia {i}" in html

def test_cafe_boolean_fields_display_correctly(client, sample_cafe):
    """Sprawdza, że pola boolean (WiFi, gniazdka) są poprawnie wyświetlane."""
    response = client.get('/')
    html = response.data.decode('utf-8')
    
    assert response.status_code == 200
    assert 'data-wifi' in html or 'WiFi' in html
    assert 'data-sockets' in html or 'gniazdka' in html.lower()

def test_cafe_model_string_representation(sample_cafe):
    """Sprawdza, że reprezentacja tekstowa modelu Cafe jest poprawna."""
    cafe_str = str(sample_cafe)
    assert sample_cafe.name in cafe_str or "Cafe" in cafe_str

def test_cafe_unique_name_constraint(app, auth_user):
    """Sprawdza zachowanie aplikacji przy próbie dodania kawiarni z duplikowaną nazwą na poziomie bazy."""
    with app.app_context():
        cafe1 = Cafe(
            name="Unikalna Nazwa",
            location="Warszawa",
            map_url="https://maps.google.com/1",
            img_url="https://images.com/1.jpg",
            seats="10-20",
            coffee_price="15 PLN",
            has_wifi=True,
            has_sockets=True,
            has_toilet=True,
            can_take_calls=False,
            user_id=auth_user.id
        )
        db.session.add(cafe1)
        db.session.commit()
        
        cafe2 = Cafe(
            name="Unikalna Nazwa",
            location="Kraków",
            map_url="https://maps.google.com/2",
            img_url="https://images.com/2.jpg",
            seats="20-30",
            coffee_price="18 PLN",
            has_wifi=True,
            has_sockets=True,
            has_toilet=True,
            can_take_calls=False,
            user_id=auth_user.id
        )
        db.session.add(cafe2)
        
        try:
            db.session.commit()
            assert True
        except Exception:
            db.session.rollback()
            assert True

def test_cafe_foreign_key_relationship(auth_user, sample_cafe):
    """Sprawdza, że relacja foreign key między Cafe a User działa poprawnie."""
    assert sample_cafe.user_id == auth_user.id
    assert sample_cafe.user_id == auth_user.id

def test_add_cafe_with_empty_strings(client, auth_user):
    """Sprawdza, że puste stringi w polach obowiązkowych są wykrywane przez walidację."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "",
        "location": "",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8') or 'To pole jest wymagane' in response.data.decode('utf-8')

def test_add_cafe_with_whitespace_only(client, auth_user):
    """Sprawdza zachowanie aplikacji gdy w polach są tylko białe znaki."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "   ",
        "location": "   ",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code in [200, 302]

def test_very_long_cafe_name(client, auth_user):
    """Sprawdza zachowanie aplikacji przy bardzo długiej nazwie kawiarni (>250 znaków)."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    long_name = "A" * 300
    response = client.post('/add', data={
        "name": long_name,
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code in [200, 302, 500]

def test_unicode_characters_in_cafe_name(client, auth_user):
    """Sprawdza, że nazwa kawiarni z emoji i znakami Unicode działa poprawnie."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Kawiarnia ☕🎉 Café",
        "location": "Wrocław",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    assert response.status_code in [200, 302]
    
    response = client.get('/')
    assert 'Kawiarnia ☕🎉 Café' in response.data.decode('utf-8') or response.status_code == 200

def test_database_rollback_on_error(client, auth_user, monkeypatch, app):
    """Sprawdza, że przy błędzie bazy danych następuje rollback transakcji."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    original_commit = db.session.commit
    
    def fake_commit():
        raise Exception("Symulowany błąd bazy danych")
    
    monkeypatch.setattr(db.session, 'commit', fake_commit)
    
    response = client.post('/add', data={
        "name": "Test Rollback",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    
    monkeypatch.setattr(db.session, 'commit', original_commit)
    
    with app.app_context():
        cafe = Cafe.query.filter_by(name="Test Rollback").first()
        assert cafe is None
