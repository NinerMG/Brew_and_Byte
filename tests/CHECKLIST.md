# ✅ CHECKLIST TESTÓW - Co napisać i w jakiej kolejności

## 📋 TIER 1: KRYTYCZNE (MUSISZ MIEĆ) - 30-60 min

### 🔥 Security Tests (test_cafe.py)
- [ ] `test_user_cannot_delete_other_user_cafe` - **MUST!**
- [ ] `test_user_cannot_update_other_user_cafe` - **MUST!**
- [ ] `test_user_can_only_delete_own_cafe`
- [ ] `test_user_can_only_update_own_cafe`

### ✏️ Update Tests (test_cafe.py)
- [ ] `test_update_cafe_changes_name`
- [ ] `test_update_cafe_changes_location`
- [ ] `test_update_nonexistent_cafe_returns_404`

### 🔍 Validation Tests (test_cafe.py)
- [ ] `test_add_cafe_with_invalid_map_url`
- [ ] `test_add_cafe_with_invalid_img_url`
- [ ] `test_add_cafe_without_name`

**✅ Po TIER 1: ~10-13 testów = Podstawa gotowa!**

---

## 📋 TIER 2: WAŻNE (POWINIENEŚ MIEĆ) - 1-2h

### 🗑️ Delete Tests (test_cafe.py)
- [ ] `test_delete_cafe_removes_from_database`
- [ ] `test_delete_cafe_redirects_to_home`
- [ ] `test_delete_nonexistent_cafe`
- [ ] `test_delete_cafe_shows_flash_message`

### ➕ Add Tests (test_cafe.py)
- [ ] `test_add_cafe_without_location`
- [ ] `test_add_cafe_with_duplicate_name`
- [ ] `test_add_cafe_displays_in_list`
- [ ] `test_cafe_belongs_to_user`

### 📺 Display Tests (test_cafe.py)
- [ ] `test_home_displays_all_cafes`
- [ ] `test_home_with_no_cafes`
- [ ] `test_cafe_boolean_fields_display_correctly`

### 👤 User Tests (test_user_additional_templates.py)
- [ ] `test_user_password_is_hashed`
- [ ] `test_logged_in_user_cannot_access_register`
- [ ] `test_logged_in_user_cannot_access_login`
- [ ] `test_user_relationship_with_cafes`

### 🔄 Integration Test
- [ ] `test_complete_user_journey_register_to_delete_cafe` (test_integration_templates.py)

**✅ Po TIER 2: ~28-35 testów = Bardzo dobry poziom!**

---

## 📋 TIER 3: NICE TO HAVE (WOW EFFECT) - 2-4h

### 🌍 I18n Tests (test_i18n_templates.py)
- [ ] `test_set_language_to_english`
- [ ] `test_set_language_to_polish`
- [ ] `test_language_stored_in_session`
- [ ] `test_homepage_in_polish`
- [ ] `test_homepage_in_english`
- [ ] `test_login_form_in_polish`
- [ ] `test_login_form_in_english`
- [ ] `test_flash_messages_translated_polish`
- [ ] `test_flash_messages_translated_english`
- [ ] `test_form_errors_translated_polish`

### 🛡️ Security Tests (test_security_templates.py)
- [ ] `test_password_is_hashed_not_plaintext`
- [ ] `test_password_hash_is_different_for_same_password`
- [ ] `test_xss_in_cafe_name`
- [ ] `test_xss_in_user_name`
- [ ] `test_sql_injection_in_cafe_name`

### 🎭 More Integration Tests
- [ ] `test_two_users_independent_cafes`
- [ ] `test_user_adds_multiple_cafes`
- [ ] `test_language_switch_during_session`

**✅ Po TIER 3: ~45-55 testów = IMPRESSIVE!**

---

## 📊 PODSUMOWANIE POZIOMÓW

| Poziom | Liczba testów | Czas | Gotowość |
|--------|--------------|------|----------|
| **Masz obecnie** | ~15 | - | Junior (podstawa) |
| **+ TIER 1** | ~25-28 | +1h | Junior (gotowy) ✅ |
| **+ TIER 2** | ~35-40 | +2-3h | Junior (mocny) 🔥 |
| **+ TIER 3** | ~50-60 | +4-6h | Senior Junior 🚀 |

