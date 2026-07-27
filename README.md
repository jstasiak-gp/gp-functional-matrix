# Macierze funkcjonalności iMap

Wspólny format **macierzy funkcjonalności** produktów iMap + generator **samodzielnej strony statycznej**
(offline, bez backendu), pakowany w kontener Docker.

Repozytorium łączy dwie rzeczy:

1. **Paczka dla zespołu produktowego** — format, szablony, macierze produktów, skille Claude, walidator.
2. **Kontener** — `Dockerfile`, który waliduje macierze, generuje stronę i serwuje ją przez nginx.

> **Repozytorium wewnętrzne.** Macierze zawierają nazwy projektów i klientów — nie publikować poza organizacją.

## Szybki start — uruchom stronę

```bash
docker compose up -d --build
```

→ http://localhost:8080

Zatrzymanie: `docker compose down`. Skróty: `make help`.

## Struktura

| Katalog | Zawartość |
|---|---|
| `dane/produkty/` | **Źródło danych**: macierze produktów — `.xlsx` (edytuje product owner) + `.csv` (eksport, zasila build). |
| `dane/profile/` | Profile produktów (warianty schematu), np. `imapcloud.json`. |
| `dane/produkty.yaml` | **MANIFEST** — lista produktów. Dodanie produktu = edycja tego pliku, nie kodu. |
| `format/` | **Wzory dokumentów**: `SCHEMAT macierzy funkcjonalnosci.md` + szablony XLSX. |
| `generator/` | `build.py` (walidacja → generacja), `generuj_katalog.py`, `sprawdz_macierz.py`, szablon HTML. |
| `nginx/` | Konfiguracja serwera statycznego (port 8080). |
| `skille/` | Skille dla Claude: **uzupełnianie** i **sprawdzanie** macierzy. |
| `narzedzia/` | `porownaj_macierze.py` — porównanie dwóch macierzy (stara vs nowa). |
| `docs/` | Wymagania generatora strony i wytyczne projektu. |
| `site/` | **Wynik budowania** (`index.html`, `combined.json`) — generowany, niewersjonowany. |

## Zasada nr 1 — ZAKAZ ZMYŚLANIA

Do macierzy trafia **tylko to, co potwierdzone** w kodzie, konfiguracji, dokumentacji lub bazie wiedzy.
Czego nie potwierdzono — zostaje puste i dostaje `Status = do weryfikacji` (wiersz podświetla się na żółto).
Braki są **widoczne, nie ukrywane**. Nie wymyślamy nazw, opisów, wersji, interfejsów ani identyfikatorów.

## Przepływ danych

```
dane/produkty/*.xlsx   (PO edytuje)
        ↓ eksport
dane/produkty/*.csv    (wersjonowane w Git — źródło dla generatora)
        ↓ generator/build.py: walidacja (bramka) → generacja
site/index.html + site/combined.json
        ↓ nginx
strona (offline, samodzielna)
```

Build jest **deterministyczny** (ten sam input → identyczny output) i w całości **UTF-8**.
Błąd walidacji **przerywa build** — niepoprawne dane nigdy nie trafią na stronę.

## Jak pracować z macierzą (product owner)

