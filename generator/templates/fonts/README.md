# Fonty wbudowane w stronę

Pliki `.woff2` w tym katalogu są **wbudowywane w wynikowy HTML jako data-URI** przez
`generator/generuj_katalog.py`. Dzięki temu strona wygląda identycznie jak Baza Wiedzy,
a jednocześnie spełnia wymaganie „zero wywołań sieciowych" (NFR-1 / NFR-3) — nie ładujemy
Google Fonts z CDN.

| Plik | Rodzina | Zakres znaków |
|---|---|---|
| `roboto-latin.woff2` | Roboto | latin |
| `roboto-latin-ext.woff2` | Roboto | latin-ext (polskie znaki) |
| `roboto-mono-latin.woff2` | Roboto Mono | latin |
| `roboto-mono-latin-ext.woff2` | Roboto Mono | latin-ext |

To **fonty zmienne** (variable) — jeden plik obsługuje cały zakres grubości `100–900`,
dlatego nie ma osobnych plików dla 400 i 700.

## Licencja

Roboto i Roboto Mono — **Apache License 2.0**, © Google.
Licencja zezwala na redystrybucję, także w formie wbudowanej w plik HTML.
Pełny tekst: https://www.apache.org/licenses/LICENSE-2.0

## Aktualizacja

Pliki pobrano z Google Fonts (`fonts.gstatic.com`, Roboto v51 / Roboto Mono v31).
Aby je odświeżyć, pobierz nowe `.woff2` dla zakresów `latin` i `latin-ext`
i podmień pliki pod tymi samymi nazwami — generator nie wymaga zmian.
