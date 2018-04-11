TARGET ?= ./
APP_NAME = content_first_service
BEANSTALK_APP_NAME = content-first-service
IMAGE_NAME ?= dubizzledotcom/$(APP_NAME)
IMAGE_VERSION ?= $(shell docker/tag_helper.sh)
SOURCE_BUNDLE_ARCHIVE_NAME = $(BEANSTALK_APP_NAME)-$(IMAGE_VERSION).zip
GIT_REF = $(shell git rev-parse HEAD)
TEST_ARGS ?= --cov=$(TARGET) --verbose --cov-report=xml --cov-report=term --junitxml=xmlrunner/unittest.xml

.PHONY: docker

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