1. Skopiuj `format/SZABLON_macierz_produktu.xlsx` i nazwij go swoim produktem.
2. Wypełnij wg `format/SCHEMAT macierzy funkcjonalnosci.md` (albo poproś Claude o skill
   **„uzupełnianie macierzy funkcjonalności"** — `skille/uzupelnianie-macierzy-funkcjonalnosci/`).
3. Zwaliduj:
   ```bash
   python generator/sprawdz_macierz.py dane/produkty/macierz_<Produkt>.xlsx
   ```
   Produkt z profilem: dodaj `--profil dane/profile/<produkt>.json`.
4. Wyeksportuj CSV do `dane/produkty/` (obok XLSX).
5. Dopisz produkt do `dane/produkty.yaml`.
6. Przebuduj stronę: `docker compose up -d --build`.

Porównanie wersji macierzy:

```bash
python narzedzia/porownaj_macierze.py --stara <stara.csv> --nowa <nowa.csv>
```

## Praca lokalna (bez Dockera)

```bash
pip install -r requirements.txt
python generator/build.py --dane ./dane --out ./site
```

Do walidacji/odczytu plików **XLSX** dodatkowo: `pip install openpyxl==3.1.5`
(build kontenerowy idzie z CSV, więc w obrazie nie jest potrzebny).

## Cele Make

| Cel | Opis |
|---|---|
| `make up` | Zbuduj i uruchom kontener (`:8080`). |
| `make down` | Zatrzymaj. |
| `make build` | Zbuduj sam obraz. |
| `make site` | Zbuduj stronę lokalnie do `./site`. |
| `make validate` | Walidacja wszystkich macierzy CSV. |
| `make regen` | Przegeneruj `./site` w kontenerze (bez lokalnego Pythona). |
| `make logs` | Logi kontenera. |

## Konfiguracja

| Element | Domyślnie | Gdzie zmienić |
|---|---|---|
| Port w kontenerze | `8080` | `nginx/default.conf` + `EXPOSE` w `Dockerfile` |
| Mapowanie portu | `8080:8080` | `docker-compose.yml` |
| Użytkownik | nieuprzywilejowany `nginx` (uid 101) | obraz bazowy `nginx-unprivileged` |
| Data danych w nagłówku | autodetekcja | `--build-arg WERSJA=RRRR-MM-DD`, `wersja_danych` w manifeście lub `SOURCE_DATE_EPOCH` |

Szczegóły wdrożeniowe (przebudowa po zmianie danych, wariant z wolumenem, uwierzytelnianie,
ścieżka bazowa) — patrz sekcja „Wdrożenie" poniżej i `docs/`.

## CI (GitHub Actions)

Workflow `.github/workflows/build.yml` uruchamia się przy zmianie `dane/**`, `generator/**`, `nginx/**`,
`Dockerfile` lub `requirements.txt` (push do `main`, pull request, albo ręcznie):

1. **Walidacja każdej macierzy** — błąd zatrzymuje pipeline (bramka jakości).
2. **Generacja strony** + kontrola, że `index.html` i `combined.json` powstały i są poprawne.
3. **Kontrola determinizmu** — dwa buildy z tego samego wejścia muszą dać identyczny wynik.
4. **Build obrazu Docker** + smoke test (kontener wstaje, strona i JSON odpowiadają HTTP 200).

Gotowa strona ląduje jako artefakt `site` (do pobrania z zakładki Actions, przechowywany 14 dni).
Workflow **nie publikuje** obrazu ani strony — wdrożenie pozostaje ręczne.

## Wdrożenie

- **Przebudowa po zmianie macierzy:** `docker compose up -d --build` (strona zapiekana w obrazie).
- **Bez przebudowy obrazu:** odkomentuj wolumen `./site:/usr/share/nginx/html:ro` w `docker-compose.yml`,
  potem `make regen` — nginx serwuje świeże pliki od razu.
- **Uwierzytelnianie:** obraz nie ma auth. Basic Auth / SSO / VPN dodaj na reverse-proxy przed kontenerem.
- **Ścieżka bazowa:** strona to jeden `index.html` w korzeniu — działa pod dowolnym URL-em.
- **Na przyszłość:** `combined.json` to gotowy eksport danych — może zasilić zewnętrzną wyszukiwarkę
  (ElasticSearch/OpenSearch) bez zmian w obrazie.

## Dokumentacja

- `format/SCHEMAT macierzy funkcjonalnosci.md` — **źródło prawdy o formacie** (kolumny, słowniki, ID, profile).
- `docs/WYMAGANIA - generator strony (parser + WWW).md` — wymagania funkcjonalne i niefunkcjonalne strony.
- `docs/WYTYCZNE PROJEKTU - macierze funkcjonalnosci (analiza zespolowa).md` — wytyczne i ustalenia zespołu.
- `CLAUDE.md` — instrukcje pracy z tym repozytorium dla Claude.
