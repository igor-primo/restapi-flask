APP = restapi

test:
	@bandit -x ./tests -r .
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up