---

## 🎯 REKOMENDACJA

### Dla staż/trainee:
✅ TIER 1 = wystarczy (25-28 testów)

### Dla Junior (0-1 rok):
✅ TIER 1 + TIER 2 = idealnie (35-40 testów)

### Dla "wow effect":
✅ Wszystkie TIER = wyróżniasz się (50+ testów)

---

## ⏱️ PLAN CZASOWY

### Dzień 1 (2h):
- [ ] TIER 1 security tests (4 testy) - 30 min
- [ ] TIER 1 update tests (3 testy) - 30 min  
- [ ] TIER 1 validation tests (3 testy) - 30 min
- [ ] Uruchom i napraw błędy - 30 min

**= 10 nowych testów**

### Dzień 2 (2-3h):
- [ ] TIER 2 delete tests (4 testy) - 45 min
- [ ] TIER 2 add tests (4 testy) - 45 min
- [ ] TIER 2 display tests (3 testy) - 30 min
- [ ] TIER 2 user tests (4 testy) - 45 min
- [ ] Integration test (1 test) - 30 min

**= 16 nowych testów**

### Dzień 3 (opcjonalnie, 2-3h):
- [ ] TIER 3 i18n tests (10 testów) - 1.5h
- [ ] TIER 3 security tests (5 testów) - 1h
- [ ] TIER 3 integration (2 testy) - 30 min

**= 17 nowych testów**

---

## ✅ TRACKING PROGRESS

```
TIER 1: [####------] 4/10 ← Zacznij tutaj!
TIER 2: [----------] 0/16
TIER 3: [----------] 0/17

TOTAL: 4/43 testów (9%)
```

Po każdym napisanym teście aktualizuj:

```
TIER 1: [##########] 10/10 ✅
TIER 2: [####------] 7/16
TIER 3: [----------] 0/17

TOTAL: 17/43 testów (40%)
```

---

## 🎯 MILESTONES

### 🥉 Milestone 1: 25 testów
**Status:** Junior ready dla staż/trainee
**Празднуй:** Masz solidną bazę! 🎉

### 🥈 Milestone 2: 35 testów  
**Status:** Junior ready dla regularnej pozycji
**Празднуй:** Jesteś w TOP 20% aplikujących! 🔥

### 🥇 Milestone 3: 50 testów
**Status:** Wyróżniasz się z tłumu
**Празднуй:** Rekruterzy będą impressed! 🚀

---

## 💡 TIPS

### ✅ Zacznij od najłatwiejszych w każdym TIER
Nie musisz po kolei! Weź ten który rozumiesz.

### ✅ Napisz 3-5 testów naraz
Potem uruchom wszystkie razem.

### ✅ Commit po każdym TIER
```bash
git add tests/
git commit -m "Add TIER 1 tests (security + validation)"
```

### ✅ Nie blokuj się na jednym teście
Jeśli coś nie działa, oznacz `@pytest.mark.skip` i wróć później.

### ✅ Pytaj jak utkniesz!
Jestem tu żeby pomóc! 😊

---

## 🚀 START!

**Następny krok:**
1. [ ] Otwórz `test_cafe_templates.py`
2. [ ] Znajdź `test_user_cannot_delete_other_user_cafe`
3. [ ] Skopiuj do `test_cafe.py`
4. [ ] Wypełnij TODO (użyj QUICK_REFERENCE.md)
5. [ ] Run: `pytest tests/test_cafe.py::test_user_cannot_delete_other_user_cafe -v`
6. [ ] Zaznacz ✅ w checkliście
7. [ ] Następny test!

**LET'S GO!** 💪

---

## 📞 POMOC

**Utknąłeś?** Napisz:
- "Jak stworzyć drugiego użytkownika?"
- "Test nie przechodzi, co robić?"
- "Jak sprawdzić czy kawiarnia została usunięta?"

**Gotowe!** 🎉
