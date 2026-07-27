# ─────────────────────────────────────────────────────────────────────────
# Katalog funkcjonalności iMap — obraz multi-stage.
#   Etap 1 (builder): waliduje macierze i generuje statyczną stronę do /site.
#   Etap 2 (runtime):  nginx (nieuprzywilejowany) serwuje /site na porcie 8080.
# W runtime NIE ma Pythona ani żadnych połączeń sieciowych — strona jest statyczna.
# ─────────────────────────────────────────────────────────────────────────

# ── Etap 1: builder ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Powtarzalność / brak cache pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# 1) zależności (osobna warstwa — cache przy niezmienionym requirements.txt)
COPY requirements.txt ./
RUN pip install -r requirements.txt

# 2) generator + dane (źródło prawdy: CSV + profile + manifest)
COPY generator/ ./generator/
COPY dane/ ./dane/

# Opcjonalna, powtarzalna data danych (bajtowo identyczny build):
#   docker build --build-arg WERSJA=2026-07-25 .
ARG WERSJA=""
ENV WERSJA=${WERSJA}

# 3) walidacja (bramka) + generacja do /site; błąd walidacji przerywa build
RUN python generator/build.py --dane ./dane --out /site $( [ -n "$WERSJA" ] && echo --wersja "$WERSJA" )

# ── Etap 2: runtime ─────────────────────────────────────────────────────────
# Obraz „unprivileged": nasłuch na 8080, proces jako uid 101 (nginx), bez roota.
FROM nginxinc/nginx-unprivileged:1.27-alpine AS runtime

# Konfiguracja serwera (port 8080, UTF-8, gzip, typy MIME)
COPY --chown=nginx:nginx nginx/default.conf /etc/nginx/conf.d/default.conf

# Statyczna strona z etapu builder
COPY --from=builder --chown=nginx:nginx /site /usr/share/nginx/html

EXPOSE 8080

# HEALTHCHECK bez curl (nie ma go w obrazie alpine) — busybox wget, bez ruchu zewn.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1

# CMD/ENTRYPOINT/USER dziedziczone z obrazu bazowego (nginx, uid 101).
