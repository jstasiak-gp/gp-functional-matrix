# Schemat macierzy funkcjonalności — format wspólny dla wszystkich produktów

> Kanoniczny, rozszerzalny format dokumentu do tworzenia macierzy funkcjonalności produktów iMap (obecnych i przyszłych).
> Źródłem prawdy jest **plik XLSX** (edytowalny przez product ownera) lub jego **eksport CSV** (do repozytorium i generatora strony WWW).
> Ten sam schemat obsługują skille: „uzupełnianie macierzy" i „sprawdzanie macierzy".

## Zasady naczelne

1. **Jeden produkt = jeden plik** o identycznych kolumnach (arkusz `Macierz`).
2. **Jeden wiersz = jedna funkcja** (jedno odrębne DZIAŁANIE), nie pojedyncza instancja ani „1 endpoint = 1 wiersz" na siłę.
3. **Zakaz zmyślania.** Każda komórka musi mieć pokrycie w kodzie / konfiguracji / dokumentacji / bazie wiedzy. Czego nie potwierdzono — zostaje **puste** i oznaczone `Status = do weryfikacji` (nie wymyślamy opisów, wersji, interfejsów, ID).
4. **Identyfikatory: dozwolone i zalecane, ale w ściśle określonej formie** (sekcja „Identyfikatory"). Zakazane są jedynie **ID wdrożeniowe/projektowe** (specyficzne dla instancji) oraz **ID kodujące pozycję w hierarchii** (typu `F-1.1.01`). Dozwolone są: stabilne **ID produktowe** i wspólne **ID kanoniczne funkcji**.
5. **Kontrolowane słowniki** dla `Typ`, `Interfejs`, `Dokumentacja`, `Źródło`, `Status` (sekcja „Słowniki").

## Arkusz `Macierz` — kolumny

| # | Nagłówek | Klucz (CSV) | Wymagana | Opis |
|---|---|---|:--:|---|
| 1 | Lp | `lp` | nie | Numer porządkowy (może nadawać skrypt). |
| 2 | ID | `id_produktu` | zalecana | ID produktowy `PREFIKS-obszar.grupa.NN` (np. `QIM-10.3.06` = 6. funkcja w grupie 10.3): produkt-obszar-grupa-funkcja. Patrz „Identyfikatory". |
| 3 | Poziom 1 – Obszar | `poziom1` | **tak** | Obszar funkcjonalny (biznes). |
| 4 | Poziom 2 – Grupa | `poziom2` | **tak** | Grupa w obrębie obszaru. |
| 5 | Funkcjonalność | `funkcjonalnosc` | **tak** | Nazwa funkcji (1 wiersz = 1 działanie). |
| 6 | Opis | `opis` | zalecana | Opis krótki, neutralny (co robi). |
| 7 | Opis biznesowy | `opis_biznesowy` | zalecana | ≈1 zdanie, styl korzyści/wymagania: „Umożliwia… / Wyświetla… / Pozwala…". |
| 8 | Typ | `typ` | **tak** | Rodzaj elementu — słownik. |
| 9 | Interfejs | `interfejs` | opc. | Dla produktów serwerowych; wielowartościowy (`;`). Klienckie: puste lub `—`. |
| 10 | Wersja / standard | `wersja_standard` | opc. | Np. `WMS 1.3.0`, `OGC API Features 1.0`. |
| 11 | Identyfikator techniczny | `identyfikator_techniczny` | zalecana | `command` / endpoint / nazwa zadania GP / operacja OGC (kilka przez `;`). |
| 12 | ID funkcji | `id_funkcji` | opc. | ID kanoniczne z rejestru wspólnego `FN-NNNNN` (np. `FN-00342`). Patrz „Identyfikatory". |
| 13 | Dokumentacja | `dokumentacja` | zalecana | Czy udokumentowane w bazie wiedzy — `TAK`/`NIE`. |
| 14 | Źródło | `zrodlo` | **tak** | Skąd pochodzi ustalenie — słownik (może być kilka przez `;`). |
| 15 | Status | `status` | **tak** | `potwierdzone` / `do weryfikacji`. |
| 16 | Rodzaj | `rodzaj` | opc. | Klasyfikacja funkcji: `podstawowa` / `rozszerzona` / `dedykowana`. |
| 17–48 | Projekt (blok checkbox) | kolumny per projekt | opc. | Jedna kolumna na projekt (MIIP … iMapCloud SaaS). Wartość `✓` = funkcja występuje w danym projekcie; pusto = nie. Zastępuje dawną tekstową kolumnę `Projekt`. Wiele projektów = wiele ✓. Lista projektów w Słownikach (rozszerzalna). |
| 49 | Uwagi | `uwagi` | opc. | Warunki, ograniczenia, zależności (odpowiednik przypisu). |

Kolumny 9–10 są **opcjonalne** i przeznaczone dla produktów serwerowych (IMS). Kolumny ID (2, 12) są opcjonalne technicznie, ale zalecane — do czasu pełnego wdrożenia rejestru mogą pozostać puste.

## Identyfikatory (ID) — model dwuwarstwowy

Rozróżniamy **dwie** niezależne warstwy identyfikacji, bo oznaczają różne rzeczy:

### Warstwa 1 — ID produktowe (`id_produktu`)
- Identyfikuje **wiersz w macierzy danego produktu**.
- Format: **`PREFIKS-obszar.grupa.NN`** — prefiks produktu + numer **obszaru** + numer **grupy** (w obrębie obszaru) + numer **funkcji** (w obrębie grupy, 2 cyfry). Obszar i grupa bez zer wiodących; segmenty rozdzielone kropką. Przykład: `QIM-10.3.06` (6. funkcja w grupie 10.3). Numery obszaru/grupy pochodzą z mapowania w arkuszu Słowniki (stałe per produkt).
- **Koduje obszar i grupę.** UWAGA: przeniesienie funkcji do innego obszaru/grupy **zmienia jej ID** — świadomy kompromis (czytelność > stabilność). Mapowanie nazw obszarów/grup na numery jest w arkuszu Słowniki każdej macierzy.
- **Niezmienne**: raz nadane nie zmienia się; numery nadawane rosnąco (append), nigdy nie renumerujemy przy wstawianiu.
- Numer **nie jest ponownie używany** po wycofaniu funkcji.

Tabela prefiksów (rozszerzalna — nowy produkt = nowy prefiks):

| Prefiks | Produkt |
|---|---|
| `IMS` | iMapServer |
| `ICL` | iMapClient |
| `QIM` | QuickiMap |
| … | (kolejne produkty dopisuje zespół) |

**Segmenty obszar.grupa (decyzja zespołu):** obszar i grupa są kodowane w ID dla czytelności (`PREFIKS-obszar.grupa.NN`). Numery obszarów (1…N w produkcie) i grup (1…M w obrębie obszaru) są utrwalone w mapowaniu w arkuszu Słowniki; numer funkcji liczony w obrębie grupy (2 cyfry). Kompromis: przeniesienie funkcji między obszarami/grupami zmienia jej ID.

### Warstwa 2 — ID kanoniczne funkcji (`id_funkcji`)
- Identyfikuje **pojęcie funkcji ponad produktami** — to samo `FN-00342` w każdym produkcie, w którym dana funkcja występuje.
- Format: **`FN-NNNNN`** (5 cyfr, nieprzezroczyste, rosnące). Przykład: `FN-00342`.
- Żyje w **jednym rejestrze wspólnym** (`rejestr_funkcji.csv`), niezależnym od pojedynczych macierzy. To on rozwiązuje problem „ta sama funkcja w różnych produktach".
- Katalog zbiorczy **kluczuje po `id_funkcji`** — porównanie „wspólne vs unikalne" staje się deterministyczne (zamiast dopasowania po samej nazwie).
- Wzorzec sprawdzony: to ta sama idea co `command_library.csv` w skillu iMapClient (rosnący rejestr współdzielony), tylko kluczem jest funkcja, nie komenda.

### Rejestr funkcji — `rejestr_funkcji.csv` (osobny plik)

| Kolumna | Opis |
|---|---|
| `id_funkcji` | `FN-NNNNN` — klucz kanoniczny. |
| `nazwa_kanoniczna` | Jedna, uzgodniona nazwa funkcji. |
| `aliasy` | Inne nazwy używane w produktach (`;`). |
| `typ` | Typ ze słownika. |
| `opis_kanoniczny` | Opcjonalny wspólny opis. |
| `produkty` | Produkty, w których występuje (może liczyć skrypt). |
| `status` | `aktywna` / `wycofana` / `scalona`. |
| `zastapiona_przez` | ID następcy (przy scaleniu/rozbiciu). |
| `uwagi` | Notatki. |

### Mechanizm zarządzania (aby nie generować problemów)

- **Centralne nadawanie.** ID nadaje skill uzupełniania / skrypt na podstawie rejestru — nie „ręcznie w Excelu". Dla funkcji już znanej **nie tworzy nowego** `id_funkcji`, tylko podpina istniejący (analogia do `--autolib`).
- **Ta sama funkcja w wielu produktach:** różne `id_produktu`, ale wspólne `id_funkcji`. Dopasowanie wspierają `nazwa_kanoniczna` + `aliasy` (normalizacja nazw). Decyzja „czy to ta sama funkcja" należy do człowieka; rejestr ją utrwala.
- **Walidacja (CI):** format ID, unikalność `id_produktu` w obrębie produktu, istnienie każdego `id_funkcji` w rejestrze, brak kolizji. Naruszenie → build czerwony.
- **Cykl życia:** wycofanie/scalenie → `status` + `zastapiona_przez` w rejestrze (historia prześledzalna). ID nigdy nie jest usuwane ani przydzielane ponownie.
- **Zysk uboczny:** stabilne ID daje trwałe **kotwice/linki** na stronie (np. `#IMS-0142`) i jednoznaczne odwołania w ofertach/przetargach.

## Słowniki (wartości dozwolone)

**Typ** (kontrolowany, wspólny dla klienta i serwera):
`widget` · `tool` · `action` · `złożona` · `usługa` · `operacja API` · `standard OGC` · `zadanie GP` · `funkcja silnika` · `format` · `źródło danych` · `mechanizm bezpieczeństwa` · `funkcja administracyjna` · `moduł` · `wdrożenie`

**Interfejs** (serwer, wielowartościowy): `REST` · `SOAP` · `WMS` · `WMTS` · `WFS` · `WPS` · `OGC API Features` · `—`

**Dokumentacja**: `TAK` · `NIE`

**Źródło**: `kod` · `konfiguracja` · `dokumentacja` · `baza wiedzy`

**Status**: `potwierdzone` · `do weryfikacji`

**Obszary / Grupy** — mapowanie nazwa→numer (OO/GG) jest w arkuszu Słowniki każdej macierzy (kolumny ID obszaru / Obszar oraz ID grupy / Obszar / Grupa); służy do budowy ID `PREFIKS-OO-GG-NNNN`.

**Rodzaj**: `podstawowa` · `rozszerzona` · `dedykowana`

**Projekt** (blok kolumn-checkboxów `✓` — jedna kolumna na projekt; lista rozszerzalna): MIIP · Centra Operacyjne · RIIP · MineSens · GEOINFO2 · ORLEN · GDOS · WIR · HydroIQ · GUGIK · NSIS · ARiMR/NGIS · UM Nowa Sól · ISOK · MZP/MRP · GAZ · CAPAP · EMUiA · ORLEN VIA · OZE · UMWL · UM Świdnica · UM Wodzisław Śląski · Wojsko · AMS · UM Racibórz · UM Kołobrzeg · GEOINFO3 · WROSIP · SIPWW · GUS · iMapCloud SaaS

## Metodyka treści (wspólna)

- **Trzy poziomy**: Poziom 1 = obszar (biznes), Poziom 2 = grupa, Funkcjonalność = konkretne działanie.
- **Jednostka funkcji**: *scalaj* warianty różniące się tylko danymi/formatem/sposobem (np. eksport csv/xlsx/shp = jeden „Eksport"); *rozbijaj*, gdy parametr zmienia cel (rysowanie linii = pomiar odległości vs poligon = pomiar powierzchni).
- **Dwa opisy**: `Opis` neutralny + `Opis biznesowy` (≈1 zdanie).
- **Funkcje złożone** (`Typ = złożona`): jedna funkcja = sekwencja kilku elementów, gdzie helper nie ma samodzielnego sensu → jeden wiersz, kilka identyfikatorów.
- **Hosting ≠ złożona**: kontenery/launchery pozostają osobnymi funkcjami; powiązania → `Uwagi`.

## Arkusz `Katalog zbiorczy` (wiele produktów — osobny plik)

| Nagłówek | Opis |
|---|---|
| ID funkcji | `FN-NNNNN` — klucz dopasowania (podstawowy). |
| Poziom 1 – Obszar, Poziom 2 – Grupa, Funkcjonalność, Opis biznesowy, Typ | jak wyżej |
| `<Produkt_1>` … `<Produkt_N>` | dostępność: `✓` / `–` (jedna kolumna na produkt) |
| Liczba produktów | liczba produktów z daną funkcją (liczy skrypt) |
| Przykłady wykorzystania | etykiety/przykłady użycia |
| Identyfikator techniczny | wspólny `command`/nazwa |
| Dokumentacja | `TAK`/`NIE` |

Dopasowanie między produktami odbywa się po `id_funkcji` (a nie po samej nazwie), co eliminuje błędy „wspólne vs unikalne".

## Arkusze pomocnicze w pliku produktu

- `Instrukcja` — jak wypełniać (dla product ownera).
- `Słowniki` — wartości dozwolone (używane też do walidacji/rozwijanych list).
- `Macierz` — dane właściwe.
- (opcjonalnie) `Załącznik techniczny` — np. macierz interfejs × funkcja dla produktów serwerowych.

## Powiązanie z generatorem strony WWW

Klucze CSV (kolumna „Klucz") są kontraktem dla generatora `generuj.py`: skrypt czyta XLSX/CSV → waliduje wg tego schematu → buduje `DATA{rows[]}` → wstrzykuje do szablonu HTML (wyszukiwarka, filtry, sortowanie). `id_produktu` służy jako trwała kotwica/URL funkcji; `id_funkcji` łączy stronę produktu z katalogiem zbiorczym. Zmiana nazw kolumn wymaga aktualizacji schematu i generatora.

---
### Status wdrożenia ID
Kolumny ID i rejestr są zdefiniowane w schemacie i szablonie. **Nadawanie ID w istniejących macierzach oraz aktualizacja walidatora/skilli/generatora to kolejny krok** (świadomie odłożony). Do tego czasu kolumny ID pozostają opcjonalne, a istniejące macierze pozostają zgodne ze schematem.

---

## Profile produktów (warianty schematu) — wariant „rdzeń + rozszerzenia"

Niektóre produkty (np. iMapCloud) mają uzasadnione odstępstwa od wspólnego schematu. Zamiast wymuszać identyczne
kolumny, stosujemy **profil produktu** — mały plik JSON w `Format macierzy/profile/<produkt>.json`, który opisuje
odstępstwa od rdzenia. Rdzeń (kolumny wymagane: Poziom 1, Poziom 2, Funkcjonalność, Typ, Źródło, Status) pozostaje wspólny.

Profil może definiować:

- `prefiks` — prefiks ID produktu (np. `CLD`).
- `aliasy_kolumn` — mapowanie nagłówka wariantowego na klucz rdzenia, np. `"Poziom 1 – Moduł" → poziom1`.
- `kolumny_wylaczone` — kolumny nieużywane przez produkt (np. `Interfejs`, `ID funkcji`).
- `kolumny_dodatkowe` — kolumny specyficzne dla produktu z własnym słownikiem, np. `Model` (Rdzeń / Rozszerzenie SaaS / Projektowe).
- `slownik_typ` — własna taksonomia `Typ` (jeśli inna niż wspólna).
- `zrodlo_wolny_tekst` — gdy `true`, kolumna `Źródło` jest wolnym tekstem (dokładne źródła), bez słownika.

Walidator obsługuje profile: `python3 sprawdz_macierz.py <plik> --profil profile/<produkt>.json`.
Bez `--profil` działa na wspólnym rdzeniu (produkty bez odstępstw nie potrzebują profilu). Profil `_bazowy.json` dokumentuje rdzeń.

### Tabela prefiksów — uzupełnienie

| Prefiks | Produkt |
|---|---|
| `IMS` | iMapServer |
| `ICL` | iMapClient |
| `QIM` | QuickiMap |
| `CLD` | iMapCloud — od „Cloud". **Świadomy wyjątek** od reguły „skrót produktu": `ICL` jest już zajęte przez iMapClient, dlatego iMapCloud używa `CLD` (zgodnie z macierzą PO). |

### Profil iMapCloud (podsumowanie)
Alias `Poziom 1 – Moduł` → `poziom1`; wyłączone `Interfejs`, `ID funkcji`; dodana kolumna `Model` (Rdzeń / Rozszerzenie SaaS / Projektowe);
własna taksonomia `Typ` (moduł, widget, narzędzie, akcja, kreator, wizualizacja, analiza, usługa, zarządzanie, administracja, integracja, import/eksport);
`Źródło` jako wolny tekst. Plik: `Format macierzy/profile/imapcloud.json`.
