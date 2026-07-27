# Wytyczne projektu „Macierze funkcjonalności" — analiza prac zespołu i standard docelowy

> Dokument nadrzędny dla całego projektu. Powstał z dokładnej analizy materiałów wytworzonych przez zespół produktowy
> (folder „Macierze stworzone przez zespół produktowy") oraz skilla użytego do najlepiej przygotowanej macierzy (iMapClient).
> Cel końcowy projektu: **podstrona bazy wiedzy z macierzami dla każdego produktu**, generowana **skryptem Python**
> z **łatwo edytowalnych plików Excel/CSV**.

---

## 1. Co przeanalizowano

| Artefakt | Typ | Rola |
|---|---|---|
| `macierz-funkcjonalnosci.md` | Skill (metodyka) | Najbardziej dojrzały, powtarzalny proces (iMapClient) |
| `Diagram1_budowanie_macierzy.png` | Diagram | Wizualizacja procesu ze skilla |
| `iMapServer-funkcjonalnosci-v3.xlsx` | Macierz produktu | Ujęcie kategoriami + „Zadania GP" |
| `QuickiMap - Macierz funkcjonalnosci v1.0.xlsx` | Macierz produktu | Ujęcie Obszar/Kategoria + ID |
| `Katalog_zbiorczy_iMapClient 1.xlsx` | Katalog zbiorczy | Wiele projektów w kolumnach ✓/– |
| `Katalog_funkcjonalnosci_iMapClient 5.html` | Strona WWW (wzorzec) | **Interaktywna**, dane w JSON + JS (filtry, wyszukiwarka) |
| `ims-query-catalog 1.html` | Strona WWW (wzorzec) | **Statyczna**, edytorska (sekcje, bez danych/JS) |

Wniosek wstępny: zespół wypracował **dwa poziomy dojrzałości**. Najwyższy to linia iMapClient (skill → macierz projektu → katalog zbiorczy → interaktywna strona z JSON). Pozostałe macierze (iMapServer, QuickiMap) są dobre merytorycznie, ale **niespójne strukturalnie** — to główny problem do ujednolicenia.

---

## 2. Elementy wspólne wszystkich macierzy

Mimo różnic, powtarza się ten sam rdzeń:

1. **Hierarchiczna kategoryzacja** funkcji (2–3 poziomy zagnieżdżenia).
2. **Nazwa funkcjonalności** — jeden wiersz = jedna funkcja.
3. **Opis** — co najmniej jedno pole opisowe; w lepszych macierzach dwa (neutralny + biznesowy).
4. **Identyfikator techniczny** funkcji (command / nazwa techniczna) — łącznik z kodem.
5. **Grupowanie tematyczne** spójne w obrębie produktu (np. nawigacja, dane, edycja, administracja).
6. W ujęciu wieloproduktowym: **produkty jako kolumny** z oznaczeniem dostępności (✓/–), licznikiem i przykładami.

To jest fundament wspólnego schematu (sekcja 4).

---

## 3. Różnice do ujednolicenia (obecny stan)

| Aspekt | iMapClient (katalog) | iMapServer v3 | QuickiMap | Macierz IMS 5.1 (nasza) |
|---|---|---|---|---|
| Poziomy | Poziom 1 / Poziom 2 | 1 × Kategoria | Obszar / Kategoria | Kategoria + oś interfejsu |
| Opis | Opis biznesowy | Opis + Opis biznesowy | Opis | Opis + Uwagi |
| Typ | widget/tool/action/złożona | (Nazwa techniczna) | — | — |
| ID/technika | Command(y) | Nazwa techniczna | ID (Lp.) | — |
| Kolumna ID wdrożeniowa | NIE (świadomie) | nie | TAK | nie |
| Oś główna | funkcje wg działania | kategorie | obszary | **interfejs dostępu** |
| Dostępność per produkt | ✓/– (9 proj.) | n/d | n/d | n/d |

Najważniejsze rozbieżności: **liczba i nazwy poziomów**, **jedna vs dwie kolumny opisu**, obecność **ID** (skill zaleca ich brak), oraz to, że **nasza macierz IMS przyjęła inną oś** (interfejs dostępu) niż reszta produktów (kategorie funkcji). Do wspólnej strony wszystkie muszą trafić w **jednym schemacie** (sekcja 4 i 8).

---

## 4. Rekomendowany ujednolicony schemat danych (źródło = CSV/XLSX)

Dane trzymamy w plikach edytowalnych; **każdy produkt = jeden plik** o identycznych kolumnach. Kolumny (nagłówki w wierszu 1):

### 4.1 Macierz pojedynczego produktu — `<produkt>.csv`

| Kolumna | Wymagana | Opis | Słownik / format |
|---|:--:|---|---|
| `poziom1` | tak | Obszar funkcjonalny (biznes) | tekst |
| `poziom2` | tak | Grupa | tekst |
| `funkcjonalnosc` | tak | Nazwa funkcji (1 wiersz = 1 działanie) | tekst |
| `opis` | tak | Opis krótki, neutralny | tekst |
| `opis_biznesowy` | tak | 1 zdanie „Umożliwia… / Wyświetla… / Pozwala…" | tekst |
| `typ` | tak | Rodzaj elementu | `widget` \| `tool` \| `action` \| `usługa` \| `zadanie GP` \| `złożona` |
| `identyfikator_techniczny` | zalecana | command / nazwa techniczna / endpoint | tekst (kilka rozdzielonych `;`) |
| `dokumentacja` | zalecana | Czy udokumentowane w bazie wiedzy | `TAK` \| `NIE` |
| `uwagi` | opcjonalna | Warunki, ograniczenia (odpowiednik przypisu) | tekst |

Zasady: **bez kolumn ID wdrożeniowych** (zgodnie ze skillem — są specyficzne dla projektu). Puste `poziom1/poziom2` niedozwolone (nie używamy „wierszy-sekcji" jak w QuickiMap — utrudniają parsowanie; kategoria musi być w każdej komórce).

### 4.2 Katalog zbiorczy (wiele produktów) — `katalog_zbiorczy.csv`

| Kolumna | Opis |
|---|---|
| `poziom1`, `poziom2`, `funkcjonalnosc`, `opis_biznesowy`, `typ` | jak wyżej (klucz dopasowania: `funkcjonalnosc` znormalizowana + `typ`) |
| `<Produkt_1>` … `<Produkt_N>` | dostępność: `✓` / `–` (jedna kolumna na produkt) |
| `liczba_produktow` | liczba produktów, w których funkcja występuje (może liczyć skrypt) |
| `przyklady` | etykiety/przykłady użycia |
| `identyfikator_techniczny` | wspólny command / nazwa |
| `dokumentacja` | `TAK`/`NIE` |

To 1:1 model z działającego katalogu iMapClient (`DATA.rows[]`: `p1,p2,name,biz,typ,proj{},np,use,cmds,dok`).

---

## 5. Metodyka tworzenia treści (przeniesiona ze skilla iMapClient)

Zasady, które podniosły jakość macierzy iMapClient — **do stosowania we wszystkich produktach**:

- **Trzy poziomy**: P1 = obszar (biznes), P2 = grupa, P3 = konkretna funkcja (= `funkcjonalnosc`).
- **Jednostka funkcji** — jedna funkcja = jedno odrębne DZIAŁANIE:
  - *Scalaj*, gdy warianty różnią się tylko DANYMI/formatem/sposobem (np. eksport csv/xlsx/shp = jeden „Eksport").
  - *Rozbijaj*, gdy parametr zmienia DZIAŁANIE/cel (np. rysowanie linii = pomiar odległości, poligonu = pomiar powierzchni).
- **Dwa opisy**: `opis` (krótki, neutralny) + `opis_biznesowy` (≈1 zdanie w stylu wymagania). Ten drugi jest bezcenny przy przetargach.
- **Funkcje złożone** (`typ = złożona`): jedna funkcja realizowana przez SEKWENCJĘ kilku komend, gdzie helper nie ma sensu samodzielnie (np. Identyfikacja = narzędzie + widget wyników + zoom). Jeden wiersz, wiele `identyfikator_techniczny`.
- **Hosting ≠ funkcja złożona**: kontenery/launchery (okno mapy, panel dokowany) pozostają osobnymi funkcjami; powiązania idą do „uwag/powiązań", nie tworzą kompozytu.
- **Biblioteka wielokrotnego użytku** (`command_library.csv`): rosnący słownik `command → poziomy, nazwa, opisy`. Nie wymyślać na nowo opisów funkcji już znanych; po każdym produkcie dopisywać nowe. To klucz do spójności między produktami i do szybszego opisywania kolejnych.
- **Kontrola kompletności**: każdy element ma P1/P2/P3; każda użyta komenda ma wpis w bibliotece; oznaczanie braków w dokumentacji (`dokumentacja = NIE`).

Proces (wg diagramu): źródła danych → ekstrakcja → opisy z bazy wiedzy → mapowanie funkcji (biblioteka) → funkcje złożone → budowa pliku → weryfikacja → wynik (macierz produktu + katalog zbiorczy).

---

## 6. Architektura docelowej strony (Python → JSON → HTML)

Wzorzec sprawdzony w katalogu iMapClient: dane osadzone jako `const DATA = {projects, rows}`, a strona renderuje tabelę po stronie klienta z wyszukiwarką, filtrami (chipsy) i sortowaniem. **Standaryzujemy ten wzorzec** i automatyzujemy generowanie.

### 6.1 Przepływ (pipeline)

```
dane/                         (edytowalne przez zespół)
  produkty/
    imapserver.csv
    imapclient.csv
    quickimap.csv
    ...
  katalog_zbiorczy.csv
templates/
  produkt.html.j2   (szablon strony produktu: CSS + JS + placeholder na DATA)
  katalog.html.j2   (szablon katalogu zbiorczego)
  index.html.j2     (strona startowa z listą produktów)
generuj.py           →  wczytuje CSV (pandas) → waliduje schemat → buduje DATA(JSON)
                        → wstrzykuje do szablonu → zapisuje site/
site/                 (wynik — statyczne pliki do wrzucenia do bazy wiedzy)
  index.html
  imapserver.html
  imapclient.html
  ...
  katalog.html
```

### 6.2 Zasady generatora

- **Wejście**: CSV (preferowane — łatwe do diffów w Git) lub XLSX (dla wygody edycji). Skrypt obsługuje oba (`pandas.read_csv` / `read_excel`).
- **Walidacja**: sprawdź obecność wymaganych kolumn, dozwolone wartości `typ`, brak pustych `poziom1/2/funkcjonalnosc`. Błędy → przerwij z czytelnym komunikatem (odpowiednik `check_library.py`).
- **Budowa DATA**: dla strony produktu `rows[] = {p1,p2,name,opis,biz,typ,cmds,dok,uwagi}`; dla katalogu dodatkowo `proj{}`, `np`, `use`.
- **Szablon**: jeden wspólny CSS (motyw navy, karty statystyk, chipsy) + JS (filtr/sort/szukaj). Trzymać w `templates/`, nie duplikować w danych.
- **Strona produktu**: filtry po `poziom1`, `typ`, `dokumentacja`; wyszukiwarka po nazwie/opisie/command; sortowalne kolumny; licznik wyświetlonych.
- **Katalog zbiorczy**: dodatkowo filtr „występuje w produkcie…", kolumny produktów, licznik `liczba_produktow`.
- **`index.html`**: kafelki produktów (nazwa, liczba funkcji, link) + link do katalogu zbiorczego.
- **Bez zależności zewnętrznych** w wyniku (self-contained HTML) — jak obecne katalogi; ewentualnie tylko wbudowany CSS/JS.

### 6.3 Rekomendacje techniczne

- Silnik szablonów: **Jinja2** (czytelne, standard). JSON osadzać przez `json.dumps(..., ensure_ascii=False)`.
- Kodowanie **UTF-8** wszędzie (polskie znaki, symbole ✓ ● ◐).
- Repozytorium: dane i szablony wersjonowane w Git; `generuj.py` uruchamiany ręcznie lub w CI, wynik `site/` publikowany w bazie wiedzy (analogicznie do MkDocs).
- Rozważyć spójność z istniejącą bazą wiedzy (MkDocs Material) — strony można podpiąć jako sekcję „Macierze funkcjonalności".

---

## 7. Standard wizualny / UX (z katalogu iMapClient — do zachowania)

- Nagłówek z gradientem (motyw firmowy navy `#1F3864`), karty statystyk (liczba funkcji, obszarów, typów).
- Panel filtrów: pole wyszukiwania, select obszaru (P1), chipsy typu, chipsy dokumentacji, „Wyczyść filtry".
- Tabela: kolumny Obszar / Grupa / Funkcjonalność (nazwa + opis biznesowy + command) / Typ / (produkty), sortowanie po kliknięciu nagłówka, badge kolorystyczny dla typu, licznik wyników, komunikat „brak wyników".
- Responsywność (siatka statystyk `auto-fit`, `max-width` kontenera).

---

## 8. Rekomendacje spójności (decyzje do podjęcia)

1. **Ujednolicić oś macierzy IMS.** Nasza macierz IMS 5.1 używa osi „interfejs dostępu" (REST/SOAP/OGC), a reszta produktów — kategorii funkcji. Do wspólnej strony należy przekształcić IMS do wspólnego schematu: `poziom1/poziom2/funkcjonalnosc/...`, a informację o interfejsie przenieść do `typ`/`uwagi` lub dodatkowej kolumny „Interfejs". (Macierz interfejsowa może zostać jako widok pomocniczy.)
2. **Ustalić liczbę poziomów: 3** (P1/P2/P3) jako standard; produkty z 1–2 poziomami uzupełnić.
3. **Zawsze dwie kolumny opisu** (`opis` + `opis_biznesowy`).
4. **Usunąć kolumny ID** z macierzy produktowych (QuickiMap) — zgodnie z metodyką skilla.
5. **Zunifikować słownik `typ`** (sekcja 4.1) w skali całego pakietu produktów.
6. **Prowadzić wspólną `command_library.csv`** dla całego pakietu, nie tylko iMapClient.

---

## 9. Pytania / kwestie otwarte

- Czy dane trzymamy jako **CSV** (lepsze do Git/diff) czy **XLSX** (wygodniejsza edycja dla zespołu)? Rekomendacja: XLSX jako edytowalne źródło + eksport do CSV w repo.
- Czy strona ma być **osobną podstroną** czy **sekcją w istniejącym MkDocs** bazy wiedzy?
- Czy potrzebne są **kolumny przetargowe** (ID wymagania / status / uwagi) jako opcjonalny widok?
- Jak głęboko rozbijać **funkcje złożone** dla produktów serwerowych (IMS) vs klienckich (iMapClient)?
- Czy katalog zbiorczy obejmuje **całą rodzinę iMap** (serwer + klienci + QuickiMap), czy osobne katalogi per linia produktowa?

---

## 10. Proponowane następne kroki

1. Zatwierdzić **wspólny schemat** (sekcja 4) i słownik `typ`.
2. Przekształcić istniejące macierze (IMS, QuickiMap) do schematu → pliki `dane/produkty/*.csv`.
3. Zbudować **`generuj.py`** + szablony Jinja2 na bazie działającego katalogu iMapClient (odzyskać z niego CSS/JS jako szablon startowy).
4. Wygenerować `site/` (index + strony produktów + katalog zbiorczy) i podpiąć do bazy wiedzy.
5. Uruchomić wspólną `command_library.csv` i proces jej utrzymania po każdym produkcie.

---

### Załącznik: model danych działającego katalogu iMapClient (do odtworzenia w generatorze)

```js
const DATA = {
  projects: ["ARiMR","GDOŚ","GUGiK","ORLEN","PGWWP WIR","Hydroportal","UMWZ RIIP","GEOINFO 2","Centra Operacyjne"],
  rows: [
    { p1:"Nawigacja i obsługa mapy", p2:"Nawigacja po mapie", name:"Następny zasięg",
      biz:"Umożliwia przejście do następnego zasięgu widoku mapy.", typ:"action",
      proj:{ "ARiMR":true, "GUGiK":false, ... }, np:8, use:"", cmds:"map-navigation-action", dok:"TAK" }
    // ...
  ]
};
```
Strona renderuje `rows` do tabeli z filtrami (obszar/typ/projekt/dokumentacja), wyszukiwarką (nazwa+opis+command+przykład) i sortowaniem — ten sam mechanizm ma produkować `generuj.py` dla każdego produktu.
