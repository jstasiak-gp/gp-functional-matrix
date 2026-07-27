# CLAUDE.md — instrukcje pracy z repozytorium „Macierze funkcjonalności iMap"

> Przeczytaj ten plik najpierw. Obowiązuje w całym repozytorium.

## Twoja rola

Pomagasz product ownerom **tworzyć, porównywać, analizować i uzupełniać macierze funkcjonalności**
produktów iMap we wspólnym formacie, oraz utrzymywać generator strony i kontener.

## ZASADA NR 1 — ZAKAZ ZMYŚLANIA (bezwzględna)

- Wpisujesz **wyłącznie** to, co potwierdzone w dostarczonych materiałach (kod / konfiguracja / dokumentacja / baza wiedzy).
- Nie zgadujesz nazw, opisów, wersji, interfejsów, identyfikatorów ani dostępności funkcji.
- Czego nie potwierdzisz → zostaw puste, ustaw `Status = do weryfikacji`, opisz brak w `Uwagi`.
- Zawsze na końcu podaj **raport braków**: czego brakuje, by macierz była kompletna.
- Nie modyfikujesz materiałów źródłowych (tylko odczyt).

## Gdy polecenie jest ogólne („przeanalizuj to")

**Nie zgaduj zadania.** Zadaj jedno zwięzłe pytanie doprecyzowujące i zaproponuj tryby:
(1) uzupełnienie/rozbudowa macierzy z nowego źródła, (2) porównanie nowych danych z obecną macierzą,
(3) walidacja macierzy, (4) nowa macierz od szablonu, (5) budowa/uruchomienie strony lub kontenera.

Dopytaj o: **którego produktu** dotyczy, **gdzie jest źródło prawdy** (kod/dokumentacja/konfiguracja)
i **czy masz do niego dostęp**.

## Mapa repozytorium

| Ścieżka | Rola |
|---|---|
| `format/SCHEMAT macierzy funkcjonalnosci.md` | **ŹRÓDŁO PRAWDY o formacie** — kolumny, słowniki, reguły, ID, profile. |
| `format/SZABLON_macierz_produktu.xlsx` | Pusty szablon nowej macierzy. |
| `dane/produkty/*.xlsx` \| `*.csv` | Macierze produktów: XLSX edytowalny + CSV (zasila generator). |
| `dane/profile/*.json` | Profile produktów (warianty schematu). |
| `dane/produkty.yaml` | **MANIFEST** — lista produktów dla generatora. |
| `generator/build.py` | Pipeline: walidacja (bramka) → generacja → podsumowanie. |
| `generator/sprawdz_macierz.py` | **Walidator** (kanoniczny, jedna kopia). |
| `generator/generuj_katalog.py` | Generator strony (`--dane`, `--out`, `--wersja`). |
| `narzedzia/porownaj_macierze.py` | Porównanie dwóch macierzy. |
| `skille/` | Skille: uzupełnianie i sprawdzanie macierzy. |
| `docs/` | Wymagania strony i wytyczne projektu. |
| `site/` | Wynik budowania — **generowany**, nie edytuj ręcznie. |

## Runbook: „nowe źródło danych produktu X"

1. **Rozpoznanie.** Ustal produkt X i jego macierz w `dane/produkty/`. Ustal, co dostarczono jako źródło.
2. **Przeczytaj format i skill.** `format/SCHEMAT macierzy funkcjonalnosci.md` +
   `skille/uzupelnianie-macierzy-funkcjonalnosci/SKILL.md`.
3. **Zbuduj kandydata** wg schematu (kolumny, słowniki, `Źródło`, `Status`). Braki → puste + `do weryfikacji`.
4. **Porównaj z obecną macierzą:**
   ```bash
   python narzedzia/porownaj_macierze.py --stara dane/produkty/macierz_<X>.csv --nowa <kandydat>.csv
   ```
5. **Scal / uzupełnij.** Nowe funkcje dodaj; istniejące uzupełnij tylko potwierdzonymi danymi.
   Zachowaj istniejące `ID` (nigdy nie zmieniaj).
6. **Zwaliduj:**
   ```bash
   python generator/sprawdz_macierz.py <plik> [--profil dane/profile/<produkt>.json]
   ```
7. **Oddaj wynik**: zaktualizowana macierz (XLSX + CSV w `dane/produkty/`) + raport różnic, liczby
   potwierdzone vs do weryfikacji, lista braków i pytań do product ownera.

## Runbook: strona / kontener

- Build lokalny: `python generator/build.py --dane ./dane --out ./site`
- Kontener: `docker compose up -d --build` → http://localhost:8080
- Walidacja jest **bramką** — błąd przerywa build. Nie obchodź jej, tylko popraw dane.
- Build musi zostać **deterministyczny** (bez losowości i bieżącej daty w treści) i **UTF-8**.
- Lista produktów pochodzi **wyłącznie** z `dane/produkty.yaml` — nie wpisuj produktów do kodu.

## Czego NIE robić

- Nie zaczynaj pracy „w ciemno", gdy polecenie było ogólne — dopytaj.
- Nie zmyślaj danych ani ID. Nie „domykaj" luk zgadywaniem.
- Nie zmieniaj schematu ani nazw kolumn bez ustalenia (zepsuje walidator i generator).
- Nie nadpisuj cudzych macierzy bez porównania i zgody.
- Nie edytuj `site/` — to artefakt generowany.
- Nie commituj i nie pushuj bez wyraźnej prośby.

## Uwagi

- Kodowanie zawsze **UTF-8** (polskie znaki, symbole ✓ ● ◐).
- To repozytorium **wewnętrzne** — macierze zawierają nazwy projektów i klientów.
