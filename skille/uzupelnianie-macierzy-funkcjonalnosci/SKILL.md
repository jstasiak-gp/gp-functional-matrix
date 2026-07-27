---
name: uzupelnianie-macierzy-funkcjonalnosci
description: >
  Tworzy lub uzupełnia macierz funkcjonalności produktu iMap we wspólnym formacie firmowym,
  na podstawie dostarczonych materiałów: dokumentacji (md, pdf, docx, html), kodu źródłowego
  i/lub plików konfiguracyjnych. Użyj, gdy product owner chce zbudować albo rozszerzyć
  "macierz funkcjonalności" / "rejestr funkcji" swojego produktu. Produktem jest plik XLSX
  (+ eksport CSV) zgodny ze SCHEMATEM macierzy funkcjonalności. Skill NIE wymyśla danych:
  wpisuje wyłącznie fakty potwierdzone w źródłach, a braki jasno oznacza do weryfikacji.
  Słowa-klucze: macierz funkcjonalności, rejestr funkcjonalności, funkcje produktu, analiza kodu,
  analiza dokumentacji, konfiguracja, product owner.
---

# Uzupełnianie macierzy funkcjonalności (dla product ownerów)

Skill buduje/uzupełnia macierz funkcjonalności dowolnego produktu iMap w **jednym, wspólnym formacie**,
tak aby macierze wszystkich produktów były spójne i nadawały się do wspólnej strony bazy wiedzy.

## Zasada nadrzędna — ZAKAZ ZMYŚLANIA (czytaj najpierw)

