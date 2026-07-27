#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator samodzielnej strony katalogu funkcjonalności iMap.

Czyta listę produktów z MANIFESTU (dane/produkty.yaml), ładuje każdą macierz
z CSV (źródło prawdy) + opcjonalny profil, buduje obiekt DATA i renderuje
JEDNĄ samodzielną stronę HTML (offline) oraz eksport combined.json.

Ścieżki są WZGLĘDNE względem repo (domyślnie ../dane i ../site obok generatora)
i nadpisywalne argumentami CLI. Brak zaszytych ścieżek bezwzględnych.

Użycie:
    python generuj_katalog.py [--dane KATALOG] [--out KATALOG]
                              [--manifest PLIK] [--template PLIK] [--wersja RRRR-MM-DD]
"""
import argparse
import base64
import csv
import datetime
import json
import os
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("Brak PyYAML — zainstaluj: pip install -r requirements.txt\n")
    raise

# Bezpieczne UTF-8 na stdout/stderr (konsola Windows cp1250 vs polskie znaki/symbole)
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# ── Ścieżki bazowe (względne względem tego pliku) ──────────────────────────
GENERATOR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(GENERATOR_DIR)
DEFAULT_DANE = os.path.join(PROJECT_ROOT, "dane")
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "site")
DEFAULT_TEMPLATE = os.path.join(GENERATOR_DIR, "templates", "page.html.tmpl")
FONTS_DIR = os.path.join(GENERATOR_DIR, "templates", "fonts")

# Fonty wbudowywane w HTML jako data-URI — strona ma wyglądać jak Baza Wiedzy
# (Roboto), ale bez wywołań sieciowych do Google Fonts (NFR-1/NFR-3).
# Roboto v51 / Roboto Mono v31 to fonty ZMIENNE: jeden plik = cały zakres 100–900.
# Zakresy unicode skopiowane z Google Fonts (latin oraz latin-ext dla polskich znaków).
UNICODE_LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
                 "U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,"
                 "U+2212,U+2215,U+FEFF,U+FFFD")
UNICODE_LATIN_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,"
                     "U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,"
                     "U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")
FONT_FACES = [
    ("Roboto", "roboto-latin.woff2", UNICODE_LATIN),
    ("Roboto", "roboto-latin-ext.woff2", UNICODE_LATIN_EXT),
    ("Roboto Mono", "roboto-mono-latin.woff2", UNICODE_LATIN),
    ("Roboto Mono", "roboto-mono-latin-ext.woff2", UNICODE_LATIN_EXT),
]


def build_font_css():
    """Zbuduj reguły @font-face z fontami osadzonymi jako data-URI (base64).

    Brak katalogu/plików nie przerywa builda — strona zadziała na foncie
    zastępczym, ale wypisujemy ostrzeżenie, bo wygląd rozjedzie się z Bazą Wiedzy.
    """
    faces = []
    missing = []
    for family, filename, urange in FONT_FACES:
        path = os.path.join(FONTS_DIR, filename)
        if not os.path.isfile(path):
            missing.append(filename)
            continue
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        faces.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:100 900;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');"
            "unicode-range:%s}" % (family, b64, urange)
        )
    if missing:
        sys.stderr.write("UWAGA: brak plikow fontow (%s) — strona uzyje fontu zastepczego.\n"
                         % ", ".join(missing))
    return "\n".join(faces)

# ── Kontrakt schematu (klucze CSV) ─────────────────────────────────────────
BASE_HEADERS = ["Lp", "ID", "Poziom 1 – Obszar", "Poziom 2 – Grupa", "Funkcjonalność",
                "Opis", "Opis biznesowy", "Typ", "Interfejs", "Wersja / standard",
                "Identyfikator techniczny", "ID funkcji", "Dokumentacja", "Źródło",
                "Status", "Uwagi"]
BASE_KEYS = ["lp", "id_produktu", "poziom1", "poziom2", "funkcjonalnosc", "opis",
             "opis_biznesowy", "typ", "interfejs", "wersja_standard",
             "identyfikator_techniczny", "id_funkcji", "dokumentacja", "zrodlo",
             "status", "uwagi"]

LABELS = {"id_produktu": "ID", "poziom1": "Obszar", "poziom2": "Grupa",
          "funkcjonalnosc": "Funkcjonalność", "typ": "Typ", "interfejs": "Interfejs",
          "wersja_standard": "Wersja / standard", "model": "Model",
          "liczba_projektow": "Liczba projektów", "rodzaj": "Rodzaj", "projekt": "Projekt",
          "dokumentacja": "Dok.", "status": "Status"}
DISPLAY_ORDER = ["id_produktu", "poziom1", "poziom2", "funkcjonalnosc", "typ", "rodzaj",
                 "interfejs", "wersja_standard", "model", "liczba_projektow", "projekt",
                 "dokumentacja", "status"]
ALWAYS = ["poziom1", "poziom2", "funkcjonalnosc", "typ"]
PROJEKT_SET = {"MIIP", "Centra Operacyjne", "RIIP", "MineSens", "GEOINFO2", "ORLEN", "GDOS",
               "WIR", "HydroIQ", "GUGIK", "NSIS", "ARiMR/NGIS", "UM Nowa Sól", "ISOK",
               "MZP/MRP", "GAZ", "CAPAP", "EMUiA", "ORLEN VIA", "OZE", "UMWL",
               "UM Świdnica", "UM Wodzisław Śląski", "Wojsko", "AMS", "UM Racibórz",
               "UM Kołobrzeg", "GEOINFO3", "WROSIP", "SIPWW", "GUS", "iMapCloud SaaS"}
CHK = {"✓", "x", "X", "TAK", "1"}
FACETS_ORDER = ["typ", "rodzaj", "interfejs", "model", "projekt", "dokumentacja", "status"]


def build_h2k(profile=None):
    """Zbuduj mapowanie nagłówek→klucz + listę kluczy dodatkowych (z profilu)."""
    h2k = {h: k for h, k in zip(BASE_HEADERS, BASE_KEYS)}
    extra = []
    if profile:
        for h in profile.get("kolumny_wylaczone", []):
            h2k.pop(h, None)
        for h, k in profile.get("aliasy_kolumn", {}).items():
            h2k[h] = k
        for c in profile.get("kolumny_dodatkowe", []):
            h2k[c["naglowek"]] = c["klucz"]
            extra.append(c["klucz"])
    return h2k, extra


def kk(h2k, extra):
    return set(BASE_KEYS) | set(h2k.values()) | set(extra)


def h2key(h, h2k, known):
    """CSV eksportuje klucze snake-case wprost; nagłówki PL mapujemy przez h2k."""
    return h if h in known else h2k.get(h)


def load_rows_csv(path, h2k, known):
    """Wczytaj wiersze z CSV (źródło prawdy). UTF-8 (BOM-tolerant)."""
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        hdr = rd.fieldnames or []
        for d in rd:
            row = {}
            prj = []
            for h in hdr:
                if h in PROJEKT_SET:
                    if (d.get(h, "") or "").strip() in CHK:
                        prj.append(h)
                    continue
                k = h2key(h, h2k, known)
                if k:
                    row[k] = (d.get(h, "") or "").strip()
            if prj:
                row["projekt"] = ";".join(prj)
            if any(row.values()):
                rows.append(row)
    return rows


def build_product(entry, dane_dir):
    """Zbuduj obiekt produktu z pozycji manifestu."""
    key = entry["klucz"]
    name = entry["nazwa"]
    csv_path = os.path.join(dane_dir, "produkty", entry["plik_csv"])
    if not os.path.isfile(csv_path):
        raise FileNotFoundError("Brak pliku CSV produktu '%s': %s" % (name, csv_path))

    profile = None
    if entry.get("profil"):
        prof_path = os.path.join(dane_dir, "profile", entry["profil"])
        if not os.path.isfile(prof_path):
            raise FileNotFoundError("Brak profilu '%s' dla '%s': %s"
                                    % (entry["profil"], name, prof_path))
        with open(prof_path, encoding="utf-8") as f:
            profile = json.load(f)

    h2k, extra = build_h2k(profile)
    known = kk(h2k, extra)
    rows = load_rows_csv(csv_path, h2k, known)

    present = set()
    for r in rows:
        for k, v in r.items():
            if v:
                present.add(k)
    for k in extra:            # zadeklarowane kolumny dodatkowe pokazujemy zawsze
        present.add(k)
    cols = [k for k in DISPLAY_ORDER if k in present or k in ALWAYS]
    facets = [k for k in FACETS_ORDER if k in present]

    labels = dict(LABELS)
    if entry.get("poziom1_label"):    # etykieta „Poziom 1" per produkt (np. Moduł)
        labels["poziom1"] = entry["poziom1_label"]
    columns = [{"k": k, "label": labels.get(k, k)} for k in cols]

    return {"key": key, "name": name, "prefiks": entry.get("prefiks"),
            "poziom1_label": entry.get("poziom1_label") or "Obszar",
            "columns": columns, "facets": facets, "rows": rows}


def resolve_wersja(manifest, dane_dir, cli_wersja):
    """Data danych: --wersja > manifest.wersja_danych > SOURCE_DATE_EPOCH > mtime CSV."""
    if cli_wersja:
        return cli_wersja
    if manifest.get("wersja_danych"):
        return str(manifest["wersja_danych"])
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.datetime.utcfromtimestamp(int(epoch)).date().isoformat()
    prod_dir = os.path.join(dane_dir, "produkty")
    mtimes = [os.path.getmtime(os.path.join(prod_dir, f))
              for f in os.listdir(prod_dir) if f.lower().endswith(".csv")]
    if mtimes:
        return datetime.date.fromtimestamp(max(mtimes)).isoformat()
    return datetime.date.today().isoformat()


def main():
    ap = argparse.ArgumentParser(description="Generator strony katalogu funkcjonalności iMap.")
    ap.add_argument("--dane", default=DEFAULT_DANE, help="Katalog z danymi (produkty/, profile/, produkty.yaml).")
    ap.add_argument("--out", default=DEFAULT_OUT, help="Katalog wynikowy (site/).")
    ap.add_argument("--manifest", default=None, help="Ścieżka do manifestu (domyślnie <dane>/produkty.yaml).")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE, help="Szablon HTML.")
    ap.add_argument("--wersja", default=None, help="Data danych RRRR-MM-DD (nadpisuje autodetekcję).")
    a = ap.parse_args()

    dane_dir = os.path.abspath(a.dane)
    out_dir = os.path.abspath(a.out)
    manifest_path = a.manifest or os.path.join(dane_dir, "produkty.yaml")

    if not os.path.isfile(manifest_path):
        sys.stderr.write("BŁĄD: brak manifestu: %s\n" % manifest_path)
        sys.exit(2)
    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f) or {}
    entries = manifest.get("produkty") or []
    if not entries:
        sys.stderr.write("BŁĄD: manifest nie zawiera listy 'produkty'.\n")
        sys.exit(2)

    products = [build_product(e, dane_dir) for e in entries]
    wersja = resolve_wersja(manifest, dane_dir, a.wersja)

    DATA = {
        "generated": wersja,
        "products": products,
        "wspolne": [{"k": "__p", "label": "Produkt"},
                    {"k": "poziom1", "label": "Obszar"},
                    {"k": "funkcjonalnosc", "label": "Funkcjonalność"},
                    {"k": "typ", "label": "Typ"}],
    }

    os.makedirs(out_dir, exist_ok=True)
    data_json = json.dumps(DATA, ensure_ascii=False, sort_keys=True)

    # combined.json — eksport dla przyszłych integracji (np. ElasticSearch/OpenSearch)
    with open(os.path.join(out_dir, "combined.json"), "w", encoding="utf-8") as f:
        f.write(data_json)

    with open(a.template, encoding="utf-8") as f:
        template = f.read()
    # Kolejność podmian ma znaczenie: __FONTS__ i __DATE__ najpierw, bo __DATA__
    # wstawia duży blok JSON, w którym nie chcemy niczego dalej podmieniać.
    html = (template
            .replace("__FONTS__", build_font_css())
            .replace("__DATE__", wersja)
            .replace("__DATA__", data_json))
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    # ── Podsumowanie ────────────────────────────────────────────────────────
    total = sum(len(p["rows"]) for p in products)
    weryf = sum(1 for p in products for r in p["rows"] if r.get("status") == "do weryfikacji")
    print("=== GENERACJA OK ===")
    print("Manifest : %s" % manifest_path)
    print("Dane     : %s" % dane_dir)
    print("Wynik    : %s (index.html, combined.json)" % out_dir)
    print("Data danych: %s" % wersja)
    for p in products:
        pw = sum(1 for r in p["rows"] if r.get("status") == "do weryfikacji")
        pct = (100.0 * pw / len(p["rows"])) if p["rows"] else 0.0
        print("  - %-11s %4d wierszy | do weryfikacji: %3d (%4.1f%%) | kolumny: %s"
              % (p["name"], len(p["rows"]), pw, pct, [c["k"] for c in p["columns"]]))
    pct_all = (100.0 * weryf / total) if total else 0.0
    print("RAZEM: %d produktów, %d wierszy, do weryfikacji %d (%.1f%%)"
          % (len(products), total, weryf, pct_all))


if __name__ == "__main__":
    main()
