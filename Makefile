.PHONY: develop proto


develop:
	pip install poetry
	poetry install
	pre-commit install


proto:
	protoc -I=./proto --python_out=./kova/protocol/ --pyi_out=./kova/protocol/stubs/ ./proto/*.proto
