# Makefile — skróty do budowania i uruchamiania katalogu funkcjonalności iMap.
# Wymaga: docker (+ compose). Cele "site"/"validate" wymagają lokalnego Pythona.

IMAGE   ?= imap-katalog-web:latest
PORT    ?= 8080
WERSJA  ?=
PYTHON  ?= python

.DEFAULT_GOAL := help

.PHONY: help build up down restart logs regen site validate clean

help:  ## Lista celów
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

build:  ## Zbuduj obraz Docker (walidacja + generacja + nginx)
	docker build --build-arg WERSJA=$(WERSJA) -t $(IMAGE) .

up:  ## Uruchom kontener (compose) w tle → http://localhost:$(PORT)
	WERSJA=$(WERSJA) docker compose up -d --build

down:  ## Zatrzymaj i usuń kontener
	docker compose down

restart:  ## Restart kontenera
	docker compose restart

logs:  ## Podgląd logów kontenera
	docker compose logs -f

regen:  ## Przegeneruj ./site w kontenerze (bez lokalnego Pythona, bez przebudowy obrazu)
	docker run --rm -v "$(CURDIR)":/work -w /work python:3.12-slim \
		sh -c "pip install -q -r requirements.txt && python generator/build.py --dane ./dane --out ./site --wersja '$(WERSJA)'"

site:  ## Zbuduj stronę lokalnie do ./site (walidacja + generacja)
	$(PYTHON) generator/build.py --dane ./dane --out ./site $(if $(WERSJA),--wersja $(WERSJA),)

validate:  ## Uruchom samą walidację (bez generacji) lokalnie
	@for f in dane/produkty/*.csv; do echo "== $$f =="; $(PYTHON) generator/sprawdz_macierz.py "$$f"; done

clean:  ## Usuń wygenerowaną stronę
	rm -rf site/*
