TARGET ?= ./
APP_NAME = hospital_app
IMAGE_NAME ?= sshishov/$(APP_NAME)
IMAGE_VERSION ?= latest
GIT_REF = $(shell git rev-parse HEAD)
TEST_ARGS ?= --cov=$(TARGET) --verbose --cov-report=xml --cov-report=term --junitxml=xmlrunner/unittest.xml

.PHONY: docker

docker-local:
	tar -pczf /tmp/archive.tar.gz --exclude=".git" --exclude="*.pyc" --exclude="local_settings.py" .
	mv /tmp/archive.tar.gz docker/archive.tar.gz
	$(MAKE) docker-common

docker-git:
	git archive --format tar.gz --output docker/archive.tar.gz $(GIT_REF)
	$(MAKE) docker-common

docker-common:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) -f docker/Dockerfile .
	$(MAKE) clean-docker

docker: docker-git

docker-push:
	docker push $(IMAGE_NAME):$(IMAGE_VERSION)

clean-docker:
	-rm -rf docker/archive.tar.gz

clean-pyc:
	find . -name "*.pyc" -exec rm -f {} \;

clean: clean-pyc

lint:
	flake8 --statistics --count $(TARGET)
	pylint core content_first_service *.py

test-unit:
	TEST_ARGS="$(TEST_ARGS) --cov-fail-under=10 -m unit" $(MAKE) lint-test

test-integration:
	TEST_ARGS="$(TEST_ARGS) -m integration" $(MAKE) lint-test

lint-test: lint test

test: clean
	mkdir -p xmlrunner
	coverage erase
	pytest $(TEST_ARGS) $(TARGET)

translate:
	python manage.py makemessages --no-location --no-obsolete --no-wrap --locale ru

release:
	$(MAKE) docker-git
	$(MAKE) docker-push
	eb deploy
