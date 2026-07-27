#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline budowania katalogu: (a) walidacja KAŻDEJ macierzy → (b) generacja → podsumowanie.

Fail-fast: pierwszy błąd walidacji przerywa build (kod wyjścia 1), strona NIE powstaje.

Użycie:
    python build.py [--dane KATALOG] [--out KATALOG] [--wersja RRRR-MM-DD]
"""
import argparse
import os
import subprocess
import sys

import yaml

import sprawdz_macierz as val

# Bezpieczne UTF-8 na stdout/stderr (konsola Windows cp1250 vs symbole ✓/✗/polskie znaki)
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

GENERATOR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(GENERATOR_DIR)
DEFAULT_DANE = os.path.join(PROJECT_ROOT, "dane")
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "site")


def validate_one(csv_path, profil_path):
    """Zwróć (errors, warnings, stats) dla jednej macierzy."""
    profile = val.load_profile(profil_path) if profil_path else {}
    sch = val.build_schema(profile)
    rows, header = val.load(csv_path, "Macierz", sch)
    if isinstance(header, str) and not rows:
        return [header], [], {"wiersze": 0}
    return val.validate(rows, header, sch)


def main():
    ap = argparse.ArgumentParser(description="Build: walidacja (bramka) + generacja strony.")
    ap.add_argument("--dane", default=DEFAULT_DANE)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--wersja", default=None)
    a = ap.parse_args()

    dane_dir = os.path.abspath(a.dane)
    out_dir = os.path.abspath(a.out)
    manifest_path = os.path.join(dane_dir, "produkty.yaml")

    if not os.path.isfile(manifest_path):
        sys.stderr.write("BŁĄD: brak manifestu: %s\n" % manifest_path)
        sys.exit(2)
    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f) or {}
    entries = manifest.get("produkty") or []
    if not entries:
        sys.stderr.write("BŁĄD: manifest nie zawiera listy 'produkty'.\n")
        sys.exit(2)

    print("=== (1/2) WALIDACJA (bramka) ===")
    total_err = 0
    total_warn = 0
    for e in entries:
        csv_path = os.path.join(dane_dir, "produkty", e["plik_csv"])
        profil_path = os.path.join(dane_dir, "profile", e["profil"]) if e.get("profil") else None
        if not os.path.isfile(csv_path):
            sys.stderr.write("BŁĄD: brak CSV dla '%s': %s\n" % (e["nazwa"], csv_path))
            sys.exit(1)
        errors, warnings, stats = validate_one(csv_path, profil_path)
        total_warn += len(warnings)
        flaga = "OK" if not errors else "BŁĘDY"
        print("  [%-5s] %-11s profil=%-14s wierszy=%-4s błędy=%d ostrzeżenia=%d"
              % (flaga, e["nazwa"], (e.get("profil") or "(rdzeń)"),
                 stats.get("wiersze", "?"), len(errors), len(warnings)))
        if errors:
            total_err += len(errors)
            for msg in errors[:30]:
                print("        ✗ %s" % msg)
    if total_err:
        sys.stdout.flush()
        sys.stderr.write("\nWALIDACJA NIEUDANA: %d błędów. Build przerwany, strona nie powstała.\n" % total_err)
        sys.exit(1)
    print("Walidacja OK (ostrzeżenia: %d — nie blokują buildu)." % total_warn)

    print("\n=== (2/2) GENERACJA ===")
    sys.stdout.flush()   # wypchnij logi walidacji przed wyjściem podprocesu
    cmd = [sys.executable, os.path.join(GENERATOR_DIR, "generuj_katalog.py"),
           "--dane", dane_dir, "--out", out_dir]
    if a.wersja:
        cmd += ["--wersja", a.wersja]
    rc = subprocess.call(cmd)
    if rc != 0:
        sys.stderr.write("BŁĄD generacji (kod %d).\n" % rc)
        sys.exit(rc)


if __name__ == "__main__":
    main()
