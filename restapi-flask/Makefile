APP = restapi-flask

test:
	@bandit -x ./tests -r .
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up

setup-dev:
	@kind create cluster --config kubernetes/config/config.yaml
	@kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
	@kubectl wait --namespace metallb-system \
	--for=condition=ready pod \
	--selector=app=metallb \
	--timeout=900s
	@kubectl apply -f manifests/
	@helm upgrade \
		--set image.tag="5.0.8" \
		--set auth.rootPassword="root" \
		--install mongodb ./kubernetes/charts/mongodb
	@kubectl wait \
		--for=condition=ready pod \
		--selector=app.kubernetes.io/component=mongodb \
		--timeout=500s
	@helmfile apply

teardown-dev:
	@kind delete clusters kind

deploy-dev:
	@docker build -t $(APP):latest .
	@kind load docker-image $(APP):latest
	@kubectl apply -f kubernetes/manifests
	@kubectl rollout restart deploy $(APP)

dev: setup-dev deploy-dev
