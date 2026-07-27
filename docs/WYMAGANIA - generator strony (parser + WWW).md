# Wymagania — generator strony WWW z macierzami funkcjonalności (parser + strona statyczna)

> Specyfikacja dla kodu w Pythonie, który czyta macierze funkcjonalności (XLSX/CSV) i generuje **samodzielną,
> statyczną stronę** na wewnętrzną firmową dokumentację. Dokument zapisuje wymagania funkcjonalne, niefunkcjonalne,
> najważniejsze czynniki prezentacji, pułapki („na co uważać"), architekturę i kryteria akceptacji.

## 1. Kontekst i decyzje ramowe

- **Tryb:** samodzielna strona statyczna (self-contained HTML), niezależna od MkDocs — wzorzec sprawdzony w katalogu iMapClient (dane w JSON + JS: wyszukiwarka, filtry, sortowanie).
- **Źródło prawdy:** pliki **XLSX** (edytowalne przez product ownerów) → eksport **CSV** wersjonowany w Git → z CSV generowana strona.
- **Uruchamianie:** automatycznie w **CI/CD** (zmiana pliku źródłowego w repo → build → publikacja).
- **Zgodność ze schematem:** wejście musi być zgodne ze `SCHEMAT macierzy funkcjonalnosci.md` (14 kolumn, słowniki, statusy).
- **Odbiorca:** pracownicy (dokumentacja wewnętrzna); treść może trafiać także do klientów, więc jakość i czytelność jak dla odbiorcy zewnętrznego.

## 2. NAJWAŻNIEJSZE CZYNNIKI PREZENTACJI (priorytety — realizować w pierwszej kolejności)

Kolejność wynika z ustaleń. To są kryteria, wg których należy oceniać każdą decyzję projektową:

1. **Wyszukiwanie i filtrowanie (priorytet #1).** Użytkownik musi w kilka sekund znaleźć funkcję. Wymagane: pełnotekstowa wyszukiwarka (nazwa + opis + opis biznesowy + identyfikator techniczny + obszar/grupa), filtry po Poziom 1 (obszar), Typ, Dokumentacja, Status, a w katalogu zbiorczym — po produkcie. Filtry i szukanie działają natychmiastowo (bez przeładowania), łączą się (AND) i mają „Wyczyść filtry". Widoczny licznik wyników.
2. **Spójność wizualna i czytelność (priorytet #2).** Jednolity motyw firmowy (navy `#1F3864`), czytelne tabele z zamrożonym nagłówkiem, wyraźne rozróżnienie kolumn opisu, badge dla `Typ`, oraz **jednoznaczne oznaczenie wierszy `Status = do weryfikacji`** (np. żółte tło / etykieta „do weryfikacji"). Typografia i odstępy nastawione na długie listy. Responsywność (desktop przede wszystkim, ale użyteczne na tablecie).
3. **Porównanie między produktami (priorytet #3).** Widok „katalog zbiorczy": jedna funkcja = jeden wiersz, kolumny produktów z `✓/–`, licznik „liczba produktów", filtr „występuje w produkcie…", oraz szybkie odróżnienie funkcji wspólnych od unikalnych.

Eksport/druk NIE jest priorytetem (można dodać później jako „drukuj/eksport CSV", ale nie kosztem powyższych).

## 3. Architektura i przepływ (pipeline)

```
dane/
  produkty/*.xlsx           ← ŹRÓDŁO PRAWDY (edytują product ownerzy)
  produkty/*.csv            ← eksport z XLSX, wersjonowany w Git
  katalog_zbiorczy.csv      ← generowany lub utrzymywany
templates/
  produkt.html.j2           ← szablon strony produktu (CSS + JS + placeholder DATA)
  katalog.html.j2           ← szablon katalogu zbiorczego
  index.html.j2             ← strona startowa (lista produktów, statystyki)
  assets/ (styles.css, app.js)  ← wspólne, wbudowywane inline do wyniku
generuj.py                  ← parser + walidacja + budowa DATA(JSON) + render
site/                       ← WYNIK: statyczne pliki do publikacji
  index.html, <produkt>.html …, katalog.html
```

Krok po kroku: (1) wczytaj XLSX/CSV → (2) **waliduj wg schematu (twardo)** → (3) zbuduj obiekt `DATA` → (4) wstrzyknij do szablonu → (5) zapisz `site/` → (6) CI publikuje.

## 4. Wymagania funkcjonalne (FR)

### Parser / wczytywanie
- FR-1. Czyta **XLSX** (arkusz `Macierz`) i **CSV** (klucze snake_case ze schematu). Autowykrycie formatu po rozszerzeniu.
- FR-2. Mapuje kolumny wg schematu (nagłówki PL ↔ klucze CSV). Odporny na dodatkowe arkusze (Instrukcja, Słowniki) i puste wiersze.
- FR-3. **Walidacja przed generowaniem** (reużyj logiki `sprawdz_macierz.py`): brak wymaganych kolumn/pól, wartości spoza słowników, złe statusy → **build kończy się błędem** (fail-fast) z czytelnym komunikatem (plik, wiersz, problem).
- FR-4. Kodowanie **UTF-8** na każdym etapie (polskie znaki, symbole ✓ ● ◐).

### Generowanie stron
- FR-5. **Strona produktu** (`<produkt>.html`) na podstawie jednej macierzy: tabela z kolumnami Obszar / Grupa / Funkcjonalność (nazwa + opis biznesowy + identyfikator) / Typ / (Interfejs+Wersja jeśli obecne) / Status/Dokumentacja.
- FR-6. **Katalog zbiorczy** (`katalog.html`) z wielu macierzy: produkty jako kolumny `✓/–`, „liczba produktów", dopasowanie funkcji po znormalizowanej nazwie + typie.
- FR-7. **Strona startowa** (`index.html`): kafelki produktów (nazwa, liczba funkcji, % `do weryfikacji`, link) + link do katalogu zbiorczego.
- FR-8. Dane osadzone w stronie jako `const DATA = {...}` (JSON, `ensure_ascii=False`); render tabeli po stronie klienta.

### Interakcja (front-end, wbudowany JS)
- FR-9. Wyszukiwarka pełnotekstowa (pola jak w priorytecie #1), reakcja na bieżąco.
- FR-10. Filtry: Poziom 1, Typ, Dokumentacja, Status (+ Produkt w katalogu), jako chipsy/selecty; łączenie AND; „Wyczyść filtry".
- FR-11. Sortowanie kolumn po kliknięciu nagłówka (tekst wg `localeCompare('pl')`, liczby numerycznie).
- FR-12. Karty statystyk (liczba funkcji, obszarów, typów, udział „do weryfikacji").
- FR-13. Wyróżnienie wierszy `Status = do weryfikacji` i komponentów `Dokumentacja = NIE`.
- FR-14. Komunikat „brak wyników" oraz licznik „wyświetlono X z Y".

### Zawartość i integralność
- FR-15. **Nie renderować surowego HTML z danych** — każda wartość escapowana (ochrona przed wstrzyknięciem znaczników; dane pochodzą z arkuszy edytowanych ręcznie).
- FR-16. Strona MUSI pokazywać status danych — **braki i „do weryfikacji" są widoczne, nie ukrywane** (spójne z zasadą zakazu zmyślania).

## 5. Wymagania niefunkcjonalne (NFR)

- NFR-1. **Samowystarczalność**: wynik działa po otwarciu pliku/URL bez internetu — CSS/JS wbudowane inline, bez zewnętrznych CDN. (Jeśli potrzebna biblioteka — wbudować lokalnie.)
- NFR-2. **Wydajność**: płynne filtrowanie/sortowanie przy co najmniej **kilku tysiącach wierszy** (katalog zbiorczy wielu produktów). Rozważyć wirtualizację/paginację powyżej progu (np. 2000 wierszy).
- NFR-3. **Zero zależności runtime** w przeglądarce poza wbudowanym kodem; brak wywołań sieciowych.
- NFR-4. **Zależności Pythona** minimalne i deklarowane (`requirements.txt`): np. `openpyxl`, `pandas` (opcjonalnie), `jinja2`. Wersje przypięte.
- NFR-5. **Determinizm**: ten sam input → identyczny output (stabilna kolejność wierszy, brak losowości) — czyste diffy w Git.
- NFR-6. **Przeglądarki**: aktualne Chrome/Edge/Firefox; brak wymogu IE.
- NFR-7. **Dostępność/czytelność**: kontrast WCAG AA, semantyczne `<table>`, `✓/–` uzupełnione atrybutem `title`/`aria` (nie polegać wyłącznie na kolorze/symbolu).
- NFR-8. **Język**: interfejs i treść po polsku; poprawna obsługa polskiej typografii i sortowania.
- NFR-9. **Utrzymywalność**: szablony oddzielone od logiki; wspólny CSS/JS w jednym miejscu (nie duplikować per produkt).

## 6. NA CO UWAŻAĆ (pułapki — wymagania kontrolne)

- **Rozjazd schematu ↔ generator.** Generator musi walidować wg jednej definicji schematu; zmiana kolumn w arkuszu bez aktualizacji generatora ma powodować **jawny błąd**, nie ciche pominięcie kolumny.
- **Nie ukrywać braków.** Wiersze `do weryfikacji` i puste pola muszą być widoczne (filtr + wyróżnienie). Strona nie może sprawiać wrażenia kompletności tam, gdzie jej nie ma.
- **Escapowanie danych (bezpieczeństwo/renderowanie).** Wartości z arkuszy mogą zawierać `<`, `>`, `&`, cudzysłowy — zawsze escapować przed wstawieniem do HTML i do JSON.
- **Polskie znaki i kodowanie.** Wymuszać UTF-8 przy odczycie CSV/XLSX i zapisie HTML; sortowanie `localeCompare('pl')`.
- **Wydajność dużych tabel.** Przy katalogu zbiorczym (tysiące wierszy) render „wszystko naraz" może zwolnić — przewidzieć próg i mechanizm (paginacja/wirtualizacja/debounce wyszukiwania).
- **Spójność słowników między produktami.** Ten sam `Typ`/`Interfejs` musi być zapisany identycznie; generator powinien zgłaszać wartości spoza słownika (nie „naprawiać" po cichu).
- **Dopasowanie funkcji w katalogu zbiorczym.** Różne produkty nazywają funkcje różnie — potrzebna normalizacja nazw (i ewentualnie słownik nazw kanonicznych); złe dopasowanie fałszuje porównanie „wspólne vs unikalne".
- **Stabilność linków/nazw plików.** Nazwy stron produktów wyprowadzać deterministycznie z nazwy produktu (slug); unikać znaków specjalnych i spacji w nazwach plików wynikowych.
- **Wersjonowanie i data.** Każda strona powinna pokazywać wersję/datę danych źródłowych i (opcjonalnie) hash commita, żeby było wiadomo, jak „świeża" jest macierz.
- **XLSX vs CSV jako źródło prawdy.** Aby uniknąć rozjazdu, ustalić jeden kierunek: XLSX → (eksport) → CSV w repo → build. CI powinno pilnować, by CSV był aktualny względem XLSX (albo generować CSV w pipeline).
- **Puste/zdublowane wiersze.** Parser ma pomijać puste i sygnalizować duplikaty (ta sama funkcja+typ+identyfikator).

## 7. Wymagania CI/CD

- CI-1. Pipeline uruchamiany na push/merge zmieniający `dane/**`.
- CI-2. **Krok walidacji jako bramka**: `sprawdz_macierz.py` na każdym pliku; błędy → pipeline czerwony, brak publikacji.
- CI-3. (Zalecane) Generowanie/aktualizacja CSV z XLSX w pipeline, aby CSV w repo był zawsze zgodny.
- CI-4. Budowa `site/` i publikacja artefaktu na wewnętrzny serwer dokumentacji (jak obecny mechanizm publikacji bazy wiedzy).
- CI-5. Log z podsumowaniem: liczba produktów, wierszy, ostrzeżeń, udział „do weryfikacji".

## 8. Struktura repozytorium (proponowana)

`dane/produkty/*.xlsx|*.csv`, `dane/katalog_zbiorczy.csv`, `templates/*.j2`, `templates/assets/{styles.css,app.js}`, `generuj.py`, `walidacja/sprawdz_macierz.py` (współdzielony ze skillem sprawdzającym), `requirements.txt`, `README.md`, `.github/workflows/…` (lub odpowiednik CI).

## 9. Rekomendowany stos technologiczny

- **Python**: `openpyxl` (odczyt XLSX + zachowanie słowników), opcjonalnie `pandas` (CSV/agregacje), `Jinja2` (szablony), `json` (osadzanie DATA). Bez ciężkich frameworków.
- **Front-end**: czysty HTML + CSS + „vanilla" JS (wzorzec z katalogu iMapClient — filtr/sort/szukaj bez bibliotek). Jeśli zajdzie potrzeba wyszukiwania rozmytego przy dużych zbiorach — rozważyć lekką, wbudowaną lokalnie bibliotekę (np. wbudowany indeks), nadal bez CDN.

## 10. Kryteria akceptacji (Definition of Done)

- AC-1. `generuj.py` z poprawnych plików produkuje `site/` z: `index.html`, stroną każdego produktu i `katalog.html`.
- AC-2. Niepoprawny plik (brak kolumny / wartość spoza słownika) **zatrzymuje build** z czytelnym komunikatem.
- AC-3. Na stronie produktu działają: wyszukiwarka, wszystkie filtry (AND), sortowanie kolumn, licznik wyników, „Wyczyść filtry".
- AC-4. Wiersze `do weryfikacji` i `Dokumentacja = NIE` są wizualnie wyróżnione i filtrowalne.
- AC-5. Katalog zbiorczy poprawnie pokazuje `✓/–` per produkt i „liczbę produktów"; funkcje wspólne/unikalne dają się odfiltrować.
- AC-6. Strona działa offline (bez wywołań sieciowych), poprawnie renderuje polskie znaki i symbole.
- AC-7. Wynik jest deterministyczny (dwa buildy z tego samego wejścia = identyczne pliki).
- AC-8. Pipeline CI: walidacja → build → publikacja; przy błędzie danych nie publikuje.
- AC-9. Test na realnych danych: `macierz_iMapServer` (201), `macierz_iMapClient` (381), `macierz_QuickiMap` (222) generują się i są użyteczne; QuickiMap poprawnie pokazuje pozycje „do weryfikacji".

## 11. Kwestie otwarte (do doprecyzowania później)

- Czy katalog zbiorczy obejmuje całą rodzinę iMap naraz, czy osobne katalogi per linia produktowa (serwer / klient)?
- Czy potrzebny lekki eksport widoku (CSV/PDF/„drukuj") — jako funkcja drugiej fazy?
- Czy strona wymaga uwierzytelnienia/ograniczenia dostępu na serwerze wewnętrznym?
- Docelowy mechanizm publikacji (ten sam co baza wiedzy demo.gispartner.pl, czy inny).
