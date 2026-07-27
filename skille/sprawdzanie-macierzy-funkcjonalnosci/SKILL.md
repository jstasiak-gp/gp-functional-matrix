---
name: sprawdzanie-macierzy-funkcjonalnosci
description: >
  Sprawdza (waliduje) macierz funkcjonalności produktu iMap pod kątem zgodności ze wspólnym
  SCHEMATEM, kompletności, spójności słowników oraz ryzyka danych niepotwierdzonych/zmyślonych.
  Użyj, gdy product owner chce zweryfikować macierz (XLSX/CSV) przed publikacją, sprawdzić braki,
  spójność Poziomów/Typów/Interfejsów/ID albo przygotować macierz do generatora strony WWW.
  Produktem jest RAPORT walidacji (błędy, ostrzeżenia, statystyki, lista braków do uzupełnienia).
  Skill niczego nie zmyśla — wskazuje braki i wymaga ich potwierdzenia przez człowieka.
  Słowa-klucze: sprawdzenie macierzy, walidacja, kontrola jakości, kompletność, spójność, QA macierzy.
---

# Sprawdzanie macierzy funkcjonalności (dla product ownerów)

Skill weryfikuje macierz zbudowaną wg wspólnego formatu (`SCHEMAT macierzy funkcjonalnosci.md`) i zwraca
**raport**: co jest niezgodne (błędy), co budzi wątpliwości (ostrzeżenia), statystyki oraz **listę braków do uzupełnienia**.
Skill **nie poprawia danych po cichu** i **nie dopisuje treści** — wskazuje problemy do decyzji człowieka.

## Zasada nadrzędna

- Skill **nie uzupełnia ani nie zmyśla** brakujących danych. Rolą jest wykrycie i zaraportowanie.
- Wszystko, czego nie da się potwierdzić w macierzy, ma być zgłoszone jako **brak do weryfikacji**, nie „naprawione".

## Wejście

- Plik macierzy: `XLSX` (arkusz `Macierz`) lub `CSV` zgodny ze schematem.
- (opcjonalnie) `rejestr_funkcji.csv` — do kontroli `ID funkcji` (parametr `--rejestr`).
- (opcjonalnie) materiały źródłowe produktu — do kontroli krzyżowej (czy funkcje mają pokrycie).

## Co sprawdza

### 1. Zgodność ze schematem (BŁĄD, jeśli niespełnione)
- Obecne wszystkie **wymagane** kolumny (Poziom 1, Poziom 2, Funkcjonalność, Typ, Źródło, Status).
- Kolumny spoza schematu → OSTRZEŻENIE (są ignorowane). Kolumny ID są opcjonalne i dozwolone.

### 2. Kompletność wierszy
- Wymagane niepuste: `Poziom 1`, `Poziom 2`, `Funkcjonalność`, `Typ`, `Źródło`, `Status` (BŁĄD, jeśli puste; `Typ` może być pusty tylko przy `Status = do weryfikacji`).
- `Opis` lub `Opis biznesowy` obecny — OSTRZEŻENIE, jeśli oba puste.
- Duplikaty (ta sama `Funkcjonalność` + `Typ` + `Identyfikator techniczny`) — OSTRZEŻENIE.

### 3. Spójność słowników (BŁĄD)
- `Typ` ∈ słownik; `Interfejs` (po rozbiciu `;`) ∈ słownik; `Dokumentacja` ∈ {TAK,NIE}; `Status` ∈ {potwierdzone, do weryfikacji}; `Źródło` (po `;`) ∈ słownik.

### 3b. Identyfikatory ID — jeśli obecne (BŁĄD)
- Kolumny `ID` i `ID funkcji` są opcjonalne; sprawdzane tylko, gdy wypełnione.
- `ID` (produktowe) musi pasować do `PREFIKS-obszar.grupa.NN` (np. `QIM-10.3.06`) i być **unikalne** w pliku.
- `ID funkcji` musi pasować do `FN-NNNNN`; z opcją `--rejestr rejestr_funkcji.csv` sprawdzane jest też **istnienie w rejestrze**.

### 4. Kontrola „anty-zmyślanie" (OSTRZEŻENIE)
- `Status = potwierdzone`, ale `Źródło` puste → podejrzane.
- `Status = potwierdzone`, a jednocześnie brak jakiegokolwiek zakotwiczenia (pusty `Identyfikator techniczny` ORAZ pusty `Opis` ORAZ pusty `Opis biznesowy`) → prawdopodobnie niepotwierdzone.
- Wiersz z `Wersja/standard` bez `Interfejs` → do sprawdzenia.
- (jeśli dostarczono kod/konfigurację) `Identyfikator techniczny`, którego NIE znaleziono w materiałach → oznacz jako możliwe zmyślenie / literówkę.

### 5. Statystyki i gotowość do publikacji
- Liczba funkcji; udział `do weryfikacji`; udział `Dokumentacja = NIE`; liczba wierszy z `ID`/`ID funkcji`; rozkład po `Poziom 1` i `Typ`.
- „Gotowość do generatora": brak błędów krytycznych + 0 pustych pól wymaganych (poza `do weryfikacji`).

## Procedura

1. Wczytaj macierz (XLSX/CSV). Rozpoznaj arkusz `Macierz`.
2. Uruchom walidator: `python3 generator/sprawdz_macierz.py <plik> [--rejestr rejestr_funkcji.csv]` (zwraca JSON: `errors`, `warnings`, `stats`). Ścieżki podawaj od korzenia repozytorium.
3. Jeśli dostarczono materiały źródłowe — wykonaj kontrolę krzyżową identyfikatorów technicznych i istnienia funkcji.
4. Zbuduj **czytelny raport** (poniżej). Nie modyfikuj danych.
5. Jeśli są błędy/braki — sformułuj konkretne pytania i listę „do uzupełnienia" dla product ownera; zaproponuj użycie skilla „uzupełnianie macierzy funkcjonalności".

## Format raportu (zwróć użytkownikowi)

- **Podsumowanie**: liczba wierszy, błędów, ostrzeżeń; werdykt „gotowa / do poprawy".
- **Błędy** (muszą zniknąć przed publikacją) — lista z numerami wierszy.
- **Ostrzeżenia** — lista z numerami wierszy.
- **Braki do uzupełnienia** — czego brakuje i w których obszarach; jakich materiałów potrzeba.
- **Statystyki** — rozkłady i udział `do weryfikacji`.

## Weryfikacja samego skilla
- Raport nie zawiera propozycji „zmyślonych" wartości — tylko wskazania braków.
- Numery wierszy w raporcie zgadzają się z plikiem.

## Profile produktów

Dla produktów z wariantem schematu uruchom walidator z profilem:
`python3 generator/sprawdz_macierz.py <plik> --profil dane/profile/<produkt>.json`.
Profil obsługuje aliasy kolumn, kolumny wyłączone/dodatkowe (z własnym słownikiem), własną taksonomię `Typ`
oraz `Źródło` jako wolny tekst. Bez `--profil` walidacja działa na wspólnym rdzeniu (zgodność wsteczna).