- **Wpisuj wyłącznie to, co potwierdzone w dostarczonych materiałach** (kod, konfiguracja, dokumentacja, baza wiedzy).
- **Nigdy nie zgaduj** nazw funkcji, opisów, wersji, interfejsów, identyfikatorów technicznych ani dostępności.
- Czego nie da się potwierdzić — **zostaw puste** i ustaw `Status = do weryfikacji`, a w `Uwagi` napisz czego brakuje.
- Każdy wiersz musi mieć wypełnione `Źródło` (skąd pochodzi ustalenie). Brak źródła = wiersz niedozwolony.
- Na końcu **zawsze** przedstaw listę braków i pytań (sekcja „Raport kompletności"); jasno komunikuj, jakich materiałów potrzeba, by macierz była kompletna.
- Jeśli materiały są sprzeczne — nie rozstrzygaj arbitralnie; oznacz `do weryfikacji` i opisz rozbieżność.

## Wejścia (poproś o to, czego brakuje)

Product owner może dostarczyć dowolną kombinację:

1. **Dokumentacja** — pliki `.md`, `.pdf`, `.docx`, `.html`, strony bazy wiedzy, opisy usług.
2. **Kod źródłowy** — repozytorium/foldery (np. kontrolery REST, rejestry zadań, definicje usług, moduły).
3. **Pliki konfiguracyjne** — np. `application.properties`, konfiguracje projektu, definicje widgetów/akcji/narzędzi, pliki `*.gdb`, itp.

Jeśli którejś kategorii brakuje, a jest potrzebna do kompletności — **poproś o jej dostarczenie**. Nie uzupełniaj luk domysłami.
Materiały źródłowe traktuj jako **tylko do odczytu** — nie modyfikuj ich.

## Format wyjściowy

Zgodny ze `SCHEMAT macierzy funkcjonalnosci.md` (arkusz `Macierz`), kolumny:
`Lp · ID · Poziom 1 – Obszar · Poziom 2 – Grupa · Funkcjonalność · Opis · Opis biznesowy · Typ · Interfejs ·
Wersja/standard · Identyfikator techniczny · ID funkcji · Dokumentacja · Źródło · Status · Uwagi`.
Zacznij od gotowego `format/SZABLON_macierz_produktu.xlsx`. Zapis: XLSX (edytowalny) + eksport CSV (dla generatora strony) — oba w `dane/produkty/`.

## Metodyka treści (trzymaj się jej)

- **Trzy poziomy**: Poziom 1 = obszar (biznes), Poziom 2 = grupa, Funkcjonalność = konkretne DZIAŁANIE.
- **Jednostka funkcji**: *scalaj* warianty różniące się tylko danymi/formatem/sposobem (np. eksport csv/xlsx/shp = jeden „Eksport");
  *rozbijaj*, gdy parametr zmienia cel (rysowanie linii = pomiar odległości vs poligon = pomiar powierzchni). Aby ocenić — zajrzyj w parametry.
- **Dwa opisy**: `Opis` neutralny („co robi") + `Opis biznesowy` (≈1 zdanie: „Umożliwia… / Wyświetla… / Pozwala…").
- **Typ** ze słownika: `widget/tool/action/złożona` (klient) lub `usługa/operacja API/standard OGC/zadanie GP/funkcja silnika/format/źródło danych/mechanizm bezpieczeństwa/funkcja administracyjna/moduł/wdrożenie` (serwer).
- **Funkcje złożone** (`Typ = złożona`): jedna funkcja = sekwencja kilku elementów, gdzie helper nie ma sensu samodzielnie → jeden wiersz, kilka identyfikatorów w `Identyfikator techniczny`.
- **Hosting ≠ złożona**: kontenery/launchery zostają osobnymi funkcjami; powiązania → `Uwagi`.
- **Interfejs/Wersja** — tylko produkty serwerowe (REST/SOAP/WMS/WMTS/WFS/WPS/OGC API Features + wersja). Klienckie: `—`.

## Identyfikatory (ID) — model dwuwarstwowy

- **`ID` (produktowe)**: format `PREFIKS-obszar.grupa.NN` (np. `QIM-10.3.06`) — prefiks + numer obszaru + numer grupy (w obrębie obszaru) + numer funkcji (w obrębie grupy). Numery obszarów/grup bierz z mapowania w arkuszu Słowniki (nowy obszar/grupa = kolejny numer). UWAGA: zmiana obszaru/grupy funkcji zmienia jej ID.
- **`ID funkcji` (kanoniczne)**: format `FN-NNNNN` z rejestru wspólnego `rejestr_funkcji.csv`. Dla funkcji już znanej **podepnij istniejące** `id_funkcji` (nie twórz nowego) — sprawdź rejestr po nazwie kanonicznej/aliasach. Ta sama funkcja w różnych produktach ma to samo `ID funkcji`.
- **Nie zmyślaj ID.** Jeśli numer nie został jeszcze przydzielony — zostaw puste. Zakazane są ID wdrożeniowe/projektowe (per instancja) oraz ID kodujące pozycję (typu `F-1.1.01`).
- Prefiksy produktów: `IMS`=iMapServer, `ICL`=iMapClient, `QIM`=QuickiMap (nowy produkt = nowy prefiks).

## Procedura

1. **Rozpoznanie materiałów** — ustal, co dostarczono (dokumentacja / kod / konfiguracja) i czego brakuje. Zapisz źródła.
2. **Ekstrakcja kandydatów na funkcje** — zależnie od źródła:
   - *Kod*: kontrolery i mapowania (endpointy), rejestry zadań/usług, definicje modułów, enumy formatów, mechanizmy bezpieczeństwa.
   - *Konfiguracja*: widgets/actions/tools (`command`), warstwy, usługi.
   - *Dokumentacja/baza wiedzy*: typy usług, operacje, opisy, wersje standardów.
3. **Deduplikacja i jednostka funkcji** — scalaj/rozbijaj wg zasad powyżej; zajrzyj w parametry, gdy ten sam element występuje wielokrotnie.
4. **Taksonomia** — nadaj Poziom 1 / Poziom 2 / Funkcjonalność (spójnie w obrębie produktu).
5. **Opisy** — `Opis` i `Opis biznesowy` formułuj NA PODSTAWIE ŹRÓDEŁ. Jeśli źródło nie daje opisu — zostaw puste, `Status = do weryfikacji`.
6. **Metadane techniczne** — `Typ`, `Interfejs`, `Wersja/standard`, `Identyfikator techniczny` wpisuj tylko, gdy wynikają ze źródła.
7. **Identyfikatory** — nadaj `ID` (kolejny wolny numer produktu) i podepnij `ID funkcji` z rejestru; jeśli nie prowadzimy jeszcze rejestru, zostaw ID puste.
8. **Dokumentacja** — `TAK`, jeśli funkcja jest opisana w bazie wiedzy; `NIE`, jeśli komponent nieudokumentowany; puste, jeśli nie sprawdzono.
9. **Źródło i Status** — dla każdego wiersza ustaw `Źródło` (kod/konfiguracja/dokumentacja/baza wiedzy) i `Status` (potwierdzone / do weryfikacji).
10. **Zapis** — od szablonu; wiersze `do weryfikacji` podświetlają się na żółto. Wyeksportuj CSV.
11. **Raport kompletności (OBOWIĄZKOWY)** — na końcu podaj: ile wierszy potwierdzonych vs do weryfikacji; które pola/obszary są niepełne; jakich materiałów brakuje; konkretne pytania do product ownera. Nie „domykaj" luk zgadywaniem.

## Weryfikacja przed oddaniem

- Każdy wiersz: wypełnione `Poziom 1`, `Poziom 2`, `Funkcjonalność`, `Typ` (lub `do weryfikacji`), `Źródło`, `Status`.
- Wartości `Typ`, `Interfejs`, `Dokumentacja`, `Status`, `Źródło` mieszczą się w słownikach; `ID`/`ID funkcji` (jeśli są) mają poprawny format.
- Brak wierszy bez źródła. Brak zmyślonych opisów/wersji/ID.
- Plik otwiera się poprawnie; nagłówki zgodne ze schematem.
- Przekaż plik i pokaż raport kompletności. Zalecane: uruchomić skill „sprawdzanie macierzy funkcjonalności".

## Profile produktów (warianty kolumn)

Jeśli produkt ma uzasadnione odstępstwa od wspólnego schematu (inne nazwy/zestaw kolumn, np. iMapCloud:
`Poziom 1 – Moduł`, kolumna `Model`, brak `Interfejs`/`ID funkcji`, własna taksonomia `Typ`), użyj/utwórz
**profil produktu** w `dane/profile/<produkt>.json` (patrz SCHEMAT, sekcja „Profile produktów").
Buduj macierz zgodnie z profilem; rdzeń (Poziom 1/2, Funkcjonalność, Typ, Źródło, Status) pozostaje wymagany.
Prefiks ID bierz z profilu (np. iMapCloud = `CLD`).
