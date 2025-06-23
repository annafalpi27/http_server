.PHONY: test clean

test:
	@echo "Running unittest test..."
	PYTHONPATH=. python3 -m unittest discover -s test -p "test_endpoints.py